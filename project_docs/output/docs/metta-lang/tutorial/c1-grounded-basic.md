---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# c1_grounded_basic.metta

## 文件角色

BHV 扩展的**基础变换**：`bhv-new-perm`、`bhv-apply-perm` 与“置换后是否仍相关”的检验。

## 原子分类

- **导入**：`bhv_binding`。
- **绑定**：`&a`、`&b`、`&perm1`、`ab`。
- **接地**：`bhv-new`、`bhv-new-perm`、`bhv-apply-perm`、`bhv-majority`、`bhv-is-related`。

## 关键运算/函数

`bhv-apply-perm`、`bhv-is-related`；规则 `(= (perm1 $x) (bhv-apply-perm &perm1 $x))`。

## 演示的 MeTTa 特性

- 用 `=` 把符号算子映射到接地置换调用。
- 多数表决向量在置换下**整体一致变换**才保持相关。

## 教学价值

展示符号层与向量原语的**薄封装**模式，便于测试 BHV 语义。

## 概要

`perm1` 仅作用于 `&a` 而不作用于 `ab` 时相关检测为假；对两者同置换后为真。
