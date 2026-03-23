---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_extend.py 分析报告

## 文件角色

**Python 扩展模块加载**测试：`import!` 单文件模块、包目录、深层递归包名、`@grounded` 装饰器，以及扩展抛错时的错误传播。

## 测试覆盖摘要

- `!(import! &self extension)`：`get-by-key`、`&runner` 为当前 `MeTTa`、`triple`  grounded 函数。
- `@grounded(metta) def abs_dif` 无需单独 py 模块文件即可注册。
- `ext_dir` 包与 `ext_recursive:level-2:ext_nested` 路径导入与相同字典/ runner 断言。
- `extension` 模块全局 `g_object`：`set-global!` / `get-global` 跨 `run` 与 Python `import` 可见。
- `error_pyext`：`import!` 结果首子为 `Error`。

## 关键断言/特性

- 期望三元组：`[[E()], [ValueAtom(5)], [ValueAtom('B')]]`（空表达式 + 字典查找）。
- `test_extend_subdir_pymod` 整段注释禁用（LP-TODO）。

## 小结

验证 `hyperon.ext` 注册钩子与 MeTTa 模块搜索路径；递归导入确保父包被加载。
