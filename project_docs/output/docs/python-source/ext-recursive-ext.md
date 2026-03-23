---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# ext_recursive/level-2/ext_nested/ext.py 分析报告

## 文件角色

与 `ext_dir/ext.py`、`ext_sub/.../ext.py` **同内容**：`&my-dict`、`get-by-key`、`set-global!`/`get-global`、`&runner`。

## 测试覆盖摘要

- 仅 `test_extend_recursive_pymod` 使用；断言不依赖 `triple` 或全局副作用以外的行为。

## 关键断言/特性

- 与浅层 `ext_dir` 共享同一逻辑，证明**加载路径深度**不改变注册结果。

## 小结

递归导入测试用的重复模块体；强调模块解析而非实现差异。
