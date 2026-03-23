---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# python/conanfile.py

## 文件角色

**hyperonpy** 的 **Conan 2** 配方：`HyperonpyRecipe` 声明 CMake 生成器与第三方依赖，供 Python 绑定（pybind11）构建使用。

## 关键特性与集成

- **requires**：`optional-lite/3.5.0`、`pybind11/2.10.1`；Windows 额外 `openssl/3.4.1`。
- **layout**：`cmake_layout`。
- **settings**：os、compiler、build_type、arch。

## 摘要

构建系统片段，非运行时逻辑；与 CMake 工具链一致即可复现依赖环境。
