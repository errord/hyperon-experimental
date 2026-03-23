---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `lib/benches/grounding_space.rs` 分析报告

## 文件角色

`GroundingSpace::query` 性能：在空间中批量加入 `=` 规则后，对单条模式做查询。

## 关键 API

- `query_x10` / `query_x100`：`Bencher`、`bind_set!`、`expr!`

## 小结

空间规模 10 vs 100 对比同构查询开销；需 nightly `test` crate。
