---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# parse_torch_func_signatures.py（沙箱）

## 文件角色

**一次性/维护用脚本**：遍历 `torch` 与 `torch.Tensor` 的公开属性，从 `__doc__` 用正则抽取参数块与返回类型，生成 **`torch_func_signatures.json`** 供 `torchme.py` 加载。

## 关键特性与集成

- **extract_signature**：匹配 `Arguments`/`Args`/`Keyword args` 等段，解析每行参数名与说明，读取 `->` 返回类型。
- **输出路径**：常量 `TORCH_FUNC_SIGNATURES_SAVE_PATH`（可按环境修改）。
- **依赖**：`torch`、`json`、`re`；无 MeTTa 运行时依赖。

## 摘要

绕过 `inspect` 对内置/C 函数签名的限制，以文档为源的脆弱但实用的签名抓取工具；与 torch 版本文档格式强相关，属实验管线一环。
