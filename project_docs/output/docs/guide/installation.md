---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 安装指南

## PyPI（推荐）

```bash
python3 -m pip install hyperon
```

若遇 `externally-managed-environment`（如新版 Linux 发行版），请先创建 **venv** / **virtualenv** / **conda** 环境，或使用发行版文档允许的 **pip** 标志。

安装后可用 **REPL**：

```bash
metta-py
```

## Docker

```bash
docker run -ti trueagi/hyperon:latest
```

容器内同样可使用 `metta-py`；部分镜像亦提供 **Rust** `metta-repl`。

## 从源码构建（开发者）

需要 **Rust**、**Python 3.8+**、**CMake**、**GCC**、**cbindgen**、**Conan** 等。概要步骤：

1. 安装 **Rust** 与 **cargo**。
2. `cargo install cbindgen`
3. `pip install conan==2.19.1 && conan profile detect --force`
4. 按仓库根目录 `README.md` 构建 **libhyperonc** 与 **Python** 扩展。

详细命令与故障排除见 `../dev-guide/setup.md` 与官方 **README**。

## 版本

本文档对应 **Hyperon** **0.2.10**；**PyPI** 上的 `hyperon` 包版本号应与之一致或兼容。
