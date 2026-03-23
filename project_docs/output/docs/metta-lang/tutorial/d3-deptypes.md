---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# d3_deptypes.metta

## 文件角色

**Jetta `compile` API**：按名称或带元数将宿主函数注册进 Jetta，并双向验证 `jetta` 字符串调用与 `-gnd` 直接调用。

## 原子分类

- **宿主**：`boo`、`my-goo` 的类型与 `=`。
- **Jetta 空间**：`&jspace`。

## 关键运算/函数

`compile &jspace "boo"`、`compile &jspace my-goo 2`、`boo-gnd`、`my-goo-gnd`。

## 演示的 MeTTa 特性

- 宿主定义 → **编译进 Jetta** → 字符串远程调用。
- `compile` 参数错误时 `JettaCompileError` 与 `py-dot`/`case` 断言。

## 教学价值

理解 **MeTTa 与 Jetta 共享符号表**的桥梁及元数在 compile 中的作用。

## 概要

`boo`、`my-goo` 两例成功路径，以及对非法 `compile` 参数的错误字符串检测。
