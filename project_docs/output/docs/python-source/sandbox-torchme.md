---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# torchme.py（沙箱）

## 文件角色

实验性 **PyTorch ↔ MeTTa** 桥接：根据预生成的 JSON 签名，将 `torch:函数名` 注册为可调用 grounded 操作；配合 `kwargsme`、`parsing_exceptions` 扩展 MeTTa 词法/语义。

## 关键特性与集成

- **依赖**：`torch`、`hyperon`（`register_tokens`、原子类型）、本地 `kwargsme`、`parsing_exceptions`、`torch_func_signatures.json`（缺失则抛错）。
- **TensorValue / PatternValue / PatternOperation**：张量模式匹配、延迟「模式运算」、按行解构匹配。
- **torch_function_decorator**：把 MeTTa 参数解包为 `kwargs` 调用 `torch`/`Tensor` 方法；处理 `result_type`、`split` 的 `indices_or_sections`、`dtype` 字符串、`tensor` 构造等特例。
- **注册**：正则 `torch\:[^\s^\.]+` 映射到动态生成的 `OperationObject`/`PatternOperation`；`kwargs` → `pairs_to_kwargs`。

## 摘要

沙箱原型：用文档解析得到的签名批量暴露 PyTorch API，并尝试在张量上做 MeTTa 侧匹配。路径与 C 扩展签名强耦合，适合研究集成而非生产使用。
