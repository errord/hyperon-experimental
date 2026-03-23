---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `repl/src/metta_shim.rs` 分析报告

## 文件角色

REPL 与 MeTTa 之间的唯一边界：`MettaShim` 统一 `exec` / `print_result` / 配置读取 / 行解析；`feature = "python"` 时通过嵌入的 `py_shim.py` 驱动 HyperonPy，否则直接调用 `hyperon::metta`。

## 关键 API（无 Python）

- `EnvBuilder` 初始化 common env + include 路径；`Metta::new(None)`  
- `RunnerState::new_with_parser` 循环 `run_step`，配合 `exec_state_prepare` / `exec_state_should_break` 响应 SIGINT  
- 配置：`get_config_atom` 通过 `!(get-state ...)` 执行后从结果取 `Str`  

## 关键 API（Python）

- 校验 `hyperon.__version__` 与 `CARGO_PKG_VERSION` 精确一致  
- `RunnerState` / `run_step` / `run_is_complete` 在 GIL 下调用  

## 辅助

- `parse_and_unroll_syntax_tree`：供高亮遍历 `SyntaxNodeType` 与源区间  

## 小结

双路径是为在仅能经 HyperonPy 链接引擎时的过渡方案（见文件内 issue 引用）；中断处理与步进式执行保证 REPL 可取消长运行求值。
