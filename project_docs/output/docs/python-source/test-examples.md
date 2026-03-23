---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_examples.py 分析报告

## 文件角色

**端到端示例式集成测试**：接地对象与 `py-dot`、关键字参数、空间自修改、Global/PrimitiveAtom 与可变语义、依赖类型风格规则、多空间交互、字符与字符串类型。

## 测试覆盖摘要

- 注册 `&obj` 后在异空间 `interpret` 仍可替换；若在另一 MeTTa 中直接解析则失败。
- `OperationAtom` + `Kwargs` 多种调用形态。
- `add-atom` / `remove-atom` / `match` 实现简单状态存储。
- `Setter` / `SetAtom` 区分引用与按值、以及 `PrimitiveAtom` 同一实例更新。
- 自定义 `(:?` / `(:check` 与 `:=` 或 `::` 两套语法；否定样例。
- 两个 `MeTTa` 实例，`&space1` 引用与 `borrow` / `how-it-works?` 的上下文差异。
- `'A'` vs `"A"` 的 `repr` 与 `get-type`（Char vs String）。

## 关键断言/特性

- `assertEqualMettaRunnerResults` 大量用于复杂多行程序输出。
- 多空间：`borrow &space1 (how-it-works?)` 在 space2 得到 `success`，而 space1 自身仍为 `failure`。

## 小结

偏文档与回归：展示 Python–MeTTa 互操作与解释器在多空间下的实际行为（含已知“棘手”注释）。
