---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# PyTorch 实验（sandbox）

## 位置

主要代码在 `python/sandbox/pytorch/`（如 `torchme.py`、`tm_test.py`、`kwargsme.py` 等）；集成 smoke 测试见 `python/integration/test_torch.py`。

## 目的

验证 **Grounded** 操作包装 **Tensor**、自定义 **grad** 钩子、或与 **jetta** / **PLN** 类工作流结合的可行性。**Sandbox** 代码**不保证** API 稳定。

## 运行注意

需单独安装 **torch**；版本与 **CUDA** 依本地环境而定。勿默认在 **CI** 全矩阵中启用重型 **GPU** 测试。

## 状态

属 **pre-alpha** 实验；合并主产品线前需重新设计类型桥接与错误语义。

## 参见

`others.md`、`../extension-dev/grounded-ops.md`
