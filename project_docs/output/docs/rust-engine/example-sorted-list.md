---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `lib/examples/sorted_list.rs` 分析报告

## 文件角色

示例：在 MeTTa 中声明代数数据类型 `List` 与插入排序式 `insert`，并用 Rust 断言运行结果结构。

## 关键 API

- `Metta::new(None)`、`SExprParser`、`expr!` + `Number::Integer`

## 小结

展示最小函数式列表 API 与 `!(insert ...)` 求值；无额外宿主 grounded 代码。
