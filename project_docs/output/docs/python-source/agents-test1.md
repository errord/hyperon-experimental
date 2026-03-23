---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `agents/tests/test_1_python_agents.py` 分析报告

## 文件角色

可执行脚本式测试：验证纯 Python `AgentObject` 子类在 MeTTa 中的创建、`.方法` 调用、与 `create-agent` 加载的 MeTTa 代理组合。

## 公开 API

无（测试模块）。

## 核心类

- `MyAgent`：`__call__(a,b)` 与 `.subs(a)`。
- `Agent1`/`Agent2`/`Agent3`：生成器链式 `yield`，测非并发流式组合。

## 小结

两段断言：`assertEqual` 与嵌套 `((new-agent-3) ((new-agent-2) ((new-agent-1))))` 应得到 `[0,2,...,18]`。依赖 `hyperon.exts.agents` 与 `agents` 扩展。
