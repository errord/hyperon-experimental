---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `c/src/module.rs` 分析报告

## 文件角色

模块系统的 C 插件面：`ModuleLoader` 的 C 实现（`module_loader_t`）、`ModuleDescriptor`、`ModId` 的 C 封装，以及文件系统模块格式 `fs_module_format_t` 与 `FsModuleFormat` trait 的对接。

## FFI 类型映射

| 类型 | 说明 |
|------|------|
| `module_loader_t` | `load` / `load_tokens` / `to_string` / `free`；错误通过 `write_t` 写 UTF-8 文本，返回码 0 成功 |
| `CModuleLoader` | `Send + Sync`（`unsafe impl`，注释讨论重入性）；`Drop` 调可选 `free` |
| `metta_mod_ref_t` | 装箱 `&MettaMod` 指针，供 `load_tokens` 目标模块引用 |
| `module_descriptor_t` | `Box<ModuleDescriptor>`，`module_descriptor_free` 释放 |
| `module_id_t` | `usize` 镜像 `ModId`，**无需 free** |
| `fs_module_format_t` | `path_for_name` 写缓冲区；`try_path` 输出 `module_loader_t*` 与 `module_descriptor_t`；可选 `free` 释放格式插件状态 |

## 内存与所有权

- `CModuleLoader::new` 要求非空 loader 指针；Rust 侧 `load` 将 `RunContext` 转为 `run_context_t` 传入 C。  
- `try_path` 成功时 `mod_descriptor` 被 `into_inner` 取走；loader 指针交给 `CModuleLoader` 拥有语义由 C 侧约定。  
- `CFsModuleFormat::drop` 调格式表的 `free`；注释强调多线程重入需 C 端自理。

## 小结

模块加载错误路径部分仍待把字符串传回 `metta_err_str`（`run_context_load_module` TODO）。`fs_module_format_t` 与 Hyperon 包管理遍历目录、`try_path` 流程紧耦合。
