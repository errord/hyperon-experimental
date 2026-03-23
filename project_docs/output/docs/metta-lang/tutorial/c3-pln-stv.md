---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# c3_pln_stv.metta

## 文件角色

（文件名含 pln/stv，内容为 **Jetta** 编译执行演示。）测试 `compile` 模块：在独立 Jetta 空间中执行字符串/原子 MeTTa 代码、错误处理与递归。

## 原子分类

- **导入**：`import! &self compile`。
- **空间绑定**：`&jspace`（`new-jetta-space`）。
- **接地**：`jetta`、`new-jetta-space`、`case`、`py-dot` 等。

## 关键运算/函数

`jetta`、`assertEqual`、`assertEqualToResult`、`case` 解析 `JettaCompileError`。

## 演示的 MeTTa 特性

- 宿主 MeTTa 中**嵌套另一求值空间**（Jetta）。
- 字符串传入类型定义与 `=` 规则；多次调用同一空间。
- Atom 传入时**未在 Jetta 文本中定义**的符号可能不在此路径归约（注释中的 FIXME）。
- HTTP 500 类错误与符号解析错误的测试手法。

## 教学价值

展示 Hyperon 与 **Jetta 后端**集成及跨空间求值的边界情况。

## 概要

覆盖 `foo` 定义、递归 `log-int`/`fact`、错误 case，以及 TODO 中指出的多段代码与类型推断限制。
