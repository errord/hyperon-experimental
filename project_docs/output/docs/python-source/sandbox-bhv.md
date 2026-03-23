---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# bhv_binding.py（沙箱）

## 文件角色

将 **BHV（超向量）** 库绑定为 MeTTa 原子操作：`bhv-new`、`bhv-majority`、`bhv-bind`（XOR）、相似度/置换等，通过 `@register_atoms` 暴露。

## 关键特性与集成

- **依赖**：`bhv.np` 中 `NumPyBoolBHV`、`NumPyBoolPermutation`（外部 `bhv` 包）。
- **操作**：随机向量、majority、绑定、相对 std_apart、related、随机置换、应用置换 `a(b)`。

## 摘要

极小胶水层，把分布式超向量运算挂到 MeTTa；无业务逻辑，典型沙箱扩展示例。
