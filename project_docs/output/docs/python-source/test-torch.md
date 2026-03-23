---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# python/integration/test_torch.py

## 文件角色

**集成测试**：验证 MeTTa 中注册的 grounded PyTorch 调用链 **不会切断 autograd**——经 `OperationAtom` 包装后多步训练 loss 仍应下降。

## 关键特性与集成

- **unittest**：`TorchDiffTest.test_torch_diff`。
- **DummyModel** + `RMSprop` + `CrossEntropyLoss`；可选 CUDA。
- **metta.register_atom**：`classify`、`&inputs`、`get-labels`、`loss-fn`、`do-step-loss`；循环 `metta.run` 同一 MeTTa 片段 10 次。
- **断言**：`losses[0] > losses[-1] + 0.01`。

## 摘要

非「torchme 沙箱」示例，而是 **hyperon↔torch 梯度完整性** 的回归测试；对 grounded 桥接质量有信号意义。
