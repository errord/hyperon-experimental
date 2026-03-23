---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `stdlib/space.rs` — 空间与 StateMonad

## 文件职责

- 创建 **新的动态空间**（`DynSpace` 包装的 `GroundingSpace`）。
- 对空间进行 **增删原子**、**枚举全部原子**（遍历 + 变量唯一化）。
- 实现 **状态单子式** 接地值 **`StateAtom`**：`new-state`（`_new-state` 函数）、`get-state`、`change-state!`，用于在 MeTTa 中携带可突变状态并受类型约束。

## 接地运算一览

| MeTTa 名 | Rust 类型 | 类型签名（语义） | 行为摘要 |
|----------|-----------|------------------|----------|
| `new-space` | `NewSpaceOp` | `→ Space` | 无参时返回新 `GroundingSpace`；有参报错 |
| `add-atom` | `AddAtomOp` | `Space → Atom → Unit` | `space.add(atom)` |
| `remove-atom` | `RemoveAtomOp` | 同上 | `space.remove(atom)` |
| `get-atoms` | `GetAtomsOp` | `Space → Atom` | `visit` 收集所有原子，`make_variables_unique`；不支持遍历则 `Runtime` 错误 |
| `_new-state` | `GroundedFunctionAtom` → `new_state` | `t → Expression → (StateMonad t)` | 首参为初值原子，次参为非空类型列表表达式，取 **第一个** 类型子项构造 `(StateMonad typ)` |
| `get-state` | `GetStateOp` | `StateMonad tg → tg` | 读 `Rc<RefCell<(Atom, Atom)>>` 中当前值 |
| `change-state!` | `ChangeStateOp` | `StateMonad t → t → StateMonad t` | 就地更新状态；**类型检查**在解释器层可能产生 `BadArgType`（测试中 `F aa` 与 `F b`） |

## 核心结构体

| 结构体 | 说明 |
|--------|------|
| `StateAtom` | `state: Rc<RefCell<(Atom, Atom)>>` — `(当前值, 类型)`；`Display` 只打印值；`Grounded::type_` 返回存储的类型原子 |
| `NewSpaceOp` / `AddAtomOp` / `RemoveAtomOp` / `GetAtomsOp` / `GetStateOp` / `ChangeStateOp` | 无状态算子单元体 |

## `CustomExecute` 要点

- **`GetAtomsOp`**：依赖具体 `Space` 是否实现 **`visit`**；与模块空间、grounding 空间等行为一致时可枚举。
- **`new_state`**：类型列表目前 **仅使用第一个元素** 作为 `StateMonad` 参数（注释提及未来多类型 grounded）。
- **`change-state!`**：突变共享 `Rc` 内状态，同一 `StateAtom` 在多处引用时共享更新。

## 与 MeTTa 语义的对应关系

- **`new-space` / `add-atom` / `remove-atom` / `get-atoms`**：对应 **知识库的可变视图**——与 `match`、规则库、模块隔离等配合，实现多空间推理与脚本化空间构建。
- **StateMonad**：在纯符号归约中嵌入 **命令式状态**（类似 IO/State monad 的最小落地），`change-state!` 的 `!` 强调副作用。
- 测试中 **`mod-space!`** 与 **`get-atoms`** 联用，展示与 **模块空间** 的互操作。

## 小结

`space.rs` 连接 **超on Space 抽象** 与 MeTTa 中的 **过程式空间操作**；`StateAtom` 提供轻量 **可突变、可类型标注** 的状态单元，适合 REPL 与有状态小程序而不必引入完整宿主对象模型。
