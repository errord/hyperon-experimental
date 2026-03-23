---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `repl/src/interactive_helper.rs` 分析报告

## 文件角色

rustyline `ReplHelper`：文件名补全、历史提示、基于语法树的 ANSI 高亮、括号匹配高亮，以及通过 `MettaShim::parse_line` 的多行/强制提交校验逻辑。

## 关键 API

- `parse_and_unroll_syntax_tree` + `SyntaxNodeType` → 配色；`StyleSettings::new` 从 MeTTa config state 读字符串/表达式向量  
- `Validator`：合法则提交；不完整则插换行；`force_submit`（Ctrl-J）与「行尾连续换行」触发语法错误提示  
- 括号函数 `find_matching_bracket` / `check_bracket` 衍生自 rustyline 12 MIT 源码（文件内声明）  

## 小结

高亮与校验都尽量不依赖完整求值，仅语法层；已知限制：注释/字符串内的括号可能影响括号匹配行为（注释标明）。
