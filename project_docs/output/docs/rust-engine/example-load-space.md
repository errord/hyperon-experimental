---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `lib/examples/load_space.rs` 分析报告

## 文件角色

命令行工具：从文件流式解析 MeTTa 原子填入 `GroundingSpace`，打印加载耗时与内存增量（`ra_ap_profile::memory_usage`），可选第二参数作为查询模式。

## 关键 API

- `SExprParser::new(BufReader<File>)`、`Tokenizer::new`、`space.add` / `space.query`

## 小结

面向大文件/图数据场景的加载与单次查询基准；注释中保留对索引结构的调试思路。
