---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# kwargsme.py（沙箱）

## 文件角色

为 MeTTa 提供 **`Kwargs` 可匹配对象** 与 **`pairs_to_kwargs` 操作**，把「键值对列表」表达式转成 Python 字典式 kwargs，供 `torchme` 等扩展消费。

## 关键特性与集成

- **Kwargs**：`MatchableObject` 子类，`match_` 针对 `(key $var)` 形式从 `content` 字典绑定变量。
- **pairs_to_kwargs**：遍历子表达式，键为 `SymbolAtom`，值为 grounded 的 `.value`、`None` 或符号名。
- **依赖**：仅 `hyperon.atoms`。

## 摘要

轻量辅助模块，承担 MeTTa 语法层「命名参数包」与 Python `**kwargs` 之间的胶水；实验性质，与 PyTorch 沙箱配套。
