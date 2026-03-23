---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_pln_tv.py 分析报告

## 文件角色

**概率/真值（STV）风格** 的 MeTTa 片段测试：用纯等式定义 `stv` 在 `And` 上的聚合，以及 `pln` 包装器与非确定性匹配。

## 测试覆盖摘要

- 定义 `min`、`s-tv`/`c-tv`、`stv (And ...)` 与 `(P A)`/`(P B)` 的默认 STV。
- 可选 `:` 类型声明（Concept/Predicate）。
- `pln` 宏：`!(pln (And (P A) (P B)))` 得 `(stv 0.3 0.8)`。
- `!(pln (And (P A) (P $x)))` 期望**两个**结果分支（A 与 B），并带注释说明与声明式 `.tv` 的差异。

## 关键断言/特性

- `assertEqualMettaRunnerResults` 与 `parse_all` 期望列表对齐。

## 小结

偏逻辑编程/PLN 演示的回归测试，强调函数式 STV 与 `match` 生成多解的行为。
