---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# repl.default.metta

## 文件角色

Hyperon **REPL 启动默认配置**：通过 `change-state!` 设置提示符、ANSI 高亮样式及部分交互状态（含 TODO 注释）。

## 原子分类

- **状态名**：`&ReplPrompt`、`&ReplStyledPrompt`、`&ReplBracketStyles` 等 REPL 专用 token。
- **字面量**：ANSI 转义字符串、颜色代码。

## 关键运算/函数

`change-state!`；注释中未启用的 `&ReplHistoryMaxLen`、`&ReplBracketMatchEnabled`。

## 演示的 MeTTa 特性

- REPL 行为由 **MeTTa 状态原子**驱动，可版本化与用户定制。
- 字符串中的 `\x1b[...m` 终端着色与语法高亮样式表。

## 教学价值

展示“宿主壳”仍可用 MeTTa **数据驱动配置**，便于主题/无障碍改造。

## 概要

设置绿色粗体提示符与括号/注释/变量/字符串/错误/匹配高亮配色，并记录待办的价值桥接问题。
