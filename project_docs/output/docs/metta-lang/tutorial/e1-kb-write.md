---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# e1_kb_write.metta

## 文件角色

**多空间工作流**：用 `bind! &kb (new-space)` 建立辅助知识库，在推理同时将结论 `add-atom` 写入 `&kb`。

## 原子分类

- **主空间规则**：`frog`、`green`、`croaks`、`eat_flies`、`ift`。
- **辅助空间**：`&kb` 中动态事实 `Green $x`。

## 关键运算/函数

`new-space`、`bind!`、`add-atom`、`match`、`assertEqualToResult`。

## 演示的 MeTTa 特性

- `ift (green $x) (add-atom &kb (Green $x))` 对多绑定产生**多副作用**（多 `()` 结果）。
- 随后 `match &kb` **检索归纳结果**（Fritz、Sam）。

## 教学价值

把“推理”和“记忆写入”分离到不同 Atom 空间，是代理/学习系统的常见模式。

## 概要

规则推出谁 `green`，把 Green 断言积累到 `&kb`，再查询 `&kb` 枚举绿色实体。
