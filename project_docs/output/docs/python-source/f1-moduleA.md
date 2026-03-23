---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# f1_moduleA.metta

## 文件角色

`f1_imports.metta` 的**被导入模块 A**：先拉取 C，再定义 `dup` 与带类型的 `f`，用于检验跨模块依赖与 `g` 的间接使用。

## 原子分类

- **导入**：`import! &self f1_moduleC`。
- **函数**：`dup`、`f`；内建 `+`、`if`、`<` 等。

## 关键运算/函数

`(= (dup $x) (if (== $x 0) (+ $x 10) (g $x)))`；`(: f (-> Number Number))` 与 `(= (f $x) ...)`。

## 演示的 MeTTa 特性

- 模块链 **A → C**（`g` 来自 C）。
- `f` 显式类型注解，与测试主脚本中的求值断言衔接。

## 教学价值

作为**最小可组合模块**示例，配合钻石依赖中的 `dup` 歧义对比 B。

## 概要

断言基础内建可用后，定义依赖 `g` 的 `dup` 与分段函数 `f`。
