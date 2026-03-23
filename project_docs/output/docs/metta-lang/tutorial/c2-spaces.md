---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# c2_spaces.metta

## 文件角色

用 BHV 模拟**键值绑定与叠加存储**：多对 `bhv-bind` 经 `bhv-majority` 合成“字典”，再按 key 取回近似 value。

## 原子分类

- **向量槽**：`&v1`…`&k3`。
- **复合**：`dict`、`v1_retrived`（原文拼写）。

## 关键运算/函数

`bhv-bind`、`bhv-majority`、`bhv-std-apart-relative`、`bhv-is-related`。

## 演示的 MeTTa 特性

- 超向量空间上的**分布式绑定**与叠加。
- 用 `bhv-is-related` 做**内容检索/一致性**断言。

## 教学价值

把“空间”直觉从 Atom 空间扩展到**向量叠加知识表示**，与符号 `&self` 形成类比。

## 概要

三对 key-value 绑定叠加为 `dict`，从 `dict` 用 `&k1` 解绑得到与 `&v1` 统计相关的向量。
