---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_include.metta

## 文件角色

Python 侧 **include/加载** 相关测试的微型数据：向 `&self` 注入一条原子，供“包含后再匹配”类用例使用。

## 原子分类

- **事实**：`(five isprime)`、`(seven isprime)`。
- **命令式**：`!(add-atom &self (six notprime))`。

## 关键运算/函数

`add-atom`；隐式依赖 `match` 测试（由测试代码驱动）。

## 演示的 MeTTa 特性

- 文件即**可追加知识片段**，与静态脚本组合。
- `&self` 在测试中作为被修改空间。

## 教学价值

说明测试如何通过外部 `.metta` **准备数据库状态**，而非全写在 Python 字符串里。

## 概要

两条素数声明加一条运行时添加的非素数事实，用于包含语义回归。
