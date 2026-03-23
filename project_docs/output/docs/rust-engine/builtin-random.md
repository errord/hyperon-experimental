---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# 内置模块：`builtin_mods/random.rs`

## 文件角色

实现 MeTTa 内置模块 **`random`**：提供可 grounded 的随机数生成器、若干 Rust 侧原语函数，并嵌入 `random.metta` 作为模块 MeTTa 源码。用于可复现/可共享状态的随机抽样（通过 `Rc<RefCell<StdRng>>`）。

## 公开 API

| 项 | 说明 |
|----|------|
| `pub static RANDOM_METTA` | `include_str!("random.metta")`，模块 MeTTa 程序体。 |
| `pub const ATOM_TYPE_RANDOM_GENERATOR` | 类型原子 `RandomGenerator`。 |
| `pub struct RandomGenerator` | 包装 `Rc<RefCell<StdRng>>`，实现 `Grounded`、`Display`、`PartialEq`（按内部指针比较）。 |

`RandomModLoader` 为 `pub(crate)`。

Tokenizer 注册的 grounded 函数（MeTTa 名）：`random-int`、`random-float`、`set-random-seed`、`new-random-generator`、`reset-random-generator`、`flip`；以及正则 token `&rng` → 默认 OS 种子生成器实例。

## 核心结构体

- **`RandomGenerator`**：构造方式包括 `from_os_rng`、`from_seed_u64`；`reseed_from_u64`、`reset`、`random_range`（委托 `rand`）。
- **`RandomModLoader`**：`ModuleLoader` 实现体，负责空间初始化、注册 token/函数、压入 `RANDOM_METTA` 解析器。

## `ModuleLoader` 实现

**`RandomModLoader`**

- `load`：`GroundingSpace::new()` → `init_self_module` → `load_tokens` → `SExprParser::new(RANDOM_METTA)` → `push_parser`。
- `load_tokens`：向模块 tokenizer 注册上述函数与 `&rng` token。

## 小结

该模块把 **Rust `rand` 的 `StdRng`** 暴露为 MeTTa 中的一等值，并支持种子与重置；代码注释提醒在 `rand` 极大范围下可能挂起，升级 `rand` 后需复查 `random-int`/`random-float`。测试覆盖 MeTTa 层与直接调用 `random_*` 辅助函数的路径。
