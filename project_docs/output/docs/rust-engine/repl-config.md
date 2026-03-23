---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `repl/src/config_params.rs` 分析报告

## 文件角色

REPL 配置常量与启动参数：`ReplParams` 根据 `MettaShim::config_dir()` 定位 `repl.metta` 与 `history.txt`，若缺省则写入内置 `repl.default.metta`。

## 关键符号

- `CFG_PROMPT`、`CFG_STYLED_PROMPT`、`CFG_*_STYLE`、`CFG_HISTORY_MAX_LEN` 等 state 名称（与 MeTTa `bind!` 对应）  
- `builtin_init_metta_code()`：注入默认 prompt、ANSI 彩色 prompt、括号/注释/变量等样式 state 初值  

## 小结

样式与提示完全 MeTTa 化，便于用户改 `repl.metta`；部分 `bind!`（历史长度、括号匹配开关）因值桥接未就绪而注释为 TODO。
