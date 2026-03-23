---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `repl/src/main.rs` 分析报告

## 文件角色

`metta` 可执行 REPL：clap 解析可选脚本路径与 `-I` include 路径；构造 `MettaShim`；脚本模式执行并打印结果，否则进入 rustyline 交互循环。

## 关键行为

- 工作目录：有脚本则为脚本父目录，否则当前目录。  
- `ctrlc`：递增计数，提示中断；第三次强制 `exit(-1)`。  
- 交互：`builtin_init_metta_code`、`repl.metta`、历史文件、`ReplHelper` 高亮与校验；Enter vs Ctrl-J 提交策略（见注释）。  

## 小结

进程入口与信号、行编辑绑定集中在此；实际 MeTTa 执行委托 `MettaShim`（Python 或纯 Rust 两套实现由 feature 决定）。
