---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# extension.py 分析报告

## 文件角色

**被 `test_extend.py` 导入的示例扩展模块**（非 unittest）：通过 `hyperon.ext` 向 MeTTa 注册原子、token 与 `@grounded` 函数。

## 测试覆盖摘要（作为夹具）

- 模块级 `g_object` 与 `set_global`：供 `set-global!` / `get-global` 使用。
- `@register_atoms`：`&my-dict`、`get-by-key`。
- `@register_tokens(pass_metta=True)`：`&runner` → 当前 `MeTTa` 实例。
- `@grounded def triple(x)`：`triple` 暴露为接地运算（`x*3`）。

## 关键断言/特性

- 无内置断言；行为由 `test_extend.py` 中 `import! extension` 后运行 MeTTa 代码验证。

## 小结

演示扩展 API 的标准写法；与 `error_pyext` 对照（成功加载路径）。
