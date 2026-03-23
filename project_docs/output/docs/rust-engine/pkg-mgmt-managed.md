---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# 包管理：`pkg_mgmt/managed_catalog.rs`

## 文件角色

定义**可管理的本地目录**抽象与默认实现 **`LocalCatalog`**：在磁盘上缓存上游 `ModuleCatalog` 提供的模块，维护 TOC（按模块名索引的 `ModuleDescriptor` 集合），并支持 `clear_all` / `fetch` / `remove` / 增强版 `fetch_newest_for_all`（按上游每个 `(name, uid)` 取最新再拉取）。与 `UpdateMode` 组合控制是否克隆、是否强制最新等。

## 公开 API

| 项 | 说明 |
|----|------|
| **`UpdateMode`** | `FetchIfMissing`、`TryFetchIfOlderThan(u64)`、`TryFetchLatest`、`FetchLatest`；`promote_to` 取更「激进」的拉取策略。 |
| **`ManagedCatalog`** trait | 继承 `ModuleCatalog`；`clear_all`、`fetch`、`remove`、默认 `fetch_newest_for_all`（先 `sync_toc` 再按名拉最新）。 |
| **`LocalCatalog`** | `new(caches_dir, name)`、`push_upstream_catalog`；`loader_for_explicit_git_module`（需上游含 `GitCatalog`）供 `resolve_module` 在 pkg-info Git 依赖时使用。 |

`dir_name_from_descriptor`、`parse_descriptor_from_dir_name` 为 `pub(crate)`，与缓存目录命名约定对应。

## 核心结构体

- **`LocalCatalog`**：`name`、`upstream_catalogs`、`storage_dir`、`Mutex<LocalCatalogTOC>`；`lookup` 先查 TOC，再顺序查上游；`get_loader` 默认 `FetchIfMissing`。
- **`LocalCatalogTOC`**：`BTreeMap<String, Vec<ModuleDescriptor>>`，从缓存目录扫描构建，忽略 `_catalog.repo`、`_catalog.json` 及点开头的条目。
- **`LocalCatalogLoader`（私有）**：包装 `upstream_loader`，在 `prepare` 中将 `update_mode` 与本地缓存目录结合，调用上游 `prepare`；`load` 为 `unreachable!`（由 prepare 替换实际 loader）。

## `ModuleLoader` 实现

**`LocalCatalogLoader`**

- `prepare`：`update_mode.promote_to` 后与 `local_cache_dir` 一并交给 `upstream_loader.prepare`。
- `load`：不应被直接调用。

## 小结

`managed_catalog.rs` 把 **「远程/上游目录 + 本地镜像」** 产品化：`LocalCatalog` 既是 `ModuleCatalog` 又是 `ManagedCatalog`，是 MeTTa `catalog-update!` / `catalog-clear!` 等操作的 Rust 侧承载；注释中坦诚 `fetch_newest_for_all` 在删除旧版本与需求求解上的局限，并指向未来 Requirement API。
