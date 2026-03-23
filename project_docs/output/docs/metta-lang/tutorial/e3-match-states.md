---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# e3_match_states.metta

## 文件角色

将 **State 嵌入知识库**：动态创建状态、用 `add-atom` 把 `(= (status (Goal $g)) $state)` 放入 `&self`，演示“空间不变、状态变”。

## 原子分类

- **规则**：`new-goal-status!` 定义。
- **事实**：`(Goal lunch-order)` 等的状态槽。
- **绑定示例**：`&state-active`（反模式警示）。

## 关键运算/函数

`new-state`、`add-atom`、`change-state!`、`get-state`、`match`、`if`、`superpose`。

## 演示的 MeTTa 特性

- 状态原子在空间中**同一地址**上可变，无需重插原子。
- 不推荐对可变 state 使用长期 `bind!` token（注释说明）。
- `match` 可直接匹配含 state 的等式；`get-state` + `if` 过滤目标 goal。

## 教学价值

连接 e2 的局部状态与**全局目标跟踪**用例（规划/任务状态）。

## 概要

创建两个 goal 的 inactive 状态，更新 `lunch-order` 为 active，演示匹配与条件查询。
