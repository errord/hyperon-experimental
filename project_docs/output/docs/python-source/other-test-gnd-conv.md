---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/sandbox/test_gnd_conv.metta"
---

# other：test_gnd_conv.metta

## 文件角色

**random 扩展**与 Rust/Python 布尔 grounded 值交互的简短回归（文件名含 gnd/conv 意涵：grounded 布尔在 `xor`/`and` 路径上的转换）。

## 关键原子/函数

- `import! &self random`
- `flip`、`xor`、`and`、字面 `True`

## 概要

断言 `xor (flip) (flip)`、`and (flip) (flip)`、`and (flip) True`、`xor True (flip)` 等可求值；注释指向 PR #597。全文件与布尔 grounded 互操作相关，非数值「转换」API 演示。
