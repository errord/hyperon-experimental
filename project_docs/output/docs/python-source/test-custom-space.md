---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_custom_space.py 分析报告

## 文件角色

通过实现 **`AbstractSpace` 子类 `CustomSpace`**，验证 `SpaceRef` 与 MeTTa 对自定义原子空间的集成（增删改查、嵌套空间、`match`）。

## 测试覆盖摘要

- CRUD：`add_atom`、`atom_count`、`get_atoms`、`remove_atom`、`replace_atom`。
- `query`：多匹配、`BindingsSet.push` 路径。
- 含空间的原子：`G(space)` 放入主空间后查询并得到子空间上的 `query`。
- `register_token` + `!(match nested ...)`；`MeTTa(space=...)` 与 `!(match &self ...)`。

## 关键断言/特性

- `get_payload()` 保留 Python 侧自定义属性。
- 查询 `(A $x)` 得到无序的 `{x: B}` 与 `{x: E}`。
- 递归：小空间内加入指向大空间的原子（注释级说明，测试侧重子空间查询）。

## 小结

文档化级注释说明 `query` 实现的朴素性；重点测 **SpaceRef 包装自定义后端** 与 MeTTa runner 协同。
