---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# b0_chaining_prelim.metta

## 文件角色

**链式匹配**入门：用自定义 `:=` 规则模拟组合子归约与 Peano 加法，展示“多步归约 = 嵌套 `match`”。

## 原子分类

- **自定义归约关系**：`:=` 与 SKI、`Add` 规则。
- **变量**：`$x`、`$y`、`$z`、`$r`、`$r2`。

## 关键运算/函数

嵌套 `match &self (:= ...) ...`；`assertEqualToResult`。

## 演示的 MeTTa 特性

- 单步 `match` 与**手动把上一步结果作为下一步输入**。
- 将两步写在**一个**外层 `match` 的内层 `match` 中，形成链式查询。

## 教学价值

在引入解释器对 `=` 的特殊处理之前，先建立“等式查询即匹配”的直观。

## 概要

SK 组合子 `(S K K x)` 两步归约到 `x`，以及 `Add (S Z) (S Z)` 两步到 `S (S Z)`，说明链式 `match` 如何模拟求值。
