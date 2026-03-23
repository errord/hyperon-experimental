---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# d5_auto_types.metta

## 文件角色

**pragma! type-check auto**：打开自动类型检查后，良构/错误表达式、`collapse`、`match`、`let` 与 `f` 包装器的行为差异。

## 原子分类

- **pragma**：`!(pragma! type-check auto)`。
- **自定义类型**：与 d4 类似的 Entity/Human 例子。
- **内建**：`+`、`==` 与 `Error`。

## 关键运算/函数

`assertEqualToResult`、`assertAlphaEqualToResult`、`collapse`、`let`、`match`。

## 演示的 MeTTa 特性

- 自动检查下 **BadArgType** 表面化。
- `collapse` 会触发对子式的求值从而暴露类型错误。
- `match` **不对模式做类型检查**（元编程/遗传编程场景动机）。
- `let` 绑定体可能延迟报错；显式类型签名函数 `f` 在调用点检查参数。

## 教学价值

把 b5 的运行时类型与 **全局自动检查**开关对照，明确各原语的检查责任。

## 概要

数值与字符串混用报错、`==` 异类命题报错、`match` 仍接受坏模式，以及 `f (+ 5 "S")` 在内层暴露错误。
