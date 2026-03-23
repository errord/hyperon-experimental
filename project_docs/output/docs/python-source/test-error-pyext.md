---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# error_pyext.py 分析报告

## 文件角色

**故意加载失败**的扩展模块夹具：在 `@register_tokens` 回调中抛出异常。

## 测试覆盖摘要（作为夹具）

- `my_get_runner` 注册阶段 `raise Exception('This MeTTa module intentionally fails to load')`。
- `test_extend.ExtendErrorTest.test_error_pyext` 期望 `import!` 结果为 `Error` 形态（首子为 `S('Error')`）。

## 关键断言/特性

- 验证 Python 侧异常能传播到 MeTTa 层并呈现为错误原子。

## 小结

与 `extension.py` 成功路径互补，用于错误处理契约测试。
