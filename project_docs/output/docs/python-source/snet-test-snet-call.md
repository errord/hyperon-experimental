---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/hyperon/exts/snet_io/test_snet_call.metta"
---

# snet_io：test_snet_call.metta

## 文件角色

**snet_io** 调用层演示：底层客户端、`py-dot`、JSON 请求 hack、`get_service_callers`、`create_service_space` 与通道存款示例。

## 关键原子/函数

- `import! &self snet_io`
- `snet-sdk create_service_client`、`create_service_space`
- `py-dot`、`get_service_callers`、`add-reduct`
- `generate`、`neural_summarisation`、`gen_gpt_2`
- `open_channel_and_deposit`

## 概要

绑定多个 NAINT 服务客户端，演示消息查询、用 `repr`/字典式 hack 调 `code-generation`，为 `generative-lms` 注入 `generate` 包装，并用 `create_service_space` 加载 `abstractive-summarisation` 与 `text-generation` 的便捷调用。含 image-generation 失败注释与 AGIX 通道示例。
