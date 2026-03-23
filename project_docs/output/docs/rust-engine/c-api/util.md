---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `c/src/util.rs` 分析报告

## 文件角色

C/Rust 互操作共用工具：C 字符串与 Rust `str`/`String` 转换、向调用方缓冲区格式化写入、以及 `write_t` / `CWrite` 供 C 回调向 Rust `fmt::Write` 汇报错误。

## FFI 与内存

| API | 行为 |
|-----|------|
| `cstr_as_str` | `CStr::from_ptr` → `&str`，非法 UTF-8 则 panic |
| `cstr_into_string` | 分配 `String` |
| `str_as_cstr` / `string_as_cstr` | 分配 `CString`（含内嵌 `\0` 会 panic） |
| `write_into_buf` | `buf_len==0` 时只算长度；否则写入并补 `\0`；不足长则返回所需长度供重试 |
| `write_debug_into_buf` | `Debug` 经适配为 `Display` 再写入缓冲区 |
| `log_error` / `log_warn` / `log_info` | 经 `log` crate 输出 |
| `write_t` | 不透明句柄，实为 `*mut CWrite` |
| `write_str` | C 调 Rust：把 UTF-8 片段写入 `CWrite`，累计 `fmt::Result` |

## 小结

几乎所有「把对象渲染进调用方缓冲区」的 C API 都依赖 `write_into_buf`；`CWrite` 是模块加载等场景下 C 向 Rust 传错的轻量管道，无额外堆分配（除 `CString` 路径外）。
