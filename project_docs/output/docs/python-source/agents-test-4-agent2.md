---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/hyperon/exts/agents/tests/test_4_agent2.metta"
---

# agents：test_4_agent2.metta

## 文件角色

事件驱动智能体 **B**：收到 `Ping` 后向智能体 A 回发 `Pong`，完成事件环。

## 关键原子/函数

- `has-event-bus`、`on_event Ping`
- `publish-event`、`queue-subscription`

## 概要

极简中继：订阅 `"event-agent-1"`，在 `Ping` 上向 `"event-agent-2"` 发布 `Pong`。与 agent1 的 `Start -> Ping` 流程闭合，使 agent1 能收到 `Pong` 并更新状态。
