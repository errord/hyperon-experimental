---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# neurospace.py（沙箱）

## 文件角色

基于 **OpenAI Chat Completions**（`gpt-3.5-turbo-0613`）的 **「神经」接地空间**：用空间内原子与查询拼 prompt，让模型返回答案并解析为 MeTTa **绑定**。

## 关键特性与集成

- **NeuralSpace.query**：罗列事实 + 自然语言问题，要求 JSON `{ $var: answer }`；`_response2bindings` 正则抽取并构造 `BindingsSet`。
- **IntentSpace.query**：从预置主题列表中做话题分类，同样 JSON 返回。
- **register_atoms**：`new-neural-space`、`new-intent-space`。
- **依赖**：`OPENAI_API_KEY` 环境变量；API 为旧版 `openai` 同步接口。

## 摘要

LLM 即「可查询空间」的演示；强依赖外部服务与 prompt 格式，属探索性集成，非稳定核心功能。
