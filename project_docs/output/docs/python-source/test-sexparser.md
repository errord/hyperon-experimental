---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_sexparser.py 分析报告

## 文件角色

**SExprParser** 语法树与错误路径：叶子节点类型序列、未闭合字符串、未闭合括号。

## 测试覆盖摘要

- `parse_to_syntax_tree` → `unroll()`，检查 `SyntaxNodeType` 序列（括号、词、空白、字符串）。
- 错误串 `(+ one "one` → `SyntaxError('Unclosed String Literal')`。
- `(+ one "one"` → `Unexpected end of expression`。
- 合法 `(+ one "one")` 经 `Tokenizer` 解析非空。

## 关键断言/特性

- 显式捕获 `SyntaxError` 与消息字符串相等。

## 小结

独立于 MeTTa runner 的底层 S-expression 词法/语法测试。
