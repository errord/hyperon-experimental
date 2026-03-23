---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_stdlib.py 分析报告

## 文件角色

**标准库与 Python 互操作**：`repr`/`parse`、字符序列、`py-atom`/`py-dot`、unwrap 模式、数值与字符串字面量、正则 token、`py-list`/`py-tuple`/`py-dict`/`py-chain` 及错误形态。

## 测试覆盖摘要

- 文本：`repr (my atom)`、`parse` 与引号转义、`stringToChars`/`charsToString`（`Char`）。
- `py-atom math`/`statistics`、`dict.get`、`str`、自定义类 `SimpleObject.method` + `Kwargs`。
- `py-dot &math pow`：`False` 类型错、`True`/箭头签名/默认 unwrap 得 `125.0`；`proc_atom_noreduce` + `unwrap=False` 使 `(+ 1 2)` 传入时不先归约（与 `let` 限制注释）。
- 整数/浮点/科学计数法加法与期望归一化。
- 字符串经 `id'` 恒等：空格、引号、换行等。
- `regex:"..."` 意图规则两条匹配、一条落空。
- 容器构造与嵌套；`py-chain` 按位或链；多种畸形 `py-dict`/`py-list` 期望 `Exception`。

## 关键断言/特性

- `atom_is_error` 用于错误路径；`assertRaises` 每次异常后重建 `MeTTa` 以隔离状态。

## 小结

Python 侧 stdlib 功能的宽覆盖；含跨平台注释（如 statistics 测试改写）。
