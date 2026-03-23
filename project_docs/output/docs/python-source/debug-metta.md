---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# debug_metta.py（仓库根）

## 文件角色

**IDE 调试入口**：配合 VS Code/Cursor 的「Python: 交互式 MeTTa 调试」配置，在 `MeTTa.run` 与 **`RunnerState` 单步**（`run_step`）上设断点，跟踪解释器状态。

## 关键特性与集成

- **hyperon**：`MeTTa`、`RunnerState`。
- **示例**：一步执行 `!(+ 1 2)`；循环打印每步 `current_results`。

## 摘要

开发者辅助脚本，无业务逻辑；核心价值是衔接 Python 调试器与 MeTTa 执行栈。
