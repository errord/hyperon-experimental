---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_atom.py 分析报告

## 文件角色

Hyperon Python 绑定中**原子（Atom）与解释**的核心单元测试：符号、变量、接地值、表达式、`GroundingSpaceRef` 相等性，以及 `interpret` 与自定义 `MatchableObject` 的匹配行为。

## 测试覆盖摘要

- **S / V / ValueAtom / E**：相等、`str`、`get_metatype`、`get_name`、UTF-8 符号名。
- **G(GroundedObject)**：`get_grounded_type`；未实现 `copy` 的接地对象在构造时触发断言。
- **`OperationAtom` 与 `interpret`**：`execute` 返回、`unwrap=False` 若返回 Python 原生值则报错、`NoReduceError` / `IncorrectArgumentError`、`atom_is_error`。
- **空间**：两空间内容相同但对象不同则 `!=`；`MatchableAtomTest` 对 `query` 做模式匹配。

## 关键断言/特性

- `ValueAtom(1.0)` 与 `G(..., S("Float"))` 的接地类型与元类型。
- `unwrap=False` 的操作必须返回原子，否则得到 `Error` 形态。
- `GroundingSpaceRef` 的 `__eq__`：同一引用相等，不同实例即使原子列表相同仍不相等。
- `interpret` 包装 `Atoms.METTA` + `G(space)` 的归约路径。

## 小结

验证原子 ADT 的 Python 封装与解释器对接地操作、错误与“不可归约”语义的契约；并包含可匹配原子的最小自定义实现示例。
