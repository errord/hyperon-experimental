---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# d1_gadt.metta

## 文件角色

Jetta 空间中的 **高阶函数与 λ**：字符串定义 `foo`/`bar`/`goo`，并在宿主侧 `compile` 生成 `-gnd` 调用。

## 原子分类

- **Jetta 文本**：含 `\\`/`\` λ 语法与高阶类型 `->`。
- **宿主侧类型与规则**：`foo-f`、`bar-lamb` 与 `compile`。

## 关键运算/函数

`jetta`、`compile`、`foo-f-gnd`、`bar-lamb-gnd` 等接地入口。

## 演示的 MeTTa 特性

- Jetta 内传递**函数值**（符号或 λ）。
- `compile` 将命名函数暴露为宿主可调用接地形式。
- 文件末尾 TODO：Jetta 内非确定性 `doo` 多子句。

## 教学价值

衔接“宿主 MeTTa 编排”与“Jetta 内富类型函数式子语言”。

## 概要

验证 `(foo 2 3 goo)`、内联 λ、`bar` 嵌套闭包数值，以及宿主 `-gnd` 与 Jetta 一致。
