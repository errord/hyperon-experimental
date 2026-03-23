---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 模块 `hyperon.base` — 公共 API

**Space**、**Tokenizer**、**SExprParser** 及底层解释器薄封装。

## 抽象空间

### `AbstractSpace`

子类需实现：

- `query(query_atom) -> BindingsSet`
- `add(atom)`, `remove(atom)`, `replace(atom, replacement)`

可选：`atom_count()`, `atoms_iter()`。

### `GroundingSpace(AbstractSpace)`

委托给 `GroundingSpaceRef`（原生 **GroundingSpace**）。

## `SpaceRef`

- `__init__(space_obj)`：`CSpace` 或任意 Python **Space**（经 `space_new_custom`）。
- `add_atom`, `remove_atom`, `replace_atom`, `atom_count`, `get_atoms`, `get_payload`
- `query(pattern) -> BindingsSet`
- `subst(pattern, templ) -> list[Atom]`
- `copy()`

### `GroundingSpaceRef(SpaceRef)`

- `__init__(cspace=None)`：默认新建原生空间。
- `_from_cspace(cspace)`

## `Tokenizer`

- `register_token(regex, constr)`：**regex** 为 **Rust regex** 语法字符串；`constr` 接收匹配文本返回 **Atom**。

## `SExprParser`

- `__init__(text)`
- `parse(tokenizer) -> Atom | None`：失败抛 `SyntaxError`（带引擎消息）。
- `parse_to_syntax_tree() -> SyntaxNode | None`

## `SyntaxNode`

- `get_type()`, `src_range()`, `unroll()`

## `Interpreter`（低级 API）

面向单表达式逐步解释：

- `__init__(gnd_space, expr)`
- `has_next()`, `next()`, `get_result()`, `get_step_result()`

### `interpret(gnd_space, expr) -> list[Atom]`

跑完整个计划并返回结果列表。

## 类型辅助

- `check_type(gnd_space, atom, type) -> bool`
- `validate_atom(gnd_space, atom) -> bool`
- `get_atom_types(gnd_space, atom) -> list[Atom]`
- `atom_is_error(atom) -> bool`

## 私有胶水（非公共 API）

`_priv_call_*_on_python_space` 仅供 **hyperonpy** 调用自定义 **Space**；扩展作者实现 `AbstractSpace` 即可，无需直接调用。
