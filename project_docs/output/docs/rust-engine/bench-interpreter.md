---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `lib/benches/interpreter_minimal.rs` 分析报告

## 文件角色

解释器 `interpret` 在深度嵌套 `CHAIN` 表达式上的步进成本（10 / 100 / 1000）。

## 关键 API

- `interpret(space, &atom)`、`CHAIN_SYMBOL`、`DynSpace` + `GroundingSpace`

## 小结

构造链式归约至 `A`，衡量解释器随链长扩展的耗时；每次迭代克隆 `DynSpace`。
