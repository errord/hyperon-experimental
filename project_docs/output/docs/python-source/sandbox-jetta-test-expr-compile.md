---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/sandbox/jetta/test_expr_compile.metta"
---

# sandbox：jetta compile 表达式

**角色**：`compile` 按名字或函数原子注册到 jetta 空间。  
**要点**：`compile &jspace "boo"`、`compile &jspace my-goo 2`、`boo-gnd`、`JettaCompileError`。  
**概要**：字符串名与带元数的形式；本地与 jetta 双侧求值一致；非法 compile 参数触发错误串匹配。
