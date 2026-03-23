---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `agents/events/__init__.py` 分析报告

## 文件角色

`hyperon.exts.agents.events` 子包入口，导出事件相关原子注册。

## 公开 API

从 `basic_bus` 再导出：`event_atoms`。

## 核心类

无。

## 小结

一行再导出，便于 `import hyperon.exts.agents.events` 时加载 `BasicEventBus` 对应的 MeTTa 操作符。
