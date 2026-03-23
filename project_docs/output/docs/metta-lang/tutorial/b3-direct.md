---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# b3_direct.metta

## 文件角色

**前向风格**规则示例（无显式 backward chaining）：用 `=` 定义 `frog`/`green`，说明推理与函数式编程的交集。

## 原子分类

- **事实规则**：`(= (croaks Fritz) T)` 等。
- **组合规则**：`And`、`frog`、`green`、`ift`。

## 关键运算/函数

`assertEqual`、`assertEqualToResult`；在 `match` 中查询 `(= ($p Fritz) T)`。

## 演示的 MeTTa 特性

- 多层 `=` 定义推出结论 `green Fritz`。
- `ift` + 变量：从条件为真反求绑定 `$x`（`Fritz`）。
- 构造 `($x (green $x))` 同时展示**变量与求值结果**。
- `match` 对含 `=` 的式子与纯符号式行为差异的注释。

## 教学价值

与 b2 对照：同一类知识可用**更直接的函数式规则**表达，减少显式 `deduce`。

## 概要

Fritz 为例演示规则组合、`ift` 反查，以及用 `match` 枚举使 `(= ($p Fritz) T)` 成立的前件谓词。
