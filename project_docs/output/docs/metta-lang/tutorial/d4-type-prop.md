---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# d4_type_prop.metta

## 文件角色

**类型即命题**的探索：`get-type`、依赖风格类型 `(Human $t)`、证明项与 `=` 的交互；含当前语言限制说明（无量词证明、Refl 语法等）。

## 原子分类

- **实体/谓词**：`Entity`、`Human`、`Mortal`、`HumansAreMortal`。
- **证明项**：`SocratesIsHuman`、`PlatoIsHuman` 等。
- **元**：`get-type`、`=`、`ift`、`match`。

## 关键运算/函数

`get-type`；自定义 `(= (= $x $x) T)` 与把 `(= $type T)` 链接到知识库中 `:` 条目的规则。

## 演示的 MeTTa 特性

- 命题类型与项的 `get-type` 行为。
- 错误证明/错误等式的类型查询**空结果**。
- 用 `match` 扩展 “`$type` 为真” 的推理时需注意与通用 `(: return (-> $t $t))` **无限循环**风险（文内注释）。
- `ift` 非确定性枚举满足 `(Mortal $x)` 的实体。

## 教学价值

揭示 MeTTa 类型层与逻辑层的**重叠与陷阱**，适合高级读者。

## 概要

从哲学例子推演到可约简为 `T` 的命题，再演示加规则后 `(Mortal Plato)` 可归约及 backward chaining 式查询。
