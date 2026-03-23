---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# f1_moduleB.metta

## 文件角色

`f1_imports.metta` 的**被导入模块 B**：同样依赖 C，但实现**另一份** `dup`，用于演示多模块导入时同名规则的非确定性。

## 原子分类

- **导入**：`import! &self f1_moduleC`。
- **函数**：`dup`（与 moduleA 不同分支结构）。

## 关键运算/函数

`(= (dup $x) (if (== $x 0) (g $x) (+ $x 10)))`。

## 演示的 MeTTa 特性

- 与 moduleA **共享** `g`（经 C），但 `dup` 定义不同 → `dup 2` 多结果 `(12 102)`。
- 钻石依赖下核心依赖去重，`dup` 仍冲突。

## 教学价值

直观展示“模块合并到 `&self`”时**同名等式集合并**的语义后果。

## 概要

极短文件：仅 import C 与一条 `dup`，专用于与 A 对比。
