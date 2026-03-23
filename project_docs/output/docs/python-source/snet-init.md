---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `snet_io/__init__.py` 分析报告

## 文件角色

`hyperon.exts.snet_io` 包入口：`from .snet_gate import *` 暴露网关模块中全部公共符号。

## 公开 API

与 `snet_gate.py` 一致（如 `SNetSDKWrapper`、`ServiceCall`、`snet_atoms`、`pretty_print_atoms` 等）。

## 核心类

无（通配导入）。

## 小结

薄封装，便于 `import hyperon.exts.snet_io` 一次性获得 SingularityNET SDK 桥接实现。
