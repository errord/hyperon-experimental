---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# b4_nondeterm.metta

## 文件角色

**非确定性**求值与匹配教程：`superpose`、`collapse`、`let`，以及组合爆炸与过滤。

## 原子分类

- **多子句 `=`**：`(= (color) green)` 等产生多结果。
- **辅助**：`superpose`、`collapse`、`let`、`match`。

## 关键运算/函数

`superpose`、`collapse`、`let`；多结果 `=` 与 `pair (bin) (bin)` 组合。

## 演示的 MeTTa 特性

- 等式查询与解释器均可返回**多结果集**；顺序不保证时用 `superpose` 比较。
- `collapse` 将非确定性结果收束为表达式（含空归约时的行为）。
- 子表达式均非确定性时**笛卡尔式组合**；部分分支无规则时保留未归约形式。
- `find-equal` 示例：用 `match` 过滤不可归约组合。

## 教学价值

理解 MeTTa 的**集合式语义**，避免将解释器仅当作单值函数。

## 概要

从 `color` 多解到 `let`+`collapse` 与 `superpose` 互逆，再到 `is (air dry)` 类资源分配非确定性故事。
