---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# 内置模块入口：`builtin_mods/mod.rs`

## 文件角色

作为 MeTTa Runner 的**内置模块聚合入口**：声明子模块、按特性（feature）条件编译导出部分子模块，并在运行时初始化阶段通过 `Metta::load_module_direct` 将各内置 `ModuleLoader` 注册到解释器。**不自动 `import`**，用户需在 MeTTa 中显式 `import!`。

## 公开 API

| 项 | 说明 |
|----|------|
| `pub fn load_builtin_mods(metta: &Metta) -> Result<(), String>` | 依次加载：`random`、`skel`、`fileio`、`json`；若启用 `pkg_mgmt` 则加载 `catalog`；若启用 `das` 则加载 `das`。失败时返回带前缀信息的 `String` 错误（部分错误文案仍写为 `"catalog"`，属历史笔误）。 |
| `#[cfg(feature = "pkg_mgmt")] pub mod catalog` | 包管理相关内置 MeTTa 接口。 |
| `#[cfg(feature = "das")] pub mod das` | 分布式原子空间（DAS）相关内置模块。 |

子模块 `skel`、`fileio`、`random`、`json` 为 `mod` 级私有，仅由此文件驱动加载。

## 核心结构体

本文件**不定义**业务结构体；仅组织子模块与加载顺序。

## `ModuleLoader` 实现

本文件**不实现** `ModuleLoader`。实现分布在：

- `random::RandomModLoader`
- `skel::SkelModLoader`
- `fileio::FileioModLoader`
- `json::JsonModLoader`
- （`pkg_mgmt`）`catalog::CatalogModLoader`
- （`das`）`das::DasModLoader`

## 小结

`builtin_mods/mod.rs` 是内置能力与 MeTTa 运行时的**接线板**：统一在初始化时注册模块名与对应 Loader，并通过 feature 控制可选子系统（目录型 catalog、DAS），保持核心路径精简、可选依赖隔离。
