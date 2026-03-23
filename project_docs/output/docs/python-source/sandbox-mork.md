---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# mork.py（沙箱）

## 文件角色

**MORK 服务** 的初步 Python 封装：`MORKSpace` 通过 HTTP（`requests`）与默认 `127.0.0.1:8000` 通信；`mork-space` 原子创建带 UUID 名称的客户端句柄（`OperationAtom` 包装实例）。

## 关键特性与集成

- **方法**：`status`、`import_uri`、`export`（GET 返回文本再 `metta.parse_all`）；`query` 目前空实现；`add` 未实现。
- **register_atoms(pass_metta=True)**：注册 `mork-space`。

## 摘要

占位型远程空间适配器，大量 TODO；用于验证与 MORK server 的集成形态，非完整功能模块。
