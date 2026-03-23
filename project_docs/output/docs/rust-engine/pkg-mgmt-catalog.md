---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# 包管理：`pkg_mgmt/catalog.rs`

## 文件角色

**模块解析与文件系统型目录**的核心实现：定义 `ModuleCatalog` trait（查找描述符、取 `ModuleLoader`、可选列举、`sync_toc`、`as_managed`）、`PkgInfo`/`DepEntry`（依赖、路径、Git 位置、版本约束）、**`resolve_module`** 主解析流程，以及单文件/目录模块格式、`DirCatalog`、`ModuleDescriptor` 与辅助函数。文件顶部 ASCII 图与大量注释说明 `import!` 解析策略与设计待定问题。

## 公开 API（节选）

- **`ModuleCatalog`**：`lookup*` 系列、`get_loader`、`list`/`list_names`/`list_name_uid_pairs`、`sync_toc`、`as_managed`、`as_any`；`dyn ModuleCatalog::downcast`。
- **`PkgInfo` / `DepEntry`**：serde 反序列化；`DepEntry` 内嵌 `ModuleGitLocation`（flatten）。
- **`ModuleDescriptor`**：名称、可选 `uid`、可选 `semver::Version`；`new`、`new_with_path_and_fmt_id`、`new_with_ident_bytes_and_fmt_id`、`uid_from_ident_bytes_and_fmt_id` 等。
- **`FsModuleFormat` / `SingleFileModuleFmt` / `DirModuleFmt`**：按名猜路径、`try_path` 识别模块。
- **`DirCatalog`**：在某目录下用格式列表发现模块。
- **`resolve_module`、`loader_for_module_at_path`**：`pub(crate)`，供 runner 导入链调用。
- **`mod_name_from_url`**：从 `.git` URL 推导合法模块名。

## 核心结构体

- **`SingleFileModule` / `DirModule`**：持 `PathBuf` 与 `PkgInfo`，负责 `init_self_module`、打开 `module.metta` 或单文件、暴露 `get_resource`（主源、版本字节等）。
- **`DirCatalog`**：`path` + `Arc<Vec<Box<dyn FsModuleFormat>>>`，`lookup` 通过 `visit_modules_in_dir_using_mod_formats` 收集描述符。

内部函数：`filter_by_version_req`、`find_newest_module`（无版本模块在「选最新」时的警告语义）。

## `ModuleLoader` 实现

1. **`SingleFileModule`**：`load` 从单 `.metta` 文件推 parser；`resource_dir` 为父目录。
2. **`DirModule`**：`load` 可选加载 `module.metta`；`resource_dir` 为模块根目录。
3. **测试用 `TestCatalog`**：`impl ModuleLoader for TestCatalog`（仅测试递归子模块导入）。

## 小结

`catalog.rs` 是 Hyperon **模块系统的「语言无关内核」**：把 PyPI/crates.io 式「目录」抽象为 `ModuleCatalog`，并与 semver、路径、Git 依赖声明衔接；`resolve_module` 串联 pkg-info、显式路径、Git、`strict` 标志、资源目录目录型 catalog 与环境 catalogs。体积大、注释多，是后续「依赖 sat 求解」等议题的主要落笔处。
