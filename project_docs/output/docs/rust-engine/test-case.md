---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `lib/tests/case.rs` 分析报告

## 文件角色

集成测试：通过 `Metta::run` + `SExprParser` 验证 MeTTa 内置 `case` 的语义（顺序匹配、变量分支、与 `superpose` 的非确定性组合、`Empty` 分支、以及类似 `Maybe` 的函数式用法）。

## 关键 API / 测试覆盖

- `Metta::new(Some(EnvBuilder::test_env()))`、`SExprParser::new`、`assert_eq_metta_results!`
- 覆盖：`case` 与算术、`superpose`、空结果、`match &self` 解构关系、`Empty`、自定义 `maybe-inc`。

## 小结

用「期望 MeTTa 程序」对照「被测程序」做端到端断言，重点锁定 `case` 在顺序、非确定性与空结果上的行为，并延伸到基于空间的模式匹配示例。
