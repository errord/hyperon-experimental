---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# ext_recursive/level-2/ext_nested/__init__.py 分析报告

## 文件角色

**深层目录 + 点分模块名** `ext_recursive:level-2:ext_nested` 的包入口：`from .ext import *`。

## 测试覆盖摘要

- `test_extend_recursive_pymod`：`import! &self ext_recursive:level-2:ext_nested` 后验证与 `ext_dir` 相同的 `get-by-key` / `&runner` 行为。

## 关键断言/特性

- 验证递归/层级路径导入时父包被正确加载（测试注释说明）。

## 小结

专门服务于**冒号路径 MeTTa 模块名**与磁盘层级对齐的集成测试。
