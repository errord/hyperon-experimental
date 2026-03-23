---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# ext_sub/ext_nested/ext.py 分析报告

## 文件角色

与 `ext_dir/ext.py` **同内容**：字典原子、全局 get/set、`pass_metta=True` 的 `&runner`；无 `triple`。

## 测试覆盖摘要

- 随 `ext_sub` 导入测试一并休眠；无活跃断言引用。

## 关键断言/特性

- 复制一份便于独立包路径而不与 `ext_dir` 共享模块对象。

## 小结

为子包导入场景准备的镜像实现；当前测试关闭。
