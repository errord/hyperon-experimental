---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 非确定性求值专题

MeTTa 的归约不必是单值的：同一表达式可以对应多个合法结果分支。引擎通过 **BindingsSet**、多结果 **Grounded** 与 **search** 式展开来管理这种非确定性。

## `superpose`

**签名（概念）**：`(-> Expression Undefined)`（实现中返回类型为 **Undefined**，语义上展开为多个后继）。

**语义**：`superpose` 接收一个 **Expression**，将其**子节点列表**视为并行可选分支——每个子项成为独立候选结果。

```metta
(superpose (A B C))
```

求值后可能分别得到 `A`、`B`、`C` 作为不同分支。常与 `match`、自定义规则组合，用于显式 **OR** 搜索空间。

## `collapse` 与 `collapse-bind`

`collapse` 在 **stdlib.metta** 中定义：对给定 Atom 调用内部 **`metta`** 求值，再通过 **`collapse-bind`** 收集 `(atom, bindings)` 对，并折叠为单一结果表达式。用于把“多分支求值”收束为可继续处理的结构（例如列表式 **Expression**）。

**`collapse-bind`**：与 `collapse` 配套，暴露绑定信息；若只需 Atom 而不要 **Bindings**，标准库中另有辅助形式（见 `stdlib.metta` 内 `@doc`）。

典型用途：

- 在定义宏级辅助函数时先 **eval** 再统一整理结果。
- 与 `unique-atom`、`union-atom` 等组合去重或合并分支。

## 多定义分支

同一模式可对应多条 `(= ...)` 规则，或一条规则的右侧引入 `superpose`，都会增加并行路径。解释器不保证分支顺序；依赖顺序的算法应使用显式顺序结构（如 `chain`）或自定义 **Grounded**。

## `match` 与非确定性

`match` 在空间上查询模式：每个成功匹配产生一组 **Bindings**，与 **template** 组合后可生成多个实例化结果。这是 **Space** 层非确定性的主要来源。

## 解释器分支管理

- **Runner** 在内部维护待探索分支；**Python** 的 `MeTTa.run` 返回**结果列表的列表**——外层为“并行结果集”，内层为单次运行路径上的 Atom 序列（具体形状以调用与程序为准）。
- **`RunnerState`**：`run_step` 单步推进；`current_results(flat=...)` 可观察当前中间结果，用于调试或自定义调度。
- **调试**：`print-alternatives!`（**debug** 库）可打印当前可选分支，便于理解 **search** 行为。

## 实践建议

1. 先用小例子验证 `superpose` + `match` 的组合是否符合预期。
2. 需要“唯一答案”时，用 `collapse` / `unique`（stdlib 定义）或自定义筛选。
3. 注意 `pragma! max-stack-depth`：深度搜索易触发栈限制。

## 参见

- `stdlib-reference.md`：`superpose`、`match`、`capture` 等条目。
- 教程：`tutorial/b4-nondeterm.md`（若已生成）。
