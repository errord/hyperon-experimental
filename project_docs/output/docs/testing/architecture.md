---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 测试架构

## 分层

| 层级 | 工具 | 范围 |
|------|------|------|
| **Rust** 单元与集成测试 | `cargo test` | `hyperon-atom`、`hyperon-space`、`lib` 解释器、**stdlib** |
| **Python** 绑定与 API | `pytest` | **hyperonpy**、**MeTTa** 从 **Python** 驱动 |
| **MeTTa** 脚本 | `metta.run` / **CI** 中的脚本目录 | 端到端语言行为 |
| **C** API | **Rust** `#[test]` 与 **FFI** 样例 | 头文件与绑定一致性 |

## **CI**

GitHub Actions 工作流（如 `ci-auto.yml`）在推送与 **PR** 上执行 **Rust** 与 **Python** 测试矩阵；发布流程单独构建 **wheel** 与 **Docker** 镜像。

## 测试环境

- **Python**：`Environment.test_env()` 返回的 **EnvBuilder** 可隔离配置目录与 **include** 路径。
- **Rust**：`#[cfg(test)]` 模块与 `hyperon_common::assert_eq_metta_results` 等宏辅助断言 **MeTTa** 结果。

## 目录约定

- `python/tests/`：**pytest** 收集根。
- `python/tests/scripts/`：供 **Python** 测试加载的 **`.metta`** 与数据。
- 各 crate 内联 `tests/` 或 `src/*_tests.rs`。

## 与设计文档的关系

行为以测试为准；规范文档（如 `../metta-lang/specification.md`）描述意图，若冲突应修正实现或更新文档。
