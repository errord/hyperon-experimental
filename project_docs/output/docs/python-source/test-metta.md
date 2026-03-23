---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_metta.py 分析报告

## 文件角色

**MeTTa 类 API**：解析时动态注册 token、`run` / `evaluate_atom`、`RunnerState` 步进、类型错误与语法错误、Rust/Python 接地原子混合 `match`。

## 测试覆盖摘要

- 同一标识 `A` 多次 `register_atom` 后 `parse_single` 结果随之变化。
- 经典 `frog`/`green` 规则，`run` 得 `[[T]]`，`evaluate_atom` 得 `[T]`。
- `RunnerState.run_step` 直到完成，累积结果 `repr` 为 `[[10]]`。
- `+ 2 "String"` 与显式 `Error ... BadArgType` 运行结果一致。
- 不完整表达式抛出 `RuntimeError('Unexpected end of expression')`。
- `match` 中 Rust 接地 `import!` 与 Python `True` 的用法；期望 `[[]]`。
- 依赖 stdlib 的 `let` 解构：`run('!(f)')` 与 `evaluate_atom(E(f))` 均得 `A`。

## 关键断言/特性

- 增量解析与 tokenizer 状态同步。
- 步进解释器与一次性 `run` 结果对齐。

## 小结

MeTTa Python 前端的核心行为回归，含错误路径与部分标准库依赖。
