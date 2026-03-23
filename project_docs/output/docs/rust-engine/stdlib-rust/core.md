---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `stdlib/core.rs` — 核心控制与原语级运算

## 文件职责

实现解释器控制、空间查询、非确定性展开辅助、以及部分与 `stdlib.metta` 协作的内部原语（如 `collapse` 相关、`foldl-atom` 的 Rust 递推核）。

## 接地运算（MeTTa token / 函数）一览

| MeTTa 名 / 注册名 | Rust 类型 | 类型签名（`Grounded::type_` 语义） | 行为摘要 |
|-------------------|-----------|-------------------------------------|----------|
| `pragma!` | `PragmaOp` | `Undefined` | 键值写入 `PragmaSettings`；对 `max-stack-depth` 校验无符号整数 |
| `nop` | `NopOp` | `Undefined` | 无操作，返回 `()` |
| `sealed` | `SealedOp` | `Expression → Atom → Atom` | 将表达式中未列入忽略列表的变量 `make_unique`，用于作用域/捕获语义 |
| `==` | `EqualOp` | `(t) (t) → Bool` | 两原子 `==` 比较，返回接地 `Bool` |
| `match` | `MatchOp` | `Space → Atom → Atom → Undefined` | 在空间上按模式查询，对每组绑定返回 `(template, bindings)` 流（见 `execute_bindings`） |
| `if-equal` | `IfEqualOp` | 四元 `Atom` → `Undefined` | `atoms_are_equivalent(atom, pattern)` 则选 then，否则 else |
| `superpose` | `SuperposeOp` | `Expression → Undefined` | 将单参表达式拆成子项列表，作为多结果返回 |
| `capture` | `CaptureOp` | `Atom → Atom` | 在当前空间与 pragma 下调用 `interpret` 子解释 |
| `_minimal-foldl-atom` | `MinimalFoldlAtomOp` | 六参（列表、初值、两变量、操作式、空间） | `foldl-atom` 的逐步展开核：空列表则 `return init`，否则生成 `chain`/`eval` 递归结构 |
| `_collapse-add-next-atom-from-collapse-bind-result` | `GroundedFunctionAtom`（自由函数） | `Expression → Expression → Atom` | 将 `(atom bindings)` 应用到列表表达式末尾，供 collapse 组合子使用 |

**注册上下文**：`pragma!`、`capture`、`_minimal-foldl-atom` 依赖当前 `Metta`/空间；其余多为上下文无关。

## 核心结构体

| 结构体 | 字段 / 要点 |
|--------|-------------|
| `PragmaOp` | `settings: PragmaSettings` |
| `CaptureOp` | `space: DynSpace`, `settings: PragmaSettings` |
| `NopOp` / `SealedOp` / `EqualOp` / `MatchOp` / `IfEqualOp` / `SuperposeOp` / `MinimalFoldlAtomOp` | 无状态单元结构体 |

辅助函数 `collapse_add_next_atom_from_collapse_bind_result`：配合 `apply_bindings_to_atom_move` 更新折叠列表。

## `CustomExecute` 要点

- **`MatchOp`**：实现 **`execute_bindings`**（非仅 `execute`），产出 `(模板, Option<Bindings>)` 迭代器，支撑多结果与变量绑定传播。
- **`MinimalFoldlAtomOp`**：用 `CachingMapper` 替换操作式中的累加变量与当前元素，并拼接 `CHAIN` / `METTA` / `EVAL` 原子，属于 **元循环展开** 而非直接数值折叠。
- **`SealedOp`**：基于 `HashSet` 记录忽略变量，对其余变量就地 `make_unique`。
- **`IfEqualOp`**：语义为 **α-等价式** 比较（`atoms_are_equivalent`），与裸 `==` 不同。

## 与 MeTTa 语义的对应关系

- **`match`**：对应逻辑编程/模式匹配在 **Space** 上的 `query`；多结果与非确定性由解释器对 `execute_bindings` 的消费方式决定。
- **`superpose`**：显式 **非确定性选择**（把并列子表达式展开为多条归约路径）。
- **`capture`**：宿主可控的 **子解释**，用于模块化求值或沙箱式执行。
- **`pragma!`**：运行期切换解释器行为（如 `interpreter bare-minimal`、`max-stack-depth`），与 `interpret` 中的栈深设置一致。
- **`sealed` / `if-equal` / `==`**：分别服务变量捕获、条件分支与布尔相等；`if-equal` 更贴近“模式一致则分支”的 MeTTa 惯用法。

## 小结

`core.rs` 提供 **解释器旋钮**（pragma、capture）、**空间级模式匹配**（match）、**非确定性**（superpose）及与 **collapse / foldl-atom** 配套的 **内部递推原语**；是连接 Rust 解释器内核与高层 `stdlib.metta` 的关键胶水层。
