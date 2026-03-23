---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# g1_docs.metta

## 文件角色

**文档内省 API**：`@doc` 注解、`get-doc` 形式化结构、`help!` 人类可读输出与缺文档行为。

## 原子分类

- **文档表达式**：`@doc`、`@desc`、`@params`、`@return`。
- **类型**：`some-func`、`SomeSymbol` 等。
- **接地占位**：`some-gnd-atom`（未真导入故类型 `%Undefined%`）。

## 关键运算/函数

`@doc`、`get-doc`、`help!`、`assertEqual`。

## 演示的 MeTTa 特性

- 函数需 `: ` 类型才能形成完整 `@doc-formal`。
- `get-doc` 对未文档原子返回 `Empty`；对函数应用返回 `Empty`。
- `help!` 副作用：打印格式化帮助（示例输出在注释中）。

## 教学价值

支持 REPL/工具链的**自描述**与可教性，衔接库作者工作流。

## 概要

覆盖函数、符号原子、接地占位符与缺失文档四种 `get-doc`/`help!` 行为。
