---
title: MeTTa 模块系统全链分析
order: 14
---

# 文档 14：模块系统（MeTTa → Python → Rust）

本文档覆盖 `import!`、`include`、模块名解析、`MettaMod` / `ModuleSpace` 依赖与查询级联、Python 文件模块加载与 `ext.py` 装饰器，以及 C API `module_loader_t` 与 `hyperonpy` 中的 `module_loader_*` 桥接。

---

## 1. MeTTa 表面形式与文档注释

`stdlib.metta` 中对 `import!` / `include` 的 `@doc` 与类型声明：

```1252:1263:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc import!
  (@desc "Imports module using its relative path (second argument), which could contain ':' as a path separation (e.g. !(import &module relative:path:to:module)) and binds it to the token (first argument) which will represent imported atomspace. If first argument is &self then everything will be imported to current atomspace)")
  (@params (
    (@param "Symbol, which is turned into the token for accessing the imported module")
    (@param "Module name/relative path to module")))
  (@return "Unit atom"))

(@doc include
  (@desc "Works just like import! but with &self as a first argument. So everything from input file will be included in the current atomspace and evaluated")
  (@params (
    (@param "Name of metta script to import")))
  (@return "Unit atom"))
```

注意：`include` 在 MeTTa 中**仅一个参数**（模块名）；语义上等价于「目标为当前空间」的包含，见下文 Rust `IncludeOp`。

---

## 2. Rust：`import!`（ImportOp）全链

### 2.1 算子定义与 `RunContext` 访问

`ImportOp` 通过 `Metta` 内共享的 `context` 栈取得当前 `RunContext`（与 `IncludeOp` 等相同 hack，见源码注释）：

```14:25:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\module.rs
#[derive(Clone, Debug)]
pub struct ImportOp {
    context: std::sync::Arc<std::sync::Mutex<Vec<std::sync::Arc<std::sync::Mutex<&'static mut RunContext<'static, 'static>>>>>>,
}

impl ImportOp {
    pub fn new(metta: Metta) -> Self {
        Self{ context: metta.0.context.clone() }
    }
}
```

`execute` 核心逻辑：

```71:104:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\module.rs
        let dest_arg = args.get(0).ok_or_else(arg_error)?;
        let mod_name = args.get(1).and_then(expect_string_like_atom).ok_or_else(arg_error)?;
        let ctx_ref = self.context.lock().unwrap().last().unwrap().clone();
        let mut context = ctx_ref.lock().unwrap();
        let mod_id = context.load_module(&mod_name)?;

        match dest_arg {
            Atom::Symbol(dest_sym) => {
                context.import_dependency_as(mod_id, Some(dest_sym.name().to_string()))?;
            }
            other_atom => {
                match &other_atom {
                    Atom::Grounded(_) if Atom::as_gnd::<DynSpace>(other_atom) == Some(&context.module().space()) => {
                        context.import_all_from_dependency(mod_id)?;
                    },
                    _ => {
                        return Err(format!("import! destination argument must be a symbol atom naming a new space, or &self.  Found: {other_atom:?}").into());
                    }
                }
            }
        }
```

**行为归纳**（与源码内注释一致）：

- 第一个参数为**符号**：`import_dependency_as`，相当于「导入为命名空间 / tokenizer 中的模块 space 句柄」。
- 第一个参数为**当前模块的 `&self` space**：`import_all_from_dependency`，相当于「from module import *」式合并（含 token 导出等，仍标记为 WIP）。

### 2.2 `RunContext::load_module` → 解析与 `ModuleLoader`

```862:878:d:\dev\hyperon-experimental\lib\src\metta\runner\mod.rs
    pub fn load_module(&mut self, mod_name: &str) -> Result<ModId, String> {
        let absolute_mod_path = self.normalize_module_name(mod_name)?;

        if let Ok(mod_id) = self.get_module_by_name(&absolute_mod_path) {
            return Ok(mod_id);
        }

        #[cfg(not(feature = "pkg_mgmt"))]
        return Err(format!("Failed to resolve module {absolute_mod_path}"));

        #[cfg(feature = "pkg_mgmt")]
        {
            let parent_mod_id = self.load_module_parents(&absolute_mod_path)?;
            self.load_module_internal(&absolute_mod_path, parent_mod_id)
        }
    }
```

无 `pkg_mgmt` 特性时，未缓存的模块名会直接失败；典型发行构建需启用包管理以解析依赖。

`load_module_internal` 在父模块上下文中调用 `resolve_module`，再 `get_or_init_module_with_descriptor`（`mod.rs` 908–918 行）。

### 2.3 `ModuleInitState::init_module` 与 `ModuleLoader::load`

加载新模块时创建 `RunnerState::new_for_loading`，将 `loader.load(context)` 压入输入流并逐步 `run_step`，最后 `finalize_loading`：

```439:465:d:\dev\hyperon-experimental\lib\src\metta\runner\modules\mod.rs
    pub fn init_module(&mut self, runner: &Metta, mod_name: &str, loader: Box<dyn ModuleLoader>) -> Result<ModId, String> {
        let mut runner_state = RunnerState::new_for_loading(runner, mod_name, self);
        runner_state.run_in_context(|context| {
            context.push_func(|context| loader.load(context));
            Ok(())
        })?;
        while !runner_state.is_complete() {
            runner_state.run_step()?;
        }
        let mod_id = runner_state.finalize_loading()?;
        self.in_frame(mod_id, |frame| Rc::get_mut(frame.the_mod.as_mut().unwrap()).unwrap().set_loader(loader));
        Ok(mod_id)
    }
```

`ModuleLoader` trait（加载主体、token 导出、资源）：

```559:605:d:\dev\hyperon-experimental\lib\src\metta\runner\modules\mod.rs
pub trait ModuleLoader: std::fmt::Debug + Send + Sync {
    fn load(&self, context: &mut RunContext) -> Result<(), String>;
    // ...
    fn load_tokens(&self, _target: &MettaMod, _metta: Metta) -> Result<(), String> {
        Ok(())
    }
}
```

### 2.4 `MettaMod::import_dependency_as`：token 合并（子模块 space 句柄）

```107:127:d:\dev\hyperon-experimental\lib\src\metta\runner\modules\mod.rs
    pub(crate) fn import_dependency_as(&self, mod_ptr: Rc<MettaMod>, name: Option<String>) -> Result<(), String> {
        let dep_space = mod_ptr.space().clone();
        let name = match name {
            Some(name) => name,
            None => mod_ptr.name().to_string()
        };
        let new_space_token = if name.starts_with('&') {
            name
        } else {
            format!("&{name}")
        };
        let dep_space_atom = Atom::gnd(dep_space);
        self.tokenizer.borrow_mut().register_token_with_regex_str(&new_space_token, move |_| { dep_space_atom.clone() });
        Ok(())
    }
```

### 2.5 `MettaMod::import_all_from_dependency`：`ModuleSpace.deps` + `load_tokens`

```179:206:d:\dev\hyperon-experimental\lib\src\metta\runner\modules\mod.rs
    pub(crate) fn import_all_from_dependency(&self, mod_id: ModId, mod_ptr: Rc<MettaMod>, metta: &Metta) -> Result<(), String> {
        if self.contains_imported_dep(&mod_id) {
            return Ok(())
        }
        let (dep_space, transitive_deps) = mod_ptr.stripped_space();
        self.insert_dep(mod_id, dep_space.clone())?;
        if let Some(transitive_deps) = transitive_deps {
            for (dep_mod_id, dep_space) in transitive_deps {
                self.insert_dep(dep_mod_id, dep_space)?;
            }
        }
        match &mod_ptr.loader {
            Some(loader) => loader.load_tokens(self, metta.clone()),
            None => Ok(()),
        }
    }
```

`RunContext` 上的薄封装：

```989:1026:d:\dev\hyperon-experimental\lib\src\metta\runner\mod.rs
    pub fn import_dependency_as(&self, mod_id: ModId, name: Option<String>) -> Result<(), String> {
        self.module().import_dependency_as(self.get_mod_ptr(mod_id)?, name)
    }
    pub fn import_all_from_dependency(&self, mod_id: ModId) -> Result<(), String> {
        self.module().import_all_from_dependency(mod_id, self.get_mod_ptr(mod_id)?, self.metta)
    }
```

### 2.6 Runner 将 `RunContext` 压栈供 `import!` 使用

```631:644:d:\dev\hyperon-experimental\lib\src\metta\runner\mod.rs
        self.metta.0.context.lock().unwrap().push(Arc::new(Mutex::new( unsafe{ std::mem::transmute(&mut context) } )));
        let result = f(&mut context);
        self.metta.0.context.lock().unwrap().pop();
```

---

## 3. Rust：`include`（IncludeOp）

```131:151:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\module.rs
impl CustomExecute for IncludeOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let mod_name = args.get(0).and_then(expect_string_like_atom).ok_or_else(arg_error)?;
        let ctx_ref = self.context.lock().unwrap().last().unwrap().clone();
        let mut context = ctx_ref.lock().unwrap();
        let resource = context.load_resource_from_module(&mod_name, ResourceKey::MainMettaSrc)?;
        let parser = crate::metta::text::SExprParser::new(resource);
        let eval_result = context.run_inline(|context| {
            context.push_parser(Box::new(parser));
            Ok(())
        })?;
        Ok(eval_result.into_iter().last().unwrap_or_else(|| vec![]))
    }
}
```

链：`load_resource_from_module`（可先加载父模块，见 `mod.rs` 925–947 行）→ 当前 `mod_id` 下 `run_inline` 解析并执行 → 原子进入**当前**模块 space（与 `import! &self` 的依赖图语义不同：include 是内联执行源文本）。

---

## 4. 模块名解析：`ModNameNode` 树与分层查找

### 4.1 约定：`top` / `self` / 分隔符

```6:21:d:\dev\hyperon-experimental\lib\src\metta\runner\modules\mod_names.rs
pub const TOP_MOD_NAME: &'static str = "top";
pub const SELF_MOD_NAME: &'static str = "self";
pub const MOD_NAME_SEPARATOR: char = ':';
```

`normalize_relative_module_name` 将相对名规范为以 `top` 开头的绝对路径（87–104 行）。

### 4.2 已加载模块：`resolve` vs 加载中帧：`resolve_layered`

```264:277:d:\dev\hyperon-experimental\lib\src\metta\runner\modules\mod_names.rs
    pub fn resolve(&self, name: &str) -> Option<ModId> {
        self.name_to_node::<&Self>(&[], name).map(|node| node.mod_id)
    }
    pub fn resolve_layered<SelfRefT: core::borrow::Borrow<Self>>(&self, subtrees: &[(&str, SelfRefT)], name: &str) -> Option<ModId> {
        self.name_to_node(subtrees, name).map(|node| node.mod_id)
    }
```

`ModuleInitState::get_module_by_name` 在 Root/Child 状态下把各 `InitFrame` 的 `sub_module_names` 与 runner 全局树一起做 `resolve_layered`：

```392:411:d:\dev\hyperon-experimental\lib\src\metta\runner\modules\mod.rs
    pub fn get_module_by_name(&self, runner: &Metta, mod_name: &str) -> Result<ModId, String> {
        let mod_id = match self {
            Self::Root(cell) |
            Self::Child(cell) => {
                let insides_ref = cell.borrow();
                let mut subtree_pairs = vec![];
                for frame in insides_ref.frames.iter() {
                    subtree_pairs.push((frame.path(), &frame.sub_module_names));
                }
                let module_names = runner.0.module_names.lock().unwrap();
                module_names.resolve_layered(&subtree_pairs[..], mod_name).ok_or_else(|| format!("Unable to locate module: {mod_name}"))
            },
            Self::None => runner.get_module_by_name(mod_name)
        }?;
        // INVALID 检查 ...
    }
```

`RunContext::get_module_by_name` 先 `normalize_relative_module_name(self.module().path(), mod_name)` 再委托 `init_state`（`mod.rs` 774–777 行）。

`Metta::merge_init_state` 将子模块名子树合并进 runner 的全局 `module_names`（`mod.rs` 357–390 行）。

---

## 5. `ModuleSpace`：依赖子空间与查询级联

模块的 `DynSpace` 内层为 `ModuleSpace::new` 包装（`modules/mod.rs` 76 行）。

```33:47:d:\dev\hyperon-experimental\lib\src\space\module.rs
    pub fn query(&self, query: &Atom) -> BindingsSet {
        complex_query(query, |query| self.single_query(query))
    }
 
    fn single_query(&self, query: &Atom) -> BindingsSet {
        let mut results = self.main.borrow().query(query);
        for dep in &self.deps {
            if let Some(space) = dep.borrow().as_any().downcast_ref::<Self>()  {
                results.extend(space.query_no_deps(query));
            } else {
                panic!("Only ModuleSpace is expected inside dependencies collection");
            }
        }
        results
    }
```

`import_all_from_dependency` 通过 `insert_dep` → `ModuleSpace::add_dep` 把依赖 space 挂入 `deps`（`modules/mod.rs` 215–224 行）。因此 **`match` / 类型查询等凡经由 `module().space()` 的路径都会级联到已导入依赖**，而 `module-space-no-deps` 仅保留主空间（`module.rs` `module_space_no_deps` 199–207 行）。

---

## 6. `&self` 在模块上下文中的含义

Tokenizer 将正则 `&self` 映射为**当前**模块空间的 `Atom::gnd(DynSpace)`：

```81:82:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\mod.rs
    let self_atom = Atom::gnd(space.clone());
    tref.register_token(regex(r"&self"), move |_| { self_atom.clone() });
```

`import!` 通过比较 `other_atom` 的 grounded space 与 `context.module().space()` 判断是否「导入到当前模块」（`stdlib/module.rs` 88–89 行）。

---

## 7. Python：环境与单文件 / 包模块加载

### 7.1 `MeTTa.__init__`：注册 `_PyFileMeTTaModFmt` 与 include 路径

```120:132:d:\dev\hyperon-experimental\python\hyperon\runner.py
            hp.env_builder_push_fs_module_format(env_builder, _PyFileMeTTaModFmt)
            builtin_mods_path = os.path.join(os.path.dirname(__file__), 'exts')
            hp.env_builder_push_include_path(env_builder, builtin_mods_path)
            py_site_packages_paths = site.getsitepackages()
            for path in py_site_packages_paths:
                hp.env_builder_push_include_path(env_builder, path)
            self.cmetta = hp.metta_new_with_stdlib_loader(_priv_load_module_stdlib, space.cspace, env_builder)
```

### 7.2 `_PyFileMeTTaModFmt`：`try_path` 与 `loader_func`

对应「单文件 `.py`」或「目录 + `__init__.py`」：

```288:334:d:\dev\hyperon-experimental\python\hyperon\runner.py
class _PyFileMeTTaModFmt:
    def try_path(path, metta_mod_name):
        path = path if path.endswith(".py") else os.path.splitext(path)[0] + ".py"
        if not os.path.exists(path):
            dir_path = os.path.join(os.path.splitext(path)[0], "__init__.py")
            if os.path.exists(dir_path):
                path = dir_path
            else:
                return None
        spec = importlib.util.spec_from_file_location(metta_mod_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[metta_mod_name] = module
        spec.loader.exec_module(module)
        def loader_func(tokenizer, metta):
            _priv_register_module_tokens(metta_mod_name, tokenizer, metta)
        return {
            'pymod_name': metta_mod_name,
            'path': path,
            'loader_func': loader_func,
        }
```

### 7.3 `_priv_load_module`：等价于 Rust `RunContext::init_self_module` + 注册 token

```336:345:d:\dev\hyperon-experimental\python\hyperon\runner.py
def _priv_load_module(loader_func, path, c_run_context):
    run_context = RunContext(c_run_context)
    if path is not None:
        resource_dir = os.path.dirname(path)
    else:
        resource_dir = None
    space = GroundingSpaceRef()
    run_context.init_self_module(space, resource_dir)
    loader_func(run_context.tokenizer(), run_context.metta())
```

`load_module_direct_from_pymod` 将 `loader_func` 交给 `metta_load_module_direct`（181–193 行）。

### 7.4 `RunContext.load_module`（Python）

```88:90:d:\dev\hyperon-experimental\python\hyperon\runner.py
    def load_module(self, mod_name):
        """Resolves a module by name in the context of the running module, and loads it into the runner"""
        return hp.run_context_load_module(self.c_run_context, mod_name)
```

### 7.5 `_priv_register_module_tokens`：消费装饰器元数据

```372:392:d:\dev\hyperon-experimental\python\hyperon\runner.py
def _priv_register_module_tokens(pymod_name, tokenizer, metta):
    mod = import_module(pymod_name)
    for n in dir(mod):
        obj = getattr(mod, n)
        if 'metta_type' in dir(obj):
            typ = obj.metta_type
            if obj.metta_pass_metta:
                items = obj(metta)
            else:
                items = obj()
            if typ == RegisterType.ATOM:
                def register(r, a):
                    tokenizer.register_token(r, lambda _: a)
                for rex, atom in items.items():
                    register(rex, atom)
            elif typ == RegisterType.TOKEN:
                for rex, lam in items.items():
                    tokenizer.register_token(rex, lam)
```

---

## 8. Python：`ext.py` 装饰器

`@register_atoms` / `@register_tokens` 通过 `mark_register_function` 写入 `metta_type` 与 `metta_pass_metta`：

```59:81:d:\dev\hyperon-experimental\python\hyperon\ext.py
def register_atoms(*args, **kwargs):
    return mark_register_function(RegisterType.ATOM, args, kwargs)

def register_tokens(*args, **kwargs):
    return mark_register_function(RegisterType.TOKEN, args, kwargs)
```

`@grounded` 生成 `OperationAtom` 并可选立即 `metta.register_atom`：

```83:104:d:\dev\hyperon-experimental\python\hyperon\ext.py
def _register_grounded(metta, func):
    name = func.__name__
    func_atom = OperationAtom(name, func, unwrap=True)
    if metta is not None:
        metta.register_atom(name, func_atom)
    else:
        return mark_register_function(RegisterType.ATOM, [lambda: {name: func_atom}], [])

def grounded(arg):
    if callable(arg):
        return _register_grounded(None, arg)
    else:
        return lambda func: _register_grounded(arg, func)
```

---

## 9. C API：`module_loader_t` 与 Rust `CModuleLoader`

C 头文件侧结构体（字段为函数指针）：

```45:72:d:\dev\hyperon-experimental\c\src\module.rs
#[repr(C)] 
pub struct module_loader_t {
    load: Option<extern "C" fn(payload: *const c_void, context: *mut run_context_t, err: write_t) -> isize>,
    load_tokens: Option<extern "C" fn(payload: *const c_void, target: metta_mod_ref_t, metta: metta_t, err: write_t) -> isize>,
    to_string: Option<extern "C" fn(payload: *const c_void, text: write_t)>,
    free: Option<extern "C" fn(payload: *mut c_void)>,
}
```

`CModuleLoader` 实现 Rust `ModuleLoader` trait，把调用转发到 C 函数指针（`c/src/module.rs` 135–149 行）。

---

## 10. `hyperonpy`：`module_loader_*` 与 Python 加载函数对接

Python 扩展将 `loader_func` 封进 `python_module_loader_t`，并填充 `module_loader_t` 的四个回调：

```547:607:d:\dev\hyperon-experimental\python\hyperonpy.cpp
struct python_module_loader_t {
    module_loader_t api;
    std::string name;
    py::function loader_func;
    nonstd::optional<std::string> path;
};

ssize_t module_loader_load(void const* pyloader, run_context_t* run_context, write_t err) {
    python_module_loader_t const* loader = static_cast<python_module_loader_t const*>(pyloader);
    py::object runner_mod = py::module_::import("hyperon.runner");
    py::function load = runner_mod.attr("_priv_load_module");
    // load(loader_func, path, &c_run_context);
}

ssize_t module_loader_load_tokens(void const* pyloader, metta_mod_ref_t target, metta_t metta, write_t err) {
    py::function load_tokens = runner_mod.attr("_priv_load_module_tokens");
    // ...
}

module_loader_t* module_loader_new(std::string name, py::function loader_func, nonstd::optional<std::string> path) {
    loader->api.load = module_loader_load;
    loader->api.load_tokens = module_loader_load_tokens;
    loader->api.to_string = module_loader_to_string;
    loader->api.free = module_loader_free;
}
```

由此：**Python 的 `loader_func(tokenizer, metta)`** 与 **C 插件的 `module_loader_t`** 统一映射到同一套 Rust `ModuleLoader` 抽象。

---

## 11. 相关辅助算子（package / 调试）

- `register-module!` / `git-module!`：`lib/src/metta/runner/stdlib/package.rs`（`Metta::load_module_at_path` 或 git 描述符路径）。
- `mod-space!`：`stdlib/module.rs` 183–196 行，`load_module` 后返回 `Atom::gnd(context.metta().module_space(mod_id))`。
- `print-mods!`：`display_loaded_modules`（`mod.rs` 336–340 行）。

---

## 12. 参考文件列表

| 主题 | 路径 |
|------|------|
| import/include/bind/mod-space | `lib/src/metta/runner/stdlib/module.rs` |
| Runner / RunContext | `lib/src/metta/runner/mod.rs` |
| MettaMod / ModuleLoader / Init | `lib/src/metta/runner/modules/mod.rs` |
| 模块名树 | `lib/src/metta/runner/modules/mod_names.rs` |
| ModuleSpace 查询 | `lib/src/space/module.rs` |
| Python Runner | `python/hyperon/runner.py` |
| 装饰器 | `python/hyperon/ext.py` |
| C module_loader | `c/src/module.rs` |
| pybind 桥 | `python/hyperonpy.cpp` |
