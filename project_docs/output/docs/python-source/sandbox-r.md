---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# r.py（沙箱）

## 文件角色

演示 **用 grounded `MeTTa` runner 替代 `(import! r r.metta)`**：内嵌 MeTTa 源码字符串，构造 `MeTTaC`（`copy` 返回自身），`run` 后把整实例作为 `G(runner, AtomType.ATOM)` 注册为原子 **`r`**。

## 关键特性与集成

- **register_atoms**：仅返回 `{'r': runnerAtom}`。
- **内容示例**：阶乘、`match &self`、`call_func` 等snippet。
- **意图**：展示在 `extend-py` 中嵌入 `import` 的一种方式。

## 摘要

教学/实验用小扩展；与 `resolve.py` 的「命名 runner」思路可组合，非仓库核心 API。
