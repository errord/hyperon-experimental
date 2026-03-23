---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# resolve.py（沙箱）

## 文件角色

**跨 Runner 符号解析**：`@register_tokens(pass_metta=True)` 注册形如 `runnerName::atomName` 的 token，在父 MeTTa 中解析子 runner 里的符号，并返回 **grounded 原子** 或包装为 **`OperationAtom`** 以便在表达式中调用。

## 关键特性与集成

- **hyperonpy**：`hp.metta_evaluate_atom(runner.cmetta, expr.catom)` 执行 `E(atom, *args)`。
- **实现细节**：通过 `metta.run('! ' + runner_name)` 取子 runner（hack）；注释承认应用 `run` 过重、待更好 tokenizer API。
- **限制**：TODO 嵌套模块、非 grounded 符号借类型为 op。

## 摘要

多 MeTTa 实例互操作的实验性词法扩展；依赖 C 扩展求值路径，适合研究模块化/嵌入场景。
