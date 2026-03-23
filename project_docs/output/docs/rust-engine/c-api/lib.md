---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `c/src/lib.rs` 分析报告

## 文件角色

Hyperon C API 的 crate 根：仅声明子模块，无独立 FFI 符号。实际导出由各子模块的 `#[no_mangle] pub extern "C"` 条目经 cbindgen 等生成头文件。

## 模块划分

- `util`：字符串缓冲区、`CStr`/`CString` 辅助、日志与 `write_t` 桥接  
- `atom`：原子、grounded、向量、绑定与匹配  
- `space`：`DynSpace` 句柄、C 实现空间、观察者  
- `metta`：分词器、解析器、解释器/Runner、环境构建、与 `module` 协同  
- `serial`：序列化回调表与结果枚举  
- `module`：模块加载器、描述符、文件格式插件  

## 小结

入口极薄；跨语言契约与内存约定分散在 `atom`/`space`/`metta`，阅读 FFI 应以子模块为准。
