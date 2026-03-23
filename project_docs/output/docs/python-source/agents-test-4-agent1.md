---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/hyperon/exts/agents/tests/test_4_agent1.metta"
---

# agents：test_4_agent1.metta

## 文件角色

事件驱动智能体 **A**：在收到 `Start` 命令时向另一智能体发 `Ping`，收到 `Pong` 后置位成功状态。

## 关键原子/函数

- `has-event-bus`、`new-state`、`add-atom`、`change-state!`
- `on_command Start`、`on_event Pong`
- `publish-event`、`queue-subscription`
- `success?`（可变状态原子）

## 概要

断言已挂事件总线；注册 `(success?)` 状态为 `False`；`on_command` 在 `Start` 时 sleep 后向 `"event-agent-1"` 发 Ping；`on_event Pong` 将 `(success?)` 设为 `True`；订阅 `"command"` 与 `"event-agent-2"`。与 `test_4_agent2.metta` 配对完成握手。
