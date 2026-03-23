---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# c/conanfile.py

## 文件角色

**C 库（hyperonc）** 的 **Conan 2** 配方：`HyperoncRecipe` 管理单元测试框架等依赖。

## 关键特性与集成

- **requires**：`libcheck/0.15.2`；Windows 额外 `openssl/3.4.1`。
- **configure**：`libcheck` 选项 `with_subunit = False`。
- **layout**：`cmake_layout`。

## 摘要

C 侧测试与构建的依赖锁定；与 Python 配方分离，各司其职。
