---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# 内置模块：`builtin_mods/fileio.rs`

## 文件角色

实现 MeTTa 内置模块 **`fileio`**：在 MeTTa 中通过 grounded 文件句柄操作本地文件（打开、读字符串、写、定位、定长读、取大小），并嵌入 `fileio.metta`。

## 公开 API

| 项 | 说明 |
|----|------|
| `pub static FILEIO_METTA` | `include_str!("fileio.metta")`。 |
| `pub const ATOM_TYPE_FILE_HANDLE` | 类型原子 `FileHandle`。 |
| `pub struct FileHandle` | 包装 `Rc<RefCell<std::fs::File>>`，实现 `Grounded`、`Display`、`PartialEq`（指针相等）。 |

Tokenizer 函数：`file-open!`、`file-read-to-string!`、`file-write!`、`file-seek!`、`file-read-exact!`、`file-get-size!`。

## 核心结构体

- **`FileHandle`**：`open(path, options)` 根据选项字符串解析 `OpenOptions`（`r`/`w`/`c`/`a`/`t` 等字符子串）；`read_to_string`、`write`、`seek`、`read_exact`（读字节再 UTF-8 解码）、`get_size`（metadata 长度）。
- **`FileioModLoader`**：`ModuleLoader`，使用 `DynSpace::new(GroundingSpace::new())` 初始化模块空间。

## `ModuleLoader` 实现

**`FileioModLoader`**

- `load`：`DynSpace` + `init_self_module` → `load_tokens` → 压入 `FILEIO_METTA`。
- `load_tokens`：注册六个 `GroundedFunctionAtom`。

注意：`file_write` 在写成功后对 `expect` 使用 `unit_result()` 路径混合；`file_seek` 对 `seek` 结果未完整传播错误（实现上以 `let _ =` 忽略部分结果），与 `read_to_string` 等路径的错误处理风格不完全一致。

## 小结

`fileio` 把 **std::fs 文件 I/O** 以句柄值模型暴露给 MeTTa，适合脚本化读写；选项字符串约定需与 MeTTa 层文档一致。集成测试通过临时文件验证读写与 seek 行为。
