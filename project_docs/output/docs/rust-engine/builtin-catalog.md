---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# 内置模块：`builtin_mods/catalog.rs`

## 文件角色

在启用 **`pkg_mgmt`** 时提供 MeTTa 内置模块 **`catalog`**：把运行环境中的模块目录（`ModuleCatalog` / `ManagedCatalog`）以少量命令暴露给 MeTTa——列出、全量更新、清空本地托管缓存。文件顶部长注释讨论未来 API 与「已安装」语义。

## 公开 API

| 项 | 说明 |
|----|------|
| `pub static CATALOG_METTA` | 嵌入的 MeTTa 源码。 |
| `pub struct CatalogListOp` | `grounded_op!`，MeTTa 名 `catalog-list!`。 |
| `pub struct CatalogUpdateOp` | `catalog-update!`。 |
| `pub struct CatalogClearOp` | `catalog-clear!`。 |

各 `Op::new(metta: Metta)` 供加载时构造。执行语义：第一个参数为**符号**目录名，或 `all`，或 `specified-mods`（环境里的 `specified_mods`）。

## 核心结构体

- **`CatalogModLoader`**：`pub(crate)`，`ModuleLoader`。
- **`CatalogListOp` / `CatalogUpdateOp` / `CatalogClearOp`**：持 `Metta`，通过 `CustomExecute::execute` 访问 `metta.environment().catalogs()` 与可选 `specified_mods`；列表/更新/清空分别调用 `list()`、`fetch_newest_for_all(UpdateMode::FetchLatest)`、`clear_all()`（仅对支持 `ManagedCatalog` 的项）。

## `ModuleLoader` 实现

**`CatalogModLoader`**

- `load`：空 `GroundingSpace` → `init_self_module` → `load_tokens` → `CATALOG_METTA`。
- `load_tokens`：用 `regex` 注册三个 grounded op token，闭包捕获 `Metta` 克隆。

## 小结

该模块是 **包管理子系统面向 MeTTa 的薄封装**：当前结果多通过 **println! 打印到 stdout**，返回 `unit_result()`；类型签名中已 TODO 未来改为返回原子列表。与 `pkg_mgmt::managed_catalog::UpdateMode`、`ManagedCatalog` 紧密耦合。
