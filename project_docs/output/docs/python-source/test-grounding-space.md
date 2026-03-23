---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_grounding_space.py 分析报告

## 文件角色

**GroundingSpaceRef / GroundingSpace** 默认空间实现的行为测试，以及子类扩展 `query` 的示例。

## 测试覆盖摘要

- 与 `test_custom_space` 类似的增删改、合取查询 `(, (A $x) (C $x))`。
- 嵌套：`G(nested)` 注册为 token `nested`，`!(match nested (A $x) $x)`。
- `SpaceRef(GroundingSpace())` 包装原生 Python 类时的 remove/query。
- `ExtendedGroundingSpace`：在查询外包一层 `(blue ...)` 并向结果注入 `color`。

## 关键断言/特性

- 合取查询期望单一绑定 `x -> B`。
- 扩展 `query` 返回额外变量 `color -> blue`，红色条目不匹配修改后的模式。

## 小结

验证 Rust 侧默认 grounding space 的 Python 封装与子类化钩子。
