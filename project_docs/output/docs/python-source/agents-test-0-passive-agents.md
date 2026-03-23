---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/hyperon/exts/agents/tests/test_0_passive_agents.metta"
---

# agents：test_0_passive_agents.metta

## 文件角色

**agents 扩展**的集成测试：被动智能体、基于表达式的智能体、无事件总线的 `event-agent` 行为及 Python 属性访问。

## 关键原子/函数

- `import! &self agents`
- `create-agent`、`event-agent`
- `add-reduct`、`assertEqual`
- `my-agent`、`g`、`h`、`f`（内联 quote 定义）

## 概要

覆盖：从 `agent.metta` 创建智能体并调用 `(g 3)`；用 `quote` 内联规则创建智能体并调用 `(f 10)`；将 `event-agent` 绑定为 `my-agent` 并多次调用 `(h …)`、`(g …)`；断言 `.is_daemon` 为 `False`。验证被动模型下无总线时与普通过载调用一致。
