---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/hyperon/exts/agents/tests/agent.metta"
---

# agents：agent.metta

## 文件角色

被动智能体测试用的**微型 MeTTa 模块**：定义可被 `create-agent` 加载的规则，供 `test_0_passive_agents.metta` 等调用。

## 关键原子/函数

- `(g $t)`、`(h $a $b)`：简单递归式规则；`g` 委托给 `h`，`h` 实现为乘法 `*`。

## 概要

两行等价关系：对数值 `t`，`(g t)` 归约为 `(h t t)` 即 `t * t`。用于验证从文件创建的智能体能正确执行空间内规则（例如 `(g 3) -> 9`）。
