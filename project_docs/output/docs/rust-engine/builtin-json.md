---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# 内置模块：`builtin_mods/json.rs`

## 文件角色

实现 MeTTa 内置模块 **`json`**：在 Atom 与 JSON 字符串之间双向转换，支持数字、布尔、字符串、列表（表达式）、字典空间（`DynSpace` 内键值对）、符号与变量（通过前缀编码）、以及 `null` 符号特例。

## 公开 API

| 项 | 说明 |
|----|------|
| `pub static JSON_METTA` | `include_str!("json.metta")`。 |
| MeTTa 操作名 | `json-encode`：`Atom -> String`；`json-decode`：`String -> Atom`。 |

`JsonModLoader` 为 `pub(crate)`。内部 `JSONError` 及 `encode_*` / `decode_*` 为私有实现细节。

## 核心结构体

- **`JsonModLoader`**：唯一对外加载器类型（crate 内）。
- **编码约定**：普通符号编码为 JSON 字符串 `"sym!:name"`，变量为 `"var!:name"`；JSON `null` 与 MeTTa 符号 `null` 互相对应；`DynSpace` 遍历要求子项为二元表达式 `(StringKey value)`，否则报错。

## `ModuleLoader` 实现

**`JsonModLoader`**

- `load`：`GroundingSpace::new()` → `init_self_module` → `load_tokens` → `JSON_METTA` 解析器。
- `load_tokens`：注册 `json-encode`、`json-decode` 两个 `GroundedFunctionAtom`。

## 小结

该模块桥接 **serde_json** 与 Hyperon 的 **Atom 模型**：对象解码为带 `DynSpace` 的 grounded space，数组解码为表达式列表。解码时对 `sym!:`/`var!:` 的识别依赖 `Value::String` 经 `to_string()` 后的前缀判断；`u64` 数字明确不支持。可选 `benchmark` feature 下含 `json_encode` 基准测试。
