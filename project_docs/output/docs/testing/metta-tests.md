---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# MeTTa 脚本测试说明

## 存放位置

- 回归用脚本：`python/tests/scripts/`
- **Sandbox** 演示：`python/sandbox/**/*.metta`
- 部分 **Rust** 测试通过 `include_str!` 内嵌小段 **MeTTa**。

## 执行方式

1. **Python**：测试中构造 `MeTTa()`，用 `run` / `load_module_at_path` 指向脚本路径。
2. **REPL**：`metta-py` 手动 `import!` / `include`。
3. **Rust**：`run_program` / `assert_eq_metta_results`（见 `lib` 内测试）。

## 编写脚本测试

- 保持每个文件聚焦单一行为，便于失败定位。
- 使用 `;` 注释说明意图。
- 需要模块路径时，使用相对 **include** 或测试里临时修改 **working_dir**。

## 与 golden 输出

部分测试比较 **Atom** 的 `repr` 或结构化结果；修改 **stdlib** 时注意批量更新期望。

## 性能

长时间搜索或非确定性用例应加 **pragma** 限制栈深或缩小搜索空间，避免 **CI** 超时。
