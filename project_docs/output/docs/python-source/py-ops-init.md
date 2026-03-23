---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `py_ops/__init__.py` 分析报告

## 文件角色

`hyperon.exts.py_ops` 包的入口，仅做符号再导出。

## 公开 API

从 `pyop` 子模块导出：`arithm_types`、`arithm_ops`、`bool_ops`（供扩展注册机制加载）。

## 核心类

无（本文件无类定义）。

## 小结

三行包装模块：导入者在 `import hyperon.exts.py_ops` 时即可拿到 MeTTa 词法/运算扩展注册函数。
