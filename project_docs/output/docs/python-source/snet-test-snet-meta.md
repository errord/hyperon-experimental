---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/hyperon/exts/snet_io/test_snet_meta.metta"
---

# snet_io：test_snet_meta.metta

## 文件角色

**元数据与发现**演示：仅需以太坊 RPC（或环境变量），列举组织/服务、无密钥查看服务消息、生成 MeTTa 形态调用说明并装入空间。

## 关键原子/函数

- `snet-sdk organization_list`、`service_list`
- `create_service_client`、`py-dot`（`get_service_messages`、`generate_callers_text`）
- `create_service_space`、`methods`

## 概要

展示 `service_list` 的位置/命名参数、`create_service_client` 后只读拉取 schema，以及 `create_service_space` 将整服务注入当前空间并可通过 `methods` 列出类型化函数。注释说明 `init` 与 `ETH_RPC_ENDPOINT` 可选关系。
