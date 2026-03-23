---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `stdlib/package.rs` — 包管理：本地路径与 Git 模块

## 文件职责

在启用 **`pkg_mgmt`** 特性时编译；向 Tokenizer 注册：

- **`register-module!`**：从 **文件系统路径** 加载模块（调用 `Metta::load_module_at_path`）。
- **`git-module!`**：从 **Git URL** 解析模块名，经环境 **catalog / 缓存** 配置获取或拉取模块（`ModuleGitLocation`、`UpdateMode::TryFetchLatest` 等）。

## 接地运算一览

| MeTTa 名 | Rust 类型 | 类型签名 | 行为摘要 |
|----------|-----------|----------|----------|
| `register-module!` | `RegisterModuleOp` | `Atom → Unit` | 参为类字符串原子 → `PathBuf` → `load_module_at_path(path, None)` |
| `git-module!` | `GitModuleOp` | `Atom → Unit` | URL 字符串 → `mod_name_from_url` → 通过 `specified_mods.loader_for_explicit_git_module` 与 `get_or_init_module_with_descriptor` 安装；无缓存目录时报错 |

## 核心结构体

| 结构体 | 持有数据 |
|--------|----------|
| `RegisterModuleOp` | `Metta` |
| `GitModuleOp` | 与 `module.rs` 相同的 `RunContext` 栈 `Arc<Mutex<...>>` hack |

## `CustomExecute` 要点

- **`register-module!`**：路径由 **`expect_string_like_atom`** 提取；错误经 `ExecError::from` 传播。
- **`git-module!`**：依赖 **`environment().specified_mods`**；注释说明 **无 git 编译** 时仍可能从 **已有缓存** 加载，但 **克隆/拉取** 需要 git 支持。

## 与 MeTTa 语义的对应关系

- 将 **宿主文件系统与远程依赖** 暴露为 MeTTa 级 **副作用原语**，与 `import!` 配合完成“注册 → 导入”工作流。
- 模块名从 URL **推导**（`mod_name_from_url`），未来可扩展可选分支名、显式模块名等（TODO 注释）。

## 小结

`package.rs` 体量小，专责 **模块发现与获取** 的两种来源：**本地路径** 与 **Git**；与 `module.rs` 的 **符号与空间导入** 互补，共同支撑 Hyperon 的 **可分发模块生态**（受特性与运行环境配置约束）。
