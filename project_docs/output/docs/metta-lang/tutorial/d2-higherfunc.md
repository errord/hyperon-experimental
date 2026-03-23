---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# d2_higherfunc.metta

## 文件角色

**依赖类型风格 + 非确定性搜索**：Jetta 中定义 `calc_err` 泛函，宿主用随机二进展开生成 λ，搜索使误差为零的函数。

## 原子分类

- **Jetta**：`calc_err`、`err` 等高阶类型。
- **宿主 Peano/二进制**：`Z`、`S`、`bin`、`num`、`rnd-square`。
- **接地比较**：`==`、`if`、`Empty`。

## 关键运算/函数

`jetta`、`let` 绑定 `rnd-square`；`if (== (jetta &jspace (calc_err $f)) 0)`.

## 演示的 MeTTa 特性

- 宿主非确定性 `(= (bin) 0/1)` 驱动 Jetta 端**数值检验**。
- 将符号 λ作为**数据**传入 Jetta 求值字符串/表达式。

## 教学价值

展示跨语言边界的**程序搜索**雏形（随机生成 + 零检验）。

## 概要

在 8 位二进制展开空间上随机抽 `rnd-square`，找到使 `calc_err` 在 Jetta 中为 0 的候选则返回该函数，否则 `Empty`。
