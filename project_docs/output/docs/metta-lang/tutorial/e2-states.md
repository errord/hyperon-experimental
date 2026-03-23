---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# e2_states.metta

## 文件角色

**State 原子**教程：`new-state`、`get-state`、`change-state!`、与 `StateMonad` 类型及错误情况。

## 原子分类

- **类型标注**：`(: (A B) PairAB)`。
- **状态 token**：`&state-token` 绑定到 `new-state`。
- **接地**：`StateMonad Number/String` 等。

## 关键运算/函数

`new-state`、`get-state`、`change-state!`、`get-type`、`nop`、`let`。

## 演示的 MeTTa 特性

- 状态封装：同一逻辑值可对应不同 state 包装仍 `assertEqual`。
- 状态类型由**初值**固定，错误 `change-state!` 返回 `Error BadArgType`。
- `let` 内新建与修改状态不污染外部；变量名与类型定义无冲突。

## 教学价值

在纯函数式归约语义中引入**可控可变单元**，解释 token 与内容区别。

## 概要

演示读写 `(A B)`、类型推断、非法类型变更报错，以及局部 `let` 状态块。
