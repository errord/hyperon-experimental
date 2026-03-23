---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# Rust Workspace 总览与 Crate 依赖

## Workspace 成员

根 `Cargo.toml` `[workspace].members`：

| Crate | 路径 | 角色 |
|-------|------|------|
| **hyperon-common** | `./hyperon-common` | 通用数据结构、字符串、集合、断言宏 |
| **hyperon-atom** | `./hyperon-atom` | **Atom** ADT、**Grounded**、**matcher**、序列化 |
| **hyperon-space** | `./hyperon-space` | **Space** **trait**、**GroundingSpace** 等 |
| **hyperon-macros** | `./hyperon-macros` | 过程宏（如 `expr!`） |
| **lib**（包名 **hyperon**） | `./lib` | **MeTTa** 解释器、**runner**、**stdlib**、文本前端 |
| **c** | `./c` | **C** API（**libhyperonc**） |
| **repl** | `./repl` | **Rust** **REPL** 二进制 |

**Resolver**：`"2"`。工作区包版本在 `[workspace.package] version = "0.2.10"` 统一声明。

## 依赖边（概念）

```
repl  ──depends on──► hyperon (lib)
c     ──depends on──► hyperon (lib)
lib   ──depends on──► hyperon-atom, hyperon-space, hyperon-common, hyperon-macros
hyperon-space ──► hyperon-atom, hyperon-common
hyperon-atom  ──► hyperon-common
```

（具体 `Cargo.toml` 以各 crate 为准；上图为架构直觉。）

## Workspace 依赖别名

`[workspace.dependencies]` 将路径依赖固定为同版本 **0.2.10**，供成员 crate 继承。

## **Python** 绑定

**Python** 包通过 **hyperonpy** 链接 **C** API；**C** 头文件由 **cbindgen** 从 **lib** / **c** 生成，构建流程见根 **README**。

## 特性（Features）

**lib** 上常见可选特性包括 **pkg_mgmt**（`register-module!` / `git-module!`）等；构建 **Python** **wheel** 时由脚本选择特性集合。

## 版本对齐

发布时同步：

- 根 `Cargo.toml` `workspace.package.version`
- `[workspace.dependencies]` 中 `hyperon*` 版本
- `python/VERSION`

详见 `docs/DEVELOPMENT.md`。
