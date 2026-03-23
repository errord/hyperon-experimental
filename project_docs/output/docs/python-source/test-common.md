---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_common.py 分析报告

## 文件角色

**测试辅助库**（非典型 `test_*` 断言文件）：提供无序列表比较、MeTTa 多结果比较、原子等价断言及切换工作目录工具。

## 测试覆盖摘要

- `areEqualNoOrder`：用伪造哈希规避不可哈希元素，按多重集比较。
- `areEqualMettaRunResults`：逐行比较 MeTTa 运行结果，每行内无序。
- `HyperonTestCase`：`assertEqualNoOrder`、`assertEqualMettaRunnerResults`、`assertAtomsAreEquivalent`（基于 `atoms_are_equivalent`）。
- `change_dir_to_parent_of`：将 cwd 设为给定文件所在目录的父级（供模块加载类测试）。

## 关键断言/特性

- 等价性断言在长度一致前提下逐对检查 `atoms_are_equivalent`。

## 小结

被 `test_custom_space`、`test_examples`、`test_grounding_space` 等复用；减少顺序敏感导致的 flaky 比较。
