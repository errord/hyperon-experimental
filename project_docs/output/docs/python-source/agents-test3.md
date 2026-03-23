---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `agents/tests/test_3_events_python.py` 分析报告

## 文件角色

验证 `EventAgent` + `BasicEventBus`：`direct-subscription` 立即在 MeTTa 中求值且不进入代理输出队列；`queue-subscription` 将事件入队并由 `event_processor` 求值，结果出现在 `get_output()`。

## 公开 API

无。

## 核心类

`FeedbackCatch`：订阅 `agent-event`，断言收到 `"Pong"`。

## 小结

脚本内构造 `EventAgent(code=..., event_bus=node)`，`start()` 后 `publish` 两主题并断言 `res == []`、`fc.catched`、`res2[0]` 为 `swapcase` 结果。文件头注释概括两种订阅语义差异。
