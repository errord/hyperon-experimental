---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# f1_imports.metta

## 文件角色

**模块导入综合测试**：`import!` 到独立空间与 `&self`、跨空间 `match` 调用、`dup` 非确定性、钻石依赖去重与重复导入幂等。

## 原子分类

- **模块空间**：`&m`、`f1_moduleA`、`f1_moduleB`、`f1_moduleC`。
- **辅助谓词**：`contains`、`is-space`（`car-atom`、`cdr-atom`、`get-type`）。

## 关键运算/函数

`import!`、`get-atoms`、`collapse`、`match`、`import! &self` 链。

## 演示的 MeTTa 特性

- 仅 `import! &m` 时**不能**像普通函数那样在 `&self` 求值 `&m` 中函数——需 `match` 或 `interpret`（注释）。
- 同一模块导入 `&self` 后 `f`/`g` 可直接求值。
- 钻石依赖下 `g`、`f` 确定；不同模块各定义 `dup` 则 `dup 2` **多解**。
- 重复 `import!` 应忽略，结果不变。

## 教学价值

理解 Hyperon **模块=空间依赖图**与 Python/no-Python 模式差异（文首注释）。

## 概要

从空 `get-atoms` 类型检查开始，走到多模块导入与 `dup` 非确定性，并记录 TODO（`get-deps` 等）。
