---
title: MeTTa 空间操作全链分析
order: 8
---

# 文档 8：空间操作（MeTTa → Rust 算子 → GroundingSpace → Python/C）

本文档追踪 **`new-space`**、**`add-atom`**、**`remove-atom`**、**`get-atoms`**、**`match`（带 space 参数）**、**`&self`**、**空间作为一等值（`DynSpace` grounded atom）**、**观察者模式（`SpaceEvent` / `SpaceObserver`）**，以及 Python **`AbstractSpace` / `GroundingSpaceRef` / `SpaceRef`** 与 C API **`space_new`**、**`space_add`**、**`space_remove`**、**`space_query`** 的对应关系。

---

## 1. MeTTa 标准库中的空间相关文档块（节选）

空间算子的 **文档与类型说明** 集中在 `stdlib.metta`（实现多为 Rust grounded + 少数 MeTTa 包装）：

```1008:1024:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc new-space
  (@desc "Creates new Atomspace which could be used further in the program as a separate from &self Atomspace")
  (@params ())
  (@return "Reference to a new space"))

(@doc remove-atom
  (@desc "Removes atom from the input Atomspace")
  (@params (
    (@param "Reference to the space from which the Atom needs to be removed")
    (@param "Atom to be removed")))
  (@return "Unit atom"))

(@doc get-atoms
  (@desc "Shows all atoms in the input Atomspace")
  (@params (
    (@param "Reference to the space")))
  (@return "List of all atoms in the input space"))
```

**`match` 的文档**（三参数：space、pattern、template）：

```1050:1056:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc match
  (@desc "Searches for all declared atoms corresponding to the given pattern (second argument) inside space (first argument) and returns the output template (third argument)")
  (@params (
    (@param "Atomspace to search pattern")
    (@param "Pattern atom to be searched")
    (@param "Output template typically containing variables from the input pattern")))
  (@return "If match was successfull it outputs template (third argument) with filled variables (if any were present in pattern) using matched pattern (second argument). Empty - otherwise"))
```

---

## 2. `new-space`：`NewSpaceOp` → `DynSpace::new(GroundingSpace::new())`

### 2.1 Rust 实现（`lib/src/metta/runner/stdlib/space.rs`）

```12:36:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
#[derive(Clone, Debug)]
pub struct NewSpaceOp {}

grounded_op!(NewSpaceOp, "new-space");

impl Grounded for NewSpaceOp {
    fn type_(&self) -> Atom {
        Atom::expr([ARROW_SYMBOL, ATOM_TYPE_SPACE])
    }
    // ...
}

impl CustomExecute for NewSpaceOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        if args.len() == 0 {
            let space = Atom::gnd(DynSpace::new(GroundingSpace::new()));
            Ok(vec![space])
        } else {
            Err("new-space doesn't expect arguments".into())
        }
    }
}
```

### 2.2 分词器注册

```206:208:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
    let new_space_op = Atom::gnd(NewSpaceOp{});
    tref.register_token(regex(r"new-space"), move |_| { new_space_op.clone() });
```

### 2.3 C API：新建 grounding 空间

`space_new_grounding_space` 与通用 `space_new`：

```256:259:d:\dev\hyperon-experimental\c\src\space.rs
#[no_mangle]
pub extern "C" fn space_new_grounding_space() -> space_t {
    DynSpace::new(GroundingSpace::new()).into()
}
```

```68:72:d:\dev\hyperon-experimental\c\src\space.rs
#[no_mangle]
pub extern "C" fn space_new(api: *const space_api_t, payload: *mut c_void) -> space_t {
    let c_space = CSpace::new(api, payload);
    DynSpace::new(c_space).into()
}
```

### 2.4 Python

`GroundingSpaceRef` 默认构造调用 `hp.space_new_grounding()`：

```263:276:d:\dev\hyperon-experimental\python\hyperon\base.py
class GroundingSpaceRef(SpaceRef):
    // ...
    def __init__(self, cspace = None):
        if cspace is None:
            self.cspace = hp.space_new_grounding()
        else:
            self.cspace = cspace
```

---

## 3. `add-atom`：`AddAtomOp` → `space.borrow_mut().add()`

```151:176:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
#[derive(Clone, Debug)]
pub struct AddAtomOp {}

grounded_op!(AddAtomOp, "add-atom");
// ...
impl CustomExecute for AddAtomOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let arg_error = || ExecError::from("add-atom expects two arguments: space and atom");
        let space = args.get(0).ok_or_else(arg_error)?;
        let atom = args.get(1).ok_or_else(arg_error)?;
        let space = Atom::as_gnd::<DynSpace>(space).ok_or("add-atom expects a space as the first argument")?;
        space.borrow_mut().add(atom.clone());
        unit_result()
    }
}
```

### 3.1 `GroundingSpace::add` 与观察者

```70:74:d:\dev\hyperon-experimental\lib\src\space\grounding\mod.rs
    pub fn add(&mut self, atom: Atom) {
        log::debug!("GroundingSpace::add: {}, atom: {}", self, atom);
        self.index.insert(atom.clone());
        self.common.notify_all_observers(&SpaceEvent::Add(atom));
    }
```

### 3.2 C API：`space_add`

```139:143:d:\dev\hyperon-experimental\c\src\space.rs
#[no_mangle]
pub extern "C" fn space_add(space: *mut space_t, atom: atom_t) {
    let dyn_space = unsafe{ &*space }.borrow();
    dyn_space.borrow_mut().add(atom.into_inner());
}
```

### 3.3 Python：`SpaceRef.add_atom`

```205:209:d:\dev\hyperon-experimental\python\hyperon\base.py
    def add_atom(self, atom):
        """
        Add an Atom to the Space.
        """
        hp.space_add(self.cspace, atom.catom)
```

`GroundingSpace` 包装类委托 `gspace.add_atom`（`base.py` 77–81 行）。

---

## 4. `remove-atom`：`RemoveAtomOp` → `borrow_mut().remove()`

```178:203:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
impl CustomExecute for RemoveAtomOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let arg_error = || ExecError::from("remove-atom expects two arguments: space and atom");
        let space = args.get(0).ok_or_else(arg_error)?;
        let atom = args.get(1).ok_or_else(arg_error)?;
        let space = Atom::as_gnd::<DynSpace>(space).ok_or("remove-atom expects a space as the first argument")?;
        space.borrow_mut().remove(atom);
        unit_result()
    }
}
```

### 4.1 `GroundingSpace::remove`

```92:98:d:\dev\hyperon-experimental\lib\src\space\grounding\mod.rs
    pub fn remove(&mut self, atom: &Atom) -> bool {
        log::debug!("GroundingSpace::remove: {}, atom: {}", self, atom);
        let is_removed = self.index.remove(atom);
        if is_removed {
            self.common.notify_all_observers(&SpaceEvent::Remove(atom.clone()));
        }
        is_removed
    }
```

### 4.2 C API：`space_remove`

```151:156:d:\dev\hyperon-experimental\c\src\space.rs
#[no_mangle]
pub extern "C" fn space_remove(space: *mut space_t, atom: *const atom_ref_t) -> bool {
    let dyn_space = unsafe{ &*space }.borrow();
    let atom = unsafe{ &*atom }.borrow();
    dyn_space.borrow_mut().remove(atom)
}
```

### 4.3 Python：`SpaceRef.remove_atom`

```211:215:d:\dev\hyperon-experimental\python\hyperon\base.py
    def remove_atom(self, atom):
        """
        Delete the specified Atom from the Space.
        """
        return hp.space_remove(self.cspace, atom.catom)
```

---

## 5. `get-atoms`：`GetAtomsOp` → `space.borrow().visit(...)`

```124:148:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
impl CustomExecute for GetAtomsOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let arg_error = || ExecError::from("get-atoms expects one argument: space");
        let space = args.get(0).ok_or_else(arg_error)?;
        let space = Atom::as_gnd::<DynSpace>(space).ok_or("get-atoms expects a space as its argument")?;
        let mut result = Vec::new();
        space.borrow().visit(&mut |atom: std::borrow::Cow<Atom>| {
            result.push(make_variables_unique(atom.into_owned()))
        }).map_or(Err(ExecError::Runtime("Unsupported Operation. Can't traverse atoms in this space".to_string())), |_| Ok(result))
    }
}
```

要点：**遍历**依赖 `Space::visit`；失败表示该 `DynSpace` 后端未实现迭代（例如部分自定义空间）。

### 5.1 `GroundingSpace` 的 `visit`

```72:74:d:\dev\hyperon-experimental\lib\src\space\grounding\mod.rs
    fn visit(&self, v: &mut dyn SpaceVisitor) -> Result<(), ()> {
       Ok(self.index.iter().for_each(|atom| v.accept(atom)))
    }
```

（完整 `impl Space for GroundingSpace` 见同文件 62–78 行。）

### 5.2 C API：`space_iterate`

```237:243:d:\dev\hyperon-experimental\c\src\space.rs
#[no_mangle]
pub extern "C" fn space_iterate(space: *const space_t,
        callback: c_atom_callback_t, context: *mut c_void) -> bool {
    let dyn_space = unsafe{ &*space }.borrow();
    match dyn_space.borrow().visit(&mut |atom: Cow<Atom>| callback(atom.as_ref().into(), context)) {
        Ok(()) => true,
        Err(()) => false,
    }
}
```

### 5.3 Python：`get_atoms` 列表接口

```229:238:d:\dev\hyperon-experimental\python\hyperon\base.py
    def get_atoms(self):
        """
        Returns a list of all Atoms in the Space, or None if that is impossible.
        """
        res = hp.space_list(self.cspace)
        if res == None:
            return None
        result = []
        for r in res:
            result.append(Atom._from_catom(r))
        return result
```

---

## 6. `match`（指定空间）：`MatchOp`

### 6.1 Rust：`execute_bindings` 与 `query`

```140:166:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\core.rs
pub struct MatchOp {}

grounded_op!(MatchOp, "match");
// ...
impl CustomExecute for MatchOp {
    fn execute_bindings(&self, args: &[Atom]) -> Result<BoxedIter<'static, (Atom, Option<Bindings>)>, ExecError> {
        let arg_error = || ExecError::from("match expects three arguments: space, pattern and template");
        let space = args.get(0).ok_or_else(arg_error)?;
        let pattern = args.get(1).ok_or_else(arg_error)?;
        let template = args.get(2).ok_or_else(arg_error)?.clone();
        let space = Atom::as_gnd::<DynSpace>(space).ok_or("match expects a space as the first argument")?;
        let results = space.borrow().query(&pattern);
        let results = results.into_iter().map(move |b| (template.clone(), Some(b)));
        Ok(Box::new(results))
    }
}
```

**语义**：对 **第一个参数所指空间** 调用 `query(pattern)`，每个绑定集与 **template** 配对，供解释器做非确定性展开（`execute_bindings` 路径见 `eval_impl`，`interpreter.rs` 512–525 行附近）。

### 6.2 分词器注册

```341:342:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\core.rs
    let match_op = Atom::gnd(MatchOp{});
    tref.register_token(regex(r"match"), move |_| { match_op.clone() });
```

### 6.3 C API：`space_query`

```183:189:d:\dev\hyperon-experimental\c\src\space.rs
#[no_mangle]
pub extern "C" fn space_query(space: *const space_t, pattern: *const atom_ref_t) -> bindings_set_t
{
    let dyn_space = unsafe{ &*space }.borrow();
    let pattern = unsafe{ &*pattern }.borrow();
    let results = dyn_space.borrow().query(pattern);
    results.into()
}
```

### 6.4 Python：`SpaceRef.query`

```248:252:d:\dev\hyperon-experimental\python\hyperon\base.py
    def query(self, pattern):
        """
        Performs the specified query on the Space, and returns the result as a BindingsSet.
        """
        result = hp.space_query(self.cspace, pattern.catom)
        return BindingsSet(result)
```

`AbstractSpace.query` 为子类约定接口（`base.py` 14–19 行）。

---

## 7. `&self`：当前模块空间如何进入 MeTTa 程序

### 7.1 分词器注册（依赖捕获的 `DynSpace`）

```74:82:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\mod.rs
    let self_atom = Atom::gnd(space.clone());
    tref.register_token(regex(r"&self"), move |_| { self_atom.clone() });
```

注释说明 **`&self` 持有强引用** 带来的生命周期与释放问题（`mod.rs` 74–80 行）。

### 7.2 语义

解析到 token `&self` 时，直接产生 **grounded `DynSpace` 原子**，其内容与当前 `MettaMod` 的 space 同步（共享 `Rc` 语义，由 `DynSpace` 实现）。

### 7.3 与 `context-space` 的对比

| 机制 | 来源 | 行为 |
|------|------|------|
| `&self` | 分词器；`stdlib/mod.rs` 81–82 行 | 解析期替换为 **当前模块** 空间原子 |
| `context-space` | 解释器内建；`interpreter.rs` 954–964 | **求值期** 取解释器 `InterpreterContext` 中的 space |

二者在 **嵌套解释** / **capture** 场景下可能不同；编写跨模块代码时需谨慎。

---

## 8. 空间作为一等值：`DynSpace` grounded atom

### 8.1 Rust

`NewSpaceOp`、`MatchOp`、`AddAtomOp` 等均把 `DynSpace` 包进 `Atom::gnd(...)`。

### 8.2 C：`atom_gnd_for_space`

```304:315:d:\dev\hyperon-experimental\c\src\atom.rs
#[no_mangle]
pub extern "C" fn atom_gnd_for_space(space: *const space_t) -> atom_t {
    let space = unsafe { &*space }.borrow();
    Atom::gnd(space.clone()).into()
}
```

### 8.3 Python：`G()` 与 `cspace` 属性

```199:214:d:\dev\hyperon-experimental\python\hyperon\atoms.py
def G(object, type=AtomType.UNDEFINED):
    """A convenient method to construct a GroundedAtom"""
    return GroundedAtom(_priv_atom_gnd(object, type))

def _priv_atom_gnd(obj, type):
    // ...
    if hasattr(obj, "cspace"):
        assert type == AtomType.UNDEFINED, f"Grounded Space Atoms {obj} can't have a custom type {type}"
        catom = hp.atom_space(obj.cspace)
```

`GroundedAtom.get_object()` 对 `GROUNDED_SPACE` 类型返回 `SpaceRef`（`atoms.py` 179–184 行）。

---

## 9. 观察者模式：`SpaceEvent` / `SpaceObserver`（C 暴露）

### 9.1 事件枚举与 C 类型

```265:276:d:\dev\hyperon-experimental\c\src\space.rs
#[repr(C)]
pub enum space_event_type_t {
    SPACE_EVENT_TYPE_ADD,
    SPACE_EVENT_TYPE_REMOVE,
    SPACE_EVENT_TYPE_REPLACE,
}
```

```293:303:d:\dev\hyperon-experimental\c\src\space.rs
#[repr(C)]
pub struct space_event_t {
    /// Internal.  Should not be accessed directly
    event: *mut RustSpaceEvent,
}

struct RustSpaceEvent(SpaceEvent);
```

### 9.2 `space_event_get_type` / `space_event_get_field_atom`

```401:407:d:\dev\hyperon-experimental\c\src\space.rs
#[no_mangle]
pub extern "C" fn space_event_get_type(event: *const space_event_t) -> space_event_type_t {
    let event = unsafe{ &*event }.borrow();
    match event {
        SpaceEvent::Add(_) => space_event_type_t::SPACE_EVENT_TYPE_ADD,
        SpaceEvent::Remove(_) => space_event_type_t::SPACE_EVENT_TYPE_REMOVE,
        SpaceEvent::Replace(_, _) => space_event_type_t::SPACE_EVENT_TYPE_REPLACE,
    }
}
```

（字段访问：419–448 行。）

### 9.3 注册观察者

```463:469:d:\dev\hyperon-experimental\c\src\space.rs
#[no_mangle]
pub extern "C" fn space_register_observer(space: *mut space_t, observer_api: *const space_observer_api_t, observer_payload: *mut c_void) -> space_observer_t {
    let dyn_space = unsafe{ &*space }.borrow();
    let space = dyn_space.borrow_mut();
    let observer = CObserver {api: observer_api, payload: observer_payload};
    let observer = space.common().register_observer(observer);
    observer.into()
}
```

### 9.4 Rust 侧触发点（GroundingSpace）

`add` / `remove` / `replace` 已在第 3–4 节引用：`notify_all_observers` 传入 `SpaceEvent::Add` / `Remove` / `Replace`（`lib/src/space/grounding/mod.rs` 73、96、123 行）。

---

## 10. Python 自定义空间：`AbstractSpace` 与 FFI 回调

### 10.1 `AbstractSpace`

```6:36:d:\dev\hyperon-experimental\python\hyperon\base.py
class AbstractSpace:
    """
    A virtual base class upon which Spaces can be implemented in Python
    """
    def query(self, query_atom):
        raise RuntimeError("Space::query() is not implemented")
    def add(self, atom):
        raise RuntimeError("Space::add() is not implemented")
    def remove(self, atom):
        raise RuntimeError("Space::remove() is not implemented")
```

### 10.2 `SpaceRef` 包装 C 或自定义空间

```168:182:d:\dev\hyperon-experimental\python\hyperon\base.py
class SpaceRef:
    def __init__(self, space_obj):
        if type(space_obj) is hp.CSpace:
            self.cspace = space_obj
        else:
            self.cspace = hp.space_new_custom(space_obj)
```

### 10.3 私有胶水函数

`_priv_call_query_on_python_space`、`_priv_call_add_on_python_space`、`_priv_call_remove_on_python_space`（`base.py` 107–132 行）把 C 层回调转到 Python 方法。

---

## 11. `space_t` 句柄与 `DynSpace` 的对应

```24:45:d:\dev\hyperon-experimental\c\src\space.rs
#[repr(C)]
pub struct space_t{
    /// Internal.  Should not be accessed directly
    space: *const RustOpaqueSpace
}

struct RustOpaqueSpace(DynSpace);
// ...
impl space_t {
    pub(crate) fn into_inner(self) -> DynSpace {
        unsafe{ Box::from_raw(self.space.cast_mut()).0 }
    }
    pub(crate) fn borrow(&self) -> &DynSpace {
        unsafe{ &(&*self.space).0 }
    }
}
```

注释解释为何使用 `Box` 间接层（`dyn SpaceMut` 与 `Rc` 元数据，见 32–37 行）。

---

## 12. `atom.rs` 与空间相关的其它 C 入口

- **`atom_get_space`**：从 grounded space atom 取 `space_t`（`c/src/atom.rs` 508–522 行）。
- **`atom_match_atom`**：两原子匹配，与空间 **查询** 不同但共享 matcher（`c/src/atom.rs` 1061–1067 行）。

---

## 13. MeTTa 测试与示例索引

- **`add-atom` / `get-atoms` / `new-space`**：`space.rs` 模块测试 236–299 行。
- **`&self` 与类型**：`stdlib/mod.rs` 175–225 行附近大量 `!(metta ... &self)`。
- **`match` 算子单测**：`core.rs` `match_op`、`match_op_issue_530`（约 530–545 行）。

---

## 14. 数据流简图（文字版）

1. **MeTTa 源码** 中出现 `(add-atom $s $a)`。
2. **解析** 得到 `Expression`，首子为 grounded `AddAtomOp`。
3. **`eval_impl`** 走 `execute`：第一个参数转为 `DynSpace`，`borrow_mut().add`。
4. **`GroundingSpace::add`** 更新索引并 **`SpaceEvent::Add`**。
5. **Python** 若持有同一空间的 `SpaceRef`，可通过 `get_atoms` / `query` 观察变化；**C 观察者** 可通过 `space_register_observer` 订阅事件。

---

## 15. 与解释器 `query` 的关系（空间外 vs 空间内）

解释器对 **普通表达式** 的归约使用 **当前上下文空间** 的 `query`（`interpreter.rs` `query` 函数，604 行起），模式为 `(= <expr> $X)`。  
**`match` 算子** 则显式传入 **任意** `DynSpace`，用于模块化知识与多空间程序。

---

## 16. `get-type-space`（交叉引用）

读取某 atom 在 **指定空间** 的类型信息时使用 `GetTypeSpaceOp`（`lib/src/metta/runner/stdlib/atom.rs` 419–446 行）。与 `get-atoms` 同属“空间为参数”的 API 家族。

---

## 17. 性能与实现注释

- `GetAtomsOp` 对每个 atom 调用 `make_variables_unique`（`space.rs` 146 行），避免遍历结果中变量 ID 冲突。
- `space_query` 返回 `bindings_set_t`，调用方负责释放（C 文档注释 181 行）。

---

## 18. 小结表

| MeTTa/Rust 名 | Rust 结构 / 函数 | 主要文件：行号 |
|---------------|------------------|----------------|
| `new-space` | `NewSpaceOp::execute` | `space.rs` 27–35 |
| `add-atom` | `AddAtomOp::execute` | `space.rs` 167–175 |
| `remove-atom` | `RemoveAtomOp::execute` | `space.rs` 194–202 |
| `get-atoms` | `GetAtomsOp::execute` | `space.rs` 139–147 |
| `match` | `MatchOp::execute_bindings` | `core.rs` 155–165 |
| `&self` token | `register_all_corelib_tokens` | `stdlib/mod.rs` 81–82 |
| `space_add` 等 | C API | `c/src/space.rs` 140–189 |
| `atom_gnd_for_space` | C API | `c/src/atom.rs` 312–314 |
| `GroundingSpace::add` | 索引 + 事件 | `grounding/mod.rs` 70–73 |

---

## 19. 附录：`Replace` 事件与 `space_replace`

`GroundingSpace::replace`（`grounding/mod.rs` 119–125 行）发出 `SpaceEvent::Replace`。C API：

```170:174:d:\dev\hyperon-experimental\c\src\space.rs
#[no_mangle]
pub extern "C" fn space_replace(space: *mut space_t, from: *const atom_ref_t, to: atom_t) -> bool {
    let dyn_space = unsafe{ &*space }.borrow();
    let from = unsafe{ &*from }.borrow();
    dyn_space.borrow_mut().replace(from, to.into_inner())
}
```

Python：`SpaceRef.replace_atom`（`base.py` 217–221 行）。

---

## 20. 附录：`space_params_notify_all_observers`

自定义 C 空间实现若需广播事件，可调用：

```631:636:d:\dev\hyperon-experimental\c\src\space.rs
#[no_mangle]
pub extern "C" fn space_params_notify_all_observers(params: *const space_params_t, event: *const space_event_t) {
    let common = unsafe{ &(*params).common.common };
    let event = unsafe{ &*event }.borrow();
    common.notify_all_observers(event);
}
```

---

## 21. 实现者备忘（扩展阅读）

### 21.1 `CSpace` trait 对象

`c/src/space.rs` 中 `CSpace` 实现 `Space` / `SpaceMut`（约 699–801 行），通过函数表 `space_api_t` 调用 C 侧实现。

### 21.2 `space_subst`

`space_subst`（203–211 行）在模式替换场景使用，与 `match` 的 query-template workflow 相关但语义不同。

### 21.3 Python `GroundingSpace.atoms_iter`

`GroundingSpace.atoms_iter` 使用 `gspace.get_atoms()`（`base.py` 101–105 行），与 Rust `visit` 的流式迭代在性能特征上不同。

### 21.4 与文档 7 的交叉

`case` / `assertEqual` 等使用 `(chain (context-space) $space ...)` 获取求值空间；与 `match` 的 **显式空间参数** 形成对照。

### 21.5 变量与查询

`GroundingSpace::query` 实现见 `grounding/mod.rs` 128–44 行（`complex_query` / `single_query`）；`match` 直接复用该查询引擎。

### 21.6 空空间与 `get-atoms`

`GetAtomsOp` 测试期望空向量（`space.rs` 283–288 行）。

### 21.7 错误路径

`get-atoms` 对不支持 `visit` 的空间返回 `ExecError::Runtime`（`space.rs` 145–147 行）。

### 21.8 FFI 安全提示

`space_add` 取得 `atom` 所有权（`c/src/space.rs` 136–137 行注释）；Python 绑定需避免 double-free。

### 21.9 未来工作

`stdlib/mod.rs` 关于 `&self` 与弱引用的 TODO（74–80 行）仍可能影响长生命周期宿主嵌入场景。

### 21.10 术语

**SpaceType**：MeTTa 类型层对空间引用的抽象；运行时载体为 **`DynSpace` grounded atom**。

---

*文档结束。*
