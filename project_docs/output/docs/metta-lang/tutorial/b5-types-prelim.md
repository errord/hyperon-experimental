---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# b5_types_prelim.metta

## 文件角色

**类型系统入门**：`:` 标注、`->`、参数化 `List`、`BadArgType` 错误、`Atom` 元类型与 `match`/`let` 交互。

## 原子分类

- **类型断言**：`(: Z Nat)`、`(: List (-> Type Type))` 等。
- **等式**：Peano `Add`、`eq`、`eqa`。
- **错误值**：`Error ... BadArgType`。

## 关键运算/函数

`get-type`、`match`、`let`、`let*`；`eq` vs `eqa`（是否归约参数）。

## 演示的 MeTTa 特性

- 无类型时 `%Undefined%` 与逐步类型检查的对比。
- 运行时类型错误表达式形态。
- **非确定性类型**（`Ten` 多注解）。
- `Atom` 类型：**不向子式下传归约**（`match` 参数）；`match` 结果可继续归约。
- `let` 第二参数求值、第三参数按 Atom 处理；模式解构与 `let*`。

## 教学价值

连接“归约语义”与“类型守卫”，为 d 系列类型即命题与自动检查铺垫。

## 概要

从 `Add S Z` 报错到 `Cons` 异构列表错误，再到 `match`+`Atom` 与 `let*` 链式示例。
