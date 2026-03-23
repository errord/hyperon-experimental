---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 模块 `hyperon.module` — 公共 API

## `MettaModRef`

对核心 **MeTTa** 模块句柄的薄包装。

### 构造

- `__init__(cmodref)`：一般由 **C** / **Rust** 侧传入，终端用户很少直接构造。

### 方法

- `tokenizer() -> Tokenizer`：返回该模块作用域的 **Tokenizer**（与 `RunContext.tokenizer()` 概念一致）。

## 与 `runner` 的关系

模块加载流程中，**Rust** 侧创建模块并调用 Python 注册的 `loader_func`；若需在当前模块上下文中注册 **token**，应使用 `RunContext` 的 API（`runner.RunContext`），`MettaModRef` 主要用于持有 `cmodref` 并暴露模块级 **Tokenizer**。

## 版本说明

模块版本与依赖解析仍在演进；未来可能在 `MettaModRef` 上增加 `space()`、`name()` 等绑定——以源码为准。
