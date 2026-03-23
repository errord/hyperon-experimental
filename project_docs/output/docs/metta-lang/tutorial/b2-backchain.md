---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# b2_backchain.metta

## 文件角色

**反向链/说明性推理**教程：`match` 嵌在 `=` 右侧，实现 `deduce` 与 `explain`；含 PLN 风格的 `Implication` 与 `And`。

## 原子分类

- **事实**：`Frog Sam`、`Evaluation (...)`。
- **规则**：`Implication`、`And`；自定义 `deduce`、`explain`、`ift`。
- **查询**：内层 `match &self`。

## 关键运算/函数

`deduce`、`explain`、`ift`、`match` 与递归式 `=` 定义。

## 演示的 MeTTa 特性

- 用 `=` 定义“可计算谓词”，其体为 `match` 对知识库的查询。
- 多子句 `=` 实现**分情形**与递归（与 `match` 多结果结合）。
- `frog` 示例区分**声明**与**可求值**表达式。

## 教学价值

展示 MeTTa 如何用少量原语拼装**定理证明器式**控制流，衔接 OpenCog/PLN 叙事。

## 概要

从 `frog` 简单查询到 Plato 是否 mortal 的递归反向链，再到 `explain` 生成证明树结构。
