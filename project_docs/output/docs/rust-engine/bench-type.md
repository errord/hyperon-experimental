---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `lib/benches/type.rs` 分析报告

## 文件角色

对 `get_atom_types` 在「较深表达式 + 简单类型空间」场景下的调用计时。

## 关键 API

- `metta_space` 解析 `(: b B) (: b BB)`；`atom_with_depth` 二叉展开；`get_atom_types`、`AtomType::is_error`

## 小结

单基准 `bench_get_atom_types_complex`；聚焦类型推导/查询在复杂结构上的成本。
