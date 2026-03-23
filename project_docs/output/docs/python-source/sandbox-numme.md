---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# numme.py（沙箱）

## 文件角色

实验性 **NumPy ↔ MeTTa** 扩展：`@register_atoms` 注册 `np.vector`、`np.array`、`np.add/sub/mul/div/matmul` 等，并把 ndarray 包装为 **`NumpyValue`** 以支持简单模式匹配。

## 关键特性与集成

- **NumpyValue / PatternValue / PatternOperation**：结构与 `torchme` 中张量侧类似（按行解构、`rec` 递归求值、变量时延迟为模式）。
- **wrapnpop**：ungrounded 参数取 `.value`，结果打上 `NPArray` + shape 类型表达式。
- **注释**：FIXME 未为运算加严格类型。

## 摘要

与 torchme 对称的 numpy 沙箱；API 面小、实现直接，适合演示 grounded 数值与 MeTTa 的互操作。
