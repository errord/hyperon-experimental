---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# metta_repl.py（沙箱）

## 文件角色

简易 **readline 交互式 REPL**（`metta> `），使用模块级 `MeTTaVS` 实例执行输入；并 **复制** `r.py` 的嵌入式 runner 与 **`resolve.py` 同构的 `::` 词法**（`my_resolver_atoms`）。

## 关键特性与集成

- **readline**：`~/.metta_history`、atexit 追加历史；`.history` 命令。
- **注意**：`my_imported_runner_atom` 在源码顺序上于模块级 `runner`/`runnerAtom` 初始化之前被定义，若注册在 import 阶段立即调用可能 **NameError**；更像未合并完成的草稿（与 `r.py`/`resolve.py` 拆分版对照使用更稳妥）。

## 摘要

本地调试用的 CLI 雏形；功能与正式 REPL 重复，维护状态实验性，使用前建议核对注册顺序或拆分为独立模块。
