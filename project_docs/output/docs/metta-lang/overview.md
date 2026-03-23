---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# MeTTa 语言概述

MeTTa（Meta Type Talk）是 Hyperon 中的核心表面语言，用于在 **Atom** 层面表达知识、规则与计算。本文从实现与使用角度概括其概念模型；更细的教程见同目录下的 `tutorial/`。

## 原子模型（Atom model）

程序与数据统一为 **Atom**，常见形态包括：

- **Symbol**：具名概念，例如 `foo`。
- **Variable**：可匹配、可绑定的占位符，例如 `$x`。
- **Expression**：由子 Atom 构成的复合结构，例如 `(+ 1 2)`。
- **GroundedAtom**：承载宿主运行时值或行为（Python / Rust 对象、**Space** 引用、内置 **Operation** 等）。

Python 中可通过 `S` / `V` / `E` / `G` 等构造器建立对应 Atom；引擎在 **C API** 与 **Rust** 核心中持有等价表示。

## 原子空间（Atom Space）

**Space** 是 Atom 的容器与查询接口。**GroundingSpace** 是最常用的具体空间：支持 `add` / `remove` / `replace` 与基于模式的 **query**。  
MeTTa 程序通过 `match`、模块空间、`&self` 等机制与当前 **Space** 交互；也可嵌入自定义 **Space**（见扩展开发文档）。

## 求值模型（Evaluation model）

顶层执行由 **MeTTa runner** 驱动：解析 S-表达式、结合 **Tokenizer** 得到 Atom 流，再在空间与规则上进行归约（reduction）。

- 表达式通常按“可约则约”的方式展开；**Grounded** 上的 **execute** 与纯规则（如 `=` 定义）共同参与。
- **非确定性**：多个可归约分支可同时存在；`superpose`、`collapse` 等与 **Bindings** 组合用于枚举与收束结果（详见 `nondeterminism.md`）。

## Grounding 机制（Grounding）

**Grounding** 把符号层与宿主层连接起来：

- **GroundedAtom** 可携带值、可匹配、可执行（**OperationObject** 等）。
- **Tokenizer** 将字面量（数字、字符串、`True`/`False` 等）解析为 **Grounded** 或符号。
- Python 侧可用 `OperationAtom`、`@grounded`、`register_atoms` / `register_tokens` 注册自定义操作与词法规则。

## 模块系统（Module system）

模块提供独立的 **Space**、**Tokenizer** 与加载逻辑。典型能力包括：

- `import!`、`include`：按路径或名称加载 **MeTTa** / 资源文件。
- `bind!`：将名称绑定到当前模块空间中的 Atom。
- `mod-space!`、`print-mods!`： introspection 与调试。
- Python 包可通过 `hyperon.exts`、**site-packages** 路径与文件系统格式加载为 **MeTTa module**（见 `module-packaging.md`）。

## 状态管理（State）

标准库提供基于 **Space** 的 **state** 操作（如 `change-state!`、`get-state`），用于在求值过程中读写命名状态，与纯规则组合使用。详见教程中 **state** 相关章节与 `stdlib-reference.md`。

## 标准库（Standard library）

核心 **stdlib** 由两部分构成：

1. **Rust** 注册的 **grounded operations**（算术、`match`、`superpose`、空间操作、类型查询、`pragma!` 等）。
2. 内嵌 **stdlib.metta**：在 **MeTTa** 中定义的规则与辅助函数（如 `collapse`、`chain` 族、`if` 等）。

Python 发行版还会加载 `hyperon.stdlib` 中的附加 **grounded** 与 **token**（如 `repr` / `parse`）。完整列表见 `stdlib-reference.md`。

## 延伸阅读

- 语言形状与语义要点：`specification.md`
- 内置操作手册：`stdlib-reference.md`
- 非确定性：`nondeterminism.md`
- **Rust** 工作区：`../rust-engine/workspace-overview.md`
