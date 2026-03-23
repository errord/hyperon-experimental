---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# a1_symbols.metta

## 文件角色

Python 测试套件中的入门教程脚本：用纯符号知识库演示 `match` 与断言，不涉及接地运算或模块。

## 原子分类

- **符号/表达式**：`leaf*`、`Sam`、`:=`、`isa` 等自定义关系与事实。
- **变量**：`$x`、`$who`、`$color`、`$tv` 等模式变量。
- **空间引用**：`&self`（当前工作空间）。
- **测试原语**：`assertEqualToResult`。

## 关键运算/函数

`match`、`assertEqualToResult`；自定义关系 `:=`、`isa`、`implies` 风格示例。

## 演示的 MeTTa 特性

- `match` 只在**顶层**匹配，不深入子表达式。
- 多变量绑定、将查询结果重组为输出模式。
- 用 `:=` 等自定义符号做“类似求值”的查询。

## 教学价值

建立“空间 + 模式匹配 + 多结果集合”的心智模型，为后续 `=` 求值与推理链打基础。

## 概要

通过叶子结构与自然语言式三元组展示 `match` 的行为边界与变量绑定，并用 `assertEqualToResult` 固定期望结果集。
