---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 模块 `hyperon.atoms` — 公共 API

表示 **Atom**、**Bindings**、**Grounded** 对象及可执行操作包装。通常通过 `from hyperon import ...` 使用（根包重导出部分符号）。

## 类

### `Atom`

- `__init__(catom)`：包装原生 **CAtom**（一般用户用工厂函数）。
- `get_metatype()`：**Atom** 元类型（**Symbol** / **Variable** / **Expression** / **Grounded**）。
- `iterate()`：深度优先遍历子树。
- `match_atom(b) -> BindingsSet`：与另一 **Atom** 匹配。
- `_from_catom(catom)`：由 **C** 句柄构造正确子类。

### `SymbolAtom(Atom)`

- `get_name() -> str`

### `VariableAtom(Atom)`

- `get_name() -> str`
- `parse_name(name) -> VariableAtom`：由 `get_name()` 结果解析。

### `ExpressionAtom(Atom)`

- `get_children() -> list[Atom]`

### `GroundedAtom(Atom)`

- `get_object()`：取出 Python 侧对象（**Space**、**ValueObject** 等）；失败可能 `TypeError`。
- `get_grounded_type() -> Atom`

### `AtomType`

常量：`UNDEFINED`, `TYPE`, `ATOM`, `SYMBOL`, `VARIABLE`, `EXPRESSION`, `GROUNDED`, `GROUNDED_SPACE`, `UNIT`, `NUMBER`, `BOOL`, `STRING`。

### `Atoms`

常量：`EMPTY`, `UNIT`, `METTA`。

### `GroundedObject` / `ValueObject` / `MatchableObject`

- **GroundedObject**：`content`, `id`, `copy()`。
- **ValueObject**：值相等、`serialize(serializer)` 用于跨运行时。
- **MatchableObject**：子类实现 `match_(atom)`。

### `OperationObject(GroundedObject)`

- `name`, `op`, `unwrap`
- `execute(*atoms, res_typ=AtomType.UNDEFINED)`：执行 **Grounded** 操作；`unwrap=True` 时从 **GroundedAtom** 解包 Python 值。

### `Bindings`

- `clone()`, `merge(other) -> BindingsSet`
- `add_var_binding(var, atom) -> bool`
- `is_empty()`, `resolve(var) -> Atom | None`, `iterator()`
- `narrow_vars(vars)`：保留指定变量绑定。

### `BindingsSet`

- `empty()`：空集（无匹配）。
- `clone()`, `push(bindings)`, `merge_into(...)`
- `add_var_binding`, `add_var_equality`
- `is_empty()`, `is_single()`, `iterator()`, `__getitem__`

### `Serializer`（基类，定义于 **hyperonpy**）

与 `SerialResult` 配合；子类见 `hyperon.conversion.ConvertingSerializer`。

## 工厂与函数

| 符号 | 说明 |
|------|------|
| `S(name)` | **SymbolAtom** |
| `V(name)` | **VariableAtom** |
| `E(*args)` | **ExpressionAtom** |
| `G(object, type=AtomType.UNDEFINED)` | **GroundedAtom** |
| `OperationAtom(name, op, type_names=None, unwrap=True)` | 包装可调用为操作 |
| `ValueAtom(value, type_name=None, atom_id=None)` | 值 **Grounded** |
| `PrimitiveAtom(...)` | 强制 Python 原始值不自动桥接到 **MeTTa** 原语 |
| `MatchableAtom(...)` | 可匹配值 |
| `atoms_are_equivalent(a, b) -> bool` | 结构等价 |
| `unwrap_args(atoms)` | 内部用于参数解包 |
| `get_string_value(value) -> str` | 字符串规范化 |

## 异常

- `NoReduceError`：无法归约。
- `IncorrectArgumentError`：参数类型/格式不符。
- `MettaError`：映射为 **MeTTa** `Error` 表达式而非 Python 栈。

## 说明

对 `get_object()` 的调用若在 **Space** **query** 回调中抛出未捕获异常，可能导致 **Rust** **panic**；建议在扩展中自行 **try/except**。
