---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# c2_spaces_kb.metta

## 文件角色

BHV **结构化记录**示例：为国家实体绑定 name/capital/money 槽，再做跨记录 `bhv-bind` 与属性查询。

## 原子分类

- **实体槽**：`&united_states`、`&washington_dc`、`&dollar` 等。
- **记录**：`USA`、`MEX`、`Pair`、`dollar_of_mexico`。

## 关键运算/函数

`bhv-majority`、`bhv-bind`、`bhv-is-related`。

## 演示的 MeTTa 特性

- 多条属性绑定合成单一**记录向量**。
- `Pair` 连接两国记录后，从“美国的 money 槽”经 Pair 上下文**关联到墨西哥货币**（peso）的演示意图。

## 教学价值

说明超向量可用于**类比推理/槽填充**类任务，不仅是数值玩具。

## 概要

验证 `(bhv-bind USA &money)` 与 `&dollar` 相关，以及 `dollar_of_mexico` 与 `&peso` 相关。
