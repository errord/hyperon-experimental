---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_grounded_type.py 分析报告

## 文件角色

**接地类型系统与高阶/多态操作**：内置运算结果的 `get_grounded_type`、`OperationAtom` 签名、`unwrap=False`、Python 与 Rust 接地值互操作及空间匹配一致性。

## 测试覆盖摘要

- 算术、比较、布尔与 `Number`/`Bool` 等同类型关系；`untop` 返回单元。
- 高阶：`curry_num` 返回带类型的 `OperationAtom`。
- `repr`：Python 与 Rust 对转义字符的字符串表示差异。
- `id_num` / `id_atom` / `id_poly_*` / `id_undef`：类型错误、`BadArgType`、未归约表达式。
- 双向：`python-*-func` 与 Rust 原语混用；`match-*` 规则与 Python 产生值匹配。
- `ValueAtom(42, "Int")` 等对原生 int/float/bool **禁止自定义接地类型**（AssertionError 消息前缀）。

## 关键断言/特性

- `@unittest.skip` 的 `test_undefined_operation_type` 标记未来行为。
- `import hyperonpy as hp` 未在断言中深度使用（可视为预留）。

## 小结

集中覆盖 **跨语言接地值的类型与相等/匹配**，并记录 Python 侧多态 `unwrap` 的限制（TODO 注释）。
