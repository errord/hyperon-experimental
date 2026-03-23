---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_modules.py 分析报告

## 文件角色

**模块系统**：`.py` 文件作为 MeTTa 模块（`PythonFileModuleFormat`）、`include` 指令，以及扩展包 `py_ops` 的导入与布尔解析。

## 测试覆盖摘要

- `import! &self pyfile_test_mod`：无错误，`pi_test` token 解析为 `ValueAtom(3.14159)`。
- `include test_include`：匹配 `isprime` 事实在 include 前后集合变化（`three` → `three,five,seven`），`notprime` 得 `six`。
- `PyOpsTest`：`config_dir=""` 下 `import! py_ops`，字符串重复 `* "a" 4`；`id False`/`True` 保持布尔接地值。

## 关键断言/特性

- `atom_is_error` 否定断言保证加载成功。
- `areEqualNoOrder` 用于 include 前后多结果比较。

## 小结

衔接磁盘上的 `pyfile_test_mod.py` 与 `test_include` 等资源文件；`py_ops` 依赖工程内扩展布局。
