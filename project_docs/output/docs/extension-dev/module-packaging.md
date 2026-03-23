---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 模块打包与发布

## Python 包布局

1. 在 **pip** 包内提供 **importable** 模块，例如 `my_ext/metta_plugin.py`。
2. 使用 `register_atoms` / `register_tokens` / `grounded` 导出注册函数。
3. 用户安装 **wheel** 后，`site-packages` 已在默认 `MeTTa` 构造时加入 **include path**，可通过 **文件路径** 或 `load_module_direct_from_pymod` 加载。

## 命名与冲突

- **MeTTa** 逻辑模块名与 **Python** 模块名可以不同；`load_module_direct_from_pymod("my-logical", "my_ext.metta_plugin")`。
- 避免多个文件模块使用相同 `metta_mod_name` 导致 `sys.modules` 碰撞（见源码 **TODO**）。

## 纯 **MeTTa** 资源

除 **Python** 外，可随包分发 `.metta` 文件，由 `import!` / `include` 解析；路径需落在工作目录或配置的 **include** 目录中。

## **Rust** / **C** 扩展

若扩展包含原生库：

- 遵循仓库 `python/install-hyperonc.sh` 与 **Conan** 工作流（见根 **README**）。
- **PyPI** 发布使用 **cibuildwheel**（`docs/DEVELOPMENT.md`）。

## 版本对齐

扩展应声明兼容的 `hyperon` **PyPI** 版本；**Breaking** 变更跟随仓库 `Cargo.toml` / `python/VERSION` 同步号。

## 检查清单

- [ ] `pytest` 覆盖加载与关键 **token**。
- [ ] 文档说明所需 `hyperon` 最低版本。
- [ ] 若依赖 **Git** 模块，说明 **OpenSSL** / **pkg_mgmt** 要求。
