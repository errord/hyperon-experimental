---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 模块 `hyperon.runner` — 公共 API

**MeTTa** 运行器、单步状态、**RunContext** 与环境构建。

## `MeTTa`

### 构造

- `MeTTa(cmetta=None, space=None, env_builder=None)`  
  默认创建 **GroundingSpaceRef**、带默认配置目录的 **EnvBuilder**，注册 **Python 文件模块格式**、内置 `hyperon/exts` 与 **site-packages** 的 **include** 路径，并用 **stdlib** 加载器初始化。

### 属性与方法

- `space() -> GroundingSpaceRef`：顶层模块空间。
- `tokenizer() -> Tokenizer`
- `working_dir() -> str`
- `register_token(regex, constr)`, `register_atom(name, symbol)`
- `parse_all(program) -> list[Atom]`, `parse_single(program) -> Atom`
- `run(program, flat=False)`：执行 **MeTTa** 源码；`flat=True` 时结果打平为一维 **Atom** 列表。
- `evaluate_atom(atom) -> list[Atom]`
- `load_module_direct_from_func(mod_name, loader_func) -> ModuleId`
- `load_module_direct_from_pymod(mod_name, pymod_name)`
- `load_module_at_path(path, mod_name=None)`
- `__eq__`：同底层 **cmetta** 则相等。

错误时抛 `RuntimeError`（引擎错误字符串）。

## `RunnerState`

用于单步执行与调试：

- `__init__(metta, program)`
- `run_step()`：前进一步；错误抛 `RuntimeError`。
- `is_complete() -> bool`
- `current_results(flat=False)`：当前中间结果。

## `RunContext`

模块加载器回调中使用：

- `init_self_module(space, resource_dir)`：在加载器内必须恰好调用一次。
- `metta() -> MeTTa`, `space() -> GroundingSpaceRef`, `tokenizer() -> Tokenizer`
- `load_module(mod_name)`
- `register_token`, `register_atom`（当前模块）
- `import_dependency(mod_id)`

## `ModuleDescriptor`

包装核心模块描述符（版本化元数据预留）。

## `Environment`

静态方法配置宿主环境：

- `config_dir()`
- `init_common_env(working_dir=..., config_dir=..., create_config=..., is_test=..., include_paths=[])`
- `test_env()`：**EnvBuilder**，适合单元测试。
- `custom_env(...)`：可共存多环境的构建器。

## 内部加载（了解即可）

- `_PyFileMeTTaModFmt`：从 `.py` 或 `__init__.py` 目录加载 **MeTTa** 模块。
- `_priv_load_module_stdlib`：加载 `hyperon.stdlib`。

扩展作者通常通过 `register_atoms` / `register_tokens` 在 Python 模块中导出注册函数，而非直接调用上述私有符号。
