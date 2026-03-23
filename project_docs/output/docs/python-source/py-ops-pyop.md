---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `py_ops/pyop.py` 分析报告

## 文件角色

为 MeTTa 提供**字面量词法**与**算术/布尔运算**的 Python 扩展：通过 `@register_tokens` / `@register_atoms` 向解释器注册，使脚本可直接使用常见数字、布尔、字符串及中缀运算符。

## 公开 API

| 符号 | 装饰器 | 作用 |
|------|--------|------|
| `arithm_types` | `@register_tokens` | 返回正则 → 词法回调字典，将 `True`/`False`、整数/浮点/科学计数、双引号字符串转为带类型的 `ValueAtom` |
| `arithm_ops` | `@register_atoms` | 返回 `+ - * / %` 对应的 `OperationAtom`，底层为 Python 算术（类型注释中的 `Number` 约束已注释掉，便于重载到非纯数字） |
| `bool_ops` | `@register_atoms` | 返回比较与逻辑运算：`> < >= <= or and not` |

## 核心类

无独立类；使用 `hyperon` 的 `ValueAtom`、`OperationAtom`。

## 小结

实现最小可用的「类脚本」算术与布尔字面量/运算符桥接；设计上刻意弱化静态类型标注，以便将来对非 `Number`/`Bool` 对象做运算重载。
