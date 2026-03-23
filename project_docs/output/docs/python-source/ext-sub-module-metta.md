---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# ext_sub/module.metta

## 文件角色

**扩展/嵌套模块路径**测试的一行入口：从子目录模块导入 `self:ext_nested`，验证模块名与路径解析。

## 原子分类

- **导入**：`import! &self self:ext_nested`。

## 关键运算/函数

`import!`；依赖外部 `ext_nested` 包/模块布局（由测试环境提供）。

## 演示的 MeTTa 特性

- `self:` 前缀与嵌套扩展目录的**模块标识**约定。
- 极短文件强调“模块文件可仅为导入 re-export”。

## 教学价值

帮助理解 Python 扩展树中 **MeTTa 模块边界**如何映射到 `import!`。

## 概要

单行将嵌套扩展载入当前 `&self`，供扩展加载集成测试引用。
