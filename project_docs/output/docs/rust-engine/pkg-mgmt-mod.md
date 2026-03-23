---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# 包管理子系统入口：`pkg_mgmt/mod.rs`

## 文件角色

作为 **`crate::metta::runner::pkg_mgmt`** 的**桶文件（barrel module）**：声明子模块并通过 `pub use` 将 `catalog` 与 `managed_catalog` 的公开项重新导出，便于外部以 `pkg_mgmt::*` 引用；`git_cache` 与 `git_catalog` 为 `pub(crate)`，仅库内使用。

## 公开 API

| 项 | 说明 |
|----|------|
| `pub use catalog::*` | 导出 `ModuleCatalog`、`PkgInfo`、`DepEntry`、`ModuleDescriptor`、`resolve_module`、`DirCatalog`、`FsModuleFormat`、单文件/目录模块加载器等（以 `catalog.rs` 实际 `pub` 为准）。 |
| `pub use managed_catalog::*` | 导出 `UpdateMode`、`ManagedCatalog`、`LocalCatalog` 等。 |

本文件**不新增**类型或函数。

## 核心结构体

无；结构体定义在子模块中。

## `ModuleLoader` 实现

本文件**不实现** `ModuleLoader`。相关实现位于：

- `catalog.rs`：`SingleFileModule`、`DirModule` 等；
- `managed_catalog.rs`：`LocalCatalogLoader`；
- `git_catalog.rs`：`GitModLoader`。

## 小结

`pkg_mgmt/mod.rs` 负责**模块边界与可见性**：对外聚合「目录解析 + 本地托管目录 + Git 目录实现」的公共表面，同时隐藏 `git_*` 实现细节于 crate 内部，减少 `runner` 其他子模块的 `use` 路径长度。
