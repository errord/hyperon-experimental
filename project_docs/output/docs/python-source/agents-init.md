---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `agents/__init__.py` 分析报告

## 文件角色

`hyperon.exts.agents` 包对外接口：导出代理基类与 MeTTa 原子注册入口。

## 公开 API

- `AgentObject`、`EventAgent`（来自 `agent_base`）
- `agent_atoms`（`@register_atoms(pass_metta=True)` 的注册函数）

## 核心类

无（再导出）。

## 小结

供 `metta-motto` 等依赖以 `from hyperon.exts.agents import ...` 使用，避免直接依赖 `agent_base` 模块路径。
