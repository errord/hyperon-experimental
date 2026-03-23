---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# repl/src/py_shim.py

## 文件角色

**REPL 与非 Python 宿主之间的薄 Python 封装**：初始化自定义环境的 `MeTTa`、加载模块、驱动 **`RunnerState` 分步运行**，并提供解析单行与读取 **config state** 的辅助函数。

## 关键特性与集成

- **init_metta**：`Environment.custom_env(working_dir, include_paths)`。
- **load_metta_module**：`import_file`。
- **start_run / run_is_complete / run_step**：异步/步进执行接口。
- **parse_line**：`SExprParser` + tokenizer，语法错误时返回消息字符串。
- **get_config_***：`!(get-state name)` 取配置原子/子表达式/字符串表示。

## 摘要

典型 FFI 适配层：把 MeTTa 运行时能力收敛为稳定、无 UI 的 API，供 Rust REPL 等调用。
