---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# a2_opencoggy.metta

## 文件角色

演示 **BHV（二进制超向量）** 绑定扩展：创建向量、多数表决组合、相似度检测；属接地扩展教程而非纯符号匹配。

## 原子分类

- **模块导入**：`import! &self bhv_binding`。
- **绑定与状态**：`bind!`、`&a`、`&b`、`&abc` 等 token。
- **接地运算**：`bhv-new`、`bhv-majority`、`bhv-std-apart-relative`、`bhv-is-related`。

## 关键运算/函数

`bhv-new`、`bhv-majority`、`bhv-std-apart-relative`、`bhv-is-related`。

## 演示的 MeTTa 特性

- 通过 `import!` 加载 Python/扩展提供的接地库。
- 用 `bind!` 持有可复用的接地原子（超向量句柄）。
- 向量叠加与“是否相关”的语义检索式用法。

## 教学价值

展示 MeTTa 如何编排**外部数值/向量原语**，与符号推理脚本形成对照。

## 概要

构造三个 BHV 及其多数表决复合体，并断言 `&a` 与复合体在统计意义上可分且相关，体现超向量空间上的绑定与检索。
