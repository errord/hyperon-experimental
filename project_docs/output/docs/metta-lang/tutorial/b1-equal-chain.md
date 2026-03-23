---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# b1_equal_chain.metta

## 文件角色

解释 **`=` 与解释器求值模型**：求值即反复构造 `(match &self (= (expr) $r) $r)`，并对比 `assertEqual` 与 `assertEqualToResult`。

## 原子分类

- **等式规则**：`(= (I $x) $x)` 等 SKI、`Add`。
- **测试**：`assertEqual`、`assertEqualToResult`。

## 关键运算/函数

内建对 `=` 的解释；子表达式先归约的行为示例；`eq` 非全函数示例。

## 演示的 MeTTa 特性

- 任意表达式求值与**空匹配则结果为自身**的语义。
- `assertEqual` 比较两式**求值结果集**；`assertEqualToResult` 更安全。
- 左部可重复使用同一变量；规则可非全定义。

## 教学价值

把 b0 的手动链式 `match` 与**语言内建归约**对齐，是后续推理与类型的核心前提。

## 概要

用 SKI 与 Peano 加法说明 `=` 驱动的归约，并演示子项归约、无规则时保持原式、以及 `eq` 仅在参数语法相同时为真。
