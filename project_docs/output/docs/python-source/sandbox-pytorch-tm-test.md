---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/sandbox/pytorch/tm_test.metta"
---

# sandbox：torchme

**角色**：`torchme` 张量、autograd、模块实例化与训练管线草稿。  
**要点**：`torch:tensor`、`matmul`、`backward`、`instantiate_module`、`kwargs`、`Trainer`（`run_trainer` 注释掉）。  
**概要**：覆盖创建/运算/直方图/组合；`requires_grad` 链；`FooModel`/`NeuralNetwork`/`FashionMNIST` 等；演示 kwargs 需位置参数也写入 kwargs 的注意事项。
