---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `agents/events/basic_bus.py` 分析报告

## 文件角色

提供**进程内、同步、极简**的事件总线实现，并注册为 MeTTa 原子，供代理与测试使用（与真实 SingularityNET 节点无关，日志器名为 `MockNode`）。

## 公开 API

- **`event_atoms()`**（`@register_atoms`）：返回 `basic-event-bus` → 构造 `BasicEventBus` 的 `OperationAtom`。

## 核心类

**`BasicEventBus`**

- `subscriptions: defaultdict(list)`：主题 → 回调列表。
- `create_subscription(topic, cb)`：追加订阅。
- `publish(topic, msg)`：同步遍历该主题下所有 `cb(msg)`（无异常隔离）。
- `terminate()`：置 `is_running = False`（当前 `publish` 未检查该标志）。
- `get_logger()`：返回 `logging.getLogger("MockNode")`。

## 小结

最小 viable 总线：`publish` 即同步派发。适合单元测试与 `EventAgent` 的 `direct-subscription` / `queue-subscription` 演示，不具备队列背压、异步或分布式语义。
