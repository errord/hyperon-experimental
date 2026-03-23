---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/hyperon/exts/agents/tests/test_4_events.metta"
---

# agents：test_4_events.metta

## 文件角色

**事件总线**端到端测试：两个 `event-agent` 协作，通过 `publish-event` / 订阅处理异步命令与回应。

## 关键原子/函数

- `import!`：`agents`、`agents:events`
- `basic-event-bus`、`bind!`、`event-agent`
- `.start` / `.stop`、`publish-event`
- `get-state`、`success?`、`py-atom time.sleep`

## 概要

创建共享 `&events`，挂载 `test_4_agent1/2.metta` 两个智能体并启动；发布 `"command" Start`；短暂睡眠后断言 agent1 的 `(success?)` 状态为 `True`；最后停止双方。依赖 agent1/2 内的 `queue-subscription` 与 `on_command` / `on_event` 链式 Ping-Pong。
