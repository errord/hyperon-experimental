---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `agents/agent_base.py` 分析报告

## 文件角色

**概念验证级**的 Python/MeTTa 双模「代理」基础设施：既可用 MeTTa 脚本当代理，也可让 Python 子类几乎无样板地暴露给 MeTTa；兼顾同步调用与（实验性）异步/守护线程场景。文件内注释说明线程模型尚不完整，后续可能由 MeTTa 层面的并行/流式原语承载。

## 公开 API

- **`StreamMethod(threading.Thread)`**：在子线程中迭代执行 `method(*args)`，结果入队；异常时向队列放入 `Error` 表达式。
- **`AgentObject`**：`get_agent_atom`、`agent_creator_atom`、`name`；实例支持从文件/`ExpressionAtom`/纯 Python 构造；`_create_metta`、`_load_code`、`__metta_call__`（支持 `.method` 形式调用 Python 方法）；`is_daemon` 为真时通过 `StreamMethod` 异步启动且当前返回空表达式（结果流未回传，TODO）。
- **`EventAgent(AgentObject)`**：可选 `event_bus`；注册 `&event_bus`、`queue-subscription`、`has-event-bus`；`start`/`stop`、`recv_queue_event`、`queue_subscription`、`event_processor`、`get_output`/`clear_outputs`；构造后 `_init_metta` 会 `! (import! &self agents)`。
- **`subscribe_metta_func(metta, event_bus, event_id, func)`**：在总线上订阅，回调内用 `metta.evaluate_atom(E(func, ValueAtom...))`。
- **`publish_event(event_bus, event_id, content)`**：断言 `event_bus` 为 grounded，调用 `publish`。
- **`agent_atoms(metta)`**（`@register_atoms(pass_metta=True)`）：注册 `create-agent`、`event-agent`、`direct-subscription`、`publish-event`。

辅助：`_try_atom2str` 将 `GroundedAtom`/`SymbolAtom` 等转为字符串键。

## 核心类

| 类/对象 | 要点 |
|---------|------|
| `StreamMethod` | 线程 + `Queue` 传递迭代结果；`__next__` 实现为在存活时非阻塞 `get_nowait`（与标准迭代器语义需注意）。 |
| `AgentObject` | 每个基于脚本的代理拥有独立 `MeTTa` 与空间；可通过 `get_agent_atom` 注入父级 `_metta`。 |
| `EventAgent` | 事件队列 + 单独线程 `event_processor` 中 `evaluate_atom`；`StopEvent` 用于停止循环。 |

## 小结

这是 metta-motto 所依赖的代理胶水层：**同步**路径直接返回 `method(*args)`；**daemon** 路径只起线程不回收流；**EventAgent** 把事件总线订阅与 MeTTa 规则桥接起来。整体设计标注为 preliminary，线程与流式语义仍待与核心 MeTTa 对齐。
