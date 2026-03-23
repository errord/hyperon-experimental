---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `agents/tests/test_2_daemon.py` 分析报告

## 文件角色

演示并测试 `daemon = True` 的 `AgentObject`：`__metta_call__` 在后台线程运行 `__call__`，主线程通过 `.input`/`.response` 轮询队列（含 `sleep`，注释说明可能偶发失败）。

## 公开 API

无。

## 核心类

`DaemonAgent`：`messages`/`output` 队列、`stop`、`input`、`response`；`__call__` 中空转等待或反转消息。

## 小结

验证守护代理不直接返回调用结果、而是通过命名方法交互；使用 `py-atom time.sleep` 做时序同步。
