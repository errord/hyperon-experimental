---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `lib/examples/custom_match.rs` 分析报告

## 文件角色

示例：实现 `TestDict` grounded 类型，自定义 `CustomMatch`（字典与字典之间按键值对做笛卡尔式 `match_atoms` 合并）。

## 关键 API

- `Grounded::as_match`、`match_atoms`、`BindingsSet::merge`、`expr!`

## 小结

演示如何用 Rust 扩展匹配语义而非仅相等比较；`main` 构造查询字典并打印 `match_atoms` 的绑定集合。
