---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `lib/tests/types.rs` 分析报告

## 文件角色

在 MeTTa 中演示简单「类型检查」与错误分支，并通过自定义 grounded `IsInt` 扩展分词器。

## 关键 API / 测试覆盖

- `tokenizer().register_token`、`Metta::run`、`UNIT_ATOM` 多次
- `IsInt`：`Grounded` + `CustomExecute`，对 `Number::Integer` 返回 `Bool`

## 小结

测试说明类型谓词可在 MeTTa 层组合（`check`），失败路径产生 `Error` 表达式；宿主侧用 `register_token` 注入 `is-int`。
