---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "integration_tests/das/test.metta"
---

# other：test.metta（DAS）

## 文件角色

**DAS 客户端**端到端断言：`new-das!` 连接本地端口区间，对远程知识库做 `match` 并与期望结果集比较。

## 关键原子/函数

- `import! &self das`
- `new-das!`、`das-service-status! pattern_matching_query`
- `match &das`、`assertEqualToResult`
- `das-helpers! sleep`

## 概要

绑定 `&das` 后等待 pattern_matching 就绪；查询 `is_animal` 对应概念列表、`snake` 上成立的谓词、`no_legs` 的概念；查询间 `sleep 2` 缓解网络时序。数据依赖 `animals.metta` 已载入 DAS。
