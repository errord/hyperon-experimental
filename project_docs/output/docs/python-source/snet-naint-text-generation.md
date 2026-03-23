---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/hyperon/exts/snet_io/snet/naint/text-generation.metta"
---

# snet_io：text-generation.metta

## 文件角色

**说明与讨论用**的 SingularityNET `text-generation` 服务草图：含生成代码示意、类型包装讨论与本体草图；注释标明不应被 import（部分为自动生成示例）。

## 关键原子/函数

- `snet-sdk create_service_client`、`add-reduct`
- `(naint text-generation)`、`gen_gpt_2`（`Kwargs` 传参）
- 注释中的 `:<proto` / `named-param` 等设想

## 概要

展示用 `create_service_client` 注册服务调用器，并定义 `gen_gpt_2` 将 MeTTa 参数映射到 `"Query"` 调用。后半为 OPTION1/2 类型设计与 AI 本体关系草案，非可执行测试。
