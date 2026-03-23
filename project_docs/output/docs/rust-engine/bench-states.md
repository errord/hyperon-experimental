---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `lib/benches/states.rs` 分析报告

## 文件角色

对比 MeTTa 中「`new-state` 存值」与「直接存原子」两种实现在查询与更新上的耗时（注释说明 grounded state 可能未索引）。

## 关键 API

- `Metta::run` 动态生成 `new-entry!`；`query_state_*`、`change_state_*`、`query_atom_*`、`change_atom_*`（10/50）

## 小结

用于跟踪未来对 State 包装与 `remove/add` 路径优化后的性能变化；含较多重复 MeTTa 字符串构造。
