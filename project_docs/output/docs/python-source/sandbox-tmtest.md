---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# tm_test.py（沙箱）

## 文件角色

**PyTorch 模型与训练脚手架**：示例 `nn.Module`（`FooModel`、MNIST 风格 `NeuralNetwork`）及 `Trainer`（train/test 循环），供沙箱实验或手动测试引用，**非 MeTTa 注册代码**。

## 关键特性与集成

- **依赖**：`torch`、`torch.nn`。
- **Trainer**：CUDA/CPU、CrossEntropy 风格训练步骤、周期性打印 loss；`test` 计算准确率。
- **Foo**：简单占位类（三个可选构造参数）。

## 摘要

纯 Python 侧深度学习小例子集合，与 `torchme` 无直接导入关系；用于快速验证张量/训练流程的实验文件。
