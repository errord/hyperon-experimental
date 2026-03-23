---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# parsing_exceptions.py（沙箱）

## 文件角色

**torchme 自动签名的手工覆盖表**：无法仅靠 JSON 签名表达的 `torch:*` 操作，在此映射为自定义 Python 实现（`OperationObject` + `unwrap` 标志）。

## 关键特性与集成

- **instantiate_module**：按符号名 `importlib` 加载模块并实例化 PyTorch 模块类，支持位置参数与 `Kwargs`。
- **to_device**：`.to(device=...)`。
- **run_trainer**：多 epoch 调用 `Trainer.train`/`test`。
- **Lambda**：`requires_grad_status`、`get_model_params`。
- **导出**：`parsing_exceptions` 字典供 `torchme.call_torchme_atoms` 查询。

## 摘要

补齐「文档解析不到的 Torch 用法」；与 `kwargsme` 协作处理构造参数。典型沙箱胶水代码。
