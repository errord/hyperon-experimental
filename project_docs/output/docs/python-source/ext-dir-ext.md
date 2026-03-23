---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# ext_dir/ext.py 分析报告

## 文件角色

与根目录 `extension.py` **几乎相同**的扩展实现：`&my-dict`、`get-by-key`、全局 `g_object` 读写、`&runner` token；**不包含** `extension.py` 中的 `@grounded triple` 函数。

## 测试覆盖摘要

- `test_extend_dir_pymod` 仅断言 `get-by-key` 与 `&runner`，不依赖 `triple`。

## 关键断言/特性

- 与 `extension.py` 对照：目录模块场景下不需要演示 `@grounded` 装饰器亦可完成导入测试。

## 小结

用作 **`ext_dir` 包的实际注册逻辑**；刻意精简以避免与单文件 `extension` 测试重复断言。
