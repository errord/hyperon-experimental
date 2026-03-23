---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_atom_type.py 分析报告

## 文件角色

针对**空间中声明的类型**与 MeTTa 类型检查 API 的单元测试：`check_type`、`validate_atom`、`get_atom_types`。

## 测试覆盖摘要

在 `GroundingSpaceRef` 中加入 `(: a A)`、`(: b B)`、`(: foo (-> A B))` 等事实，覆盖单符号类型、函数应用类型推导及错误情况。

## 关键断言/特性

- `check_type(space, S("a"), UNDEFINED)` 为真；与声明一致为真，与 `B` 为假。
- `validate_atom` 对 `(foo a)` 为真。
- `get_atom_types`：`(foo a)` → `[B]`；`(foo b)` → `[]`；`foo` 本身得到箭头类型。

## 小结

用最小类型环境验证 Python 暴露的类型查询/校验与空间中的 `:` 事实一致。
