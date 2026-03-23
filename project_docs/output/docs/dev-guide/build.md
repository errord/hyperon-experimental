---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 构建流程

## **Rust** 库与 **REPL**

在仓库根目录：

```bash
cargo build
cargo build -p repl
```

运行测试：

```bash
cargo test
```

## **C** API

**lib** crate 生成 **libhyperonc**；具体 **CMake** 调用见 `c/` 目录与 **CI** 工作流。

## **Python** 包（可编辑安装）

在配置好 **Conan** 与 **cbindgen** 后：

```bash
cd python
pip install -e .
```

或运行仓库提供的安装脚本（见 `python/install-hyperonc.sh`）以从 **Git** 获取指定提交的库。

## **Docker**

```bash
docker build -t trueagi/hyperon .
```

`--target build` 保留完整构建环境便于调试。

## 特性标志（**Rust**）

部分功能（如 **pkg_mgmt**）由 **Cargo features** 控制；默认 **CI** 配置见 `.github/workflows`。

## 常见问题

- **找不到 hyperonpy**：先完成 **Python** 扩展编译与 `pip install -e .`。
- **Conan** 配置缺失：执行 `conan profile detect --force`。
- 版本不一致：同步 `Cargo.toml` `workspace.package.version` 与 `python/VERSION`。

## 发布（维护者）

见仓库 `docs/DEVELOPMENT.md`：**cibuildwheel**、**Test PyPi** 流程与版本号三处更新。
