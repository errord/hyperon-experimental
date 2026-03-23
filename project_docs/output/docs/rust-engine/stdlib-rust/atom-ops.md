---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `stdlib/atom.rs` — 原子列表、类型与元类型运算

## 文件职责

在 **表达式（子项列表）** 上提供集合式操作（唯一、并、交、差）、数值聚合（min/max）、尺寸与索引；并提供从 **类型空间** 查询原子类型及 **元类型**（Symbol / Expression / Grounded 等）的 grounded 算子。`car-atom` / `cdr-atom` / `filter-atom` / `map-atom` / `foldl-atom` 等在本文件测试中引用，其实现主要在 `stdlib.metta` 或其它层组合上述原语。

## 接地运算一览

| MeTTa 名 | Rust 类型 | 类型签名（语义） | 行为摘要 |
|----------|-----------|------------------|----------|
| `unique-atom` | `UniqueAtomOp` | `Expression → Atom` | 按 `atoms_are_equivalent` 去重，保序 |
| `union-atom` | `UnionAtomOp` | `Expression → Expression → Atom` | 两列表拼接（不去重） |
| `intersection-atom` | `IntersectionAtomOp` | `Expression → Expression → Atom` | 交；用 `MultiTrie` + `atom_to_trie_key` 索引；匹配时消耗 RHS 同键重复项 |
| `subtraction-atom` | `SubtractionAtomOp` | `Expression → Expression → Atom` | 差（类似 multiset 减法，基于同一 trie 机制） |
| `max-atom` | `MaxAtomOp` | `Undefined → Number` | 单参表达式内全是 `Number` 时取 max，结果为 `Float` |
| `min-atom` | `MinAtomOp` | 同上 | 取 min |
| `size-atom` | `SizeAtomOp` | `Expression → Number` | 子项个数 |
| `index-atom` | `IndexAtomOp` | `Expression → Number → Atom` | 按数值下标取子项，越界报错 |
| `get-type` | `GetTypeOp` | `Atom → Undefined`（可扩展第二参空间） | 默认用构造时注入的 `self.space`；若提供第二参且为 `DynSpace` 则用该空间。`get_atom_types` 过滤有效类型；全为错误类型时返回 `Empty` |
| `get-metatype` | `GetMetaTypeOp` | `Atom → Atom` | `get_meta_type(atom)` |
| `get-type-space` | `GetTypeSpaceOp` | `Space → Atom → Atom` | 在显式空间中查询类型，规则同 `get-type` |

**上下文**：`get-type` 在 `register_context_dependent_tokens` 中绑定当前模块空间。

## 核心结构体与辅助逻辑

| 名称 | 说明 |
|------|------|
| `GetTypeOp` | 持有 `DynSpace`，支持可选第二参覆盖空间 |
| `UniqueAtomOp` / `UnionAtomOp` / … | 无状态 |
| `atom_to_trie_key` | 将原子编码为 `TrieKey<SymbolAtom>`：符号精确、表达式结构化为左右括号序列、部分 grounded 用序列化哈希、变量等为通配 |

## `CustomExecute` 要点

- **交 / 差** 依赖 `MultiTrie` 与 `atom_to_trie_key`：对 grounded 无 `as_match` 时尝试 `serialize` 哈希，否则通配；与 **精确 multiset 语义** 相关（重复元素可逐个匹配消耗）。
- **`get-type`**：与类型系统模块 `get_atom_types`、`AtomType::is_valid` / `is_error` 集成；多类型原子返回多个结果原子。

## 与 MeTTa 语义的对应关系

- **列表级原语**：MeTTa 中常把“非确定性结果集”或元组式数据建模为 **表达式子项**；`union`/`intersection`/`unique` 等对应集合与多重集层面的代数。
- **类型反射**：`get-type` / `get-type-space` 对应逻辑中 “查询 `:` 断言与类型推导结果”；`get-metatype` 对应 Atom ADT 层面的分类（符号、表达式、接地等）。
- **与高层 `map-atom` / `foldl-atom`**：测试展示其与 `eval`、`+` 等组合使用；列表遍历的通用折叠由 `core` 中 `_minimal-foldl-atom` 与 metta 定义协同完成。

## 小结

`atom.rs` 聚焦 **表达式作为列表** 的实用运算与 **类型/元类型内省**，是连接 Hyperon **类型系统** 与 **MeTTa 列表处理习惯** 的 Rust 接地层；交/差实现兼顾结构匹配与性能（Trie）。
