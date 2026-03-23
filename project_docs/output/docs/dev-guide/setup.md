---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 环境搭建

## 操作系统

**Linux** 与 **macOS** 为首选；**Windows** 可用 **WSL2** 或按 **README** 配置 **MSVC** 工具链。

## 必备组件

| 组件 | 用途 |
|------|------|
| **Rust**（stable） | `lib`、`hyperon-*` crates |
| **Python 3.8+** 与 **pip** | **hyperonpy**、**pytest** |
| **CMake 3.24+** | **C** API 与 **Python** 扩展构建 |
| **GCC** / **Clang** | 原生链接 |
| **cbindgen** | 生成 **C** 头文件 |
| **Conan 2** | 部分依赖（版本见根 **README**） |

可选：**OpenSSL**、**Zlib**（**Git** 模块）、**Protobuf**（**DAS**）。

## 克隆与子模块

```bash
git clone https://github.com/trueagi-io/hyperon-experimental.git
cd hyperon-experimental
```

若仓库使用子模块，按官方说明 `git submodule update --init --recursive`。

## Python 虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
```

## Conan 与 **cbindgen**

```bash
pip install conan==2.19.1
conan profile detect --force
cargo install cbindgen
```

## 验证

构建成功后（见 `build.md`）：

```bash
cd python && pip install -e .
pytest tests/test_atom.py -q
```

## 编辑器

推荐安装 **rust-analyzer** 与 **Python** 语言支持；大型 crate 首次索引可能较慢。
