---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# MeTTa 语言规范（精简版）

> 本文是便于实现者阅读的压缩摘要，非权威标准全文。正式叙述另见 OpenCog Wiki 上的 **MeTTa Specification** PDF。

## 语法（BNF 风格）

以下描述 **S-expression** 表层语法；具体 **token** 由 **Tokenizer**（含正则注册项）扩展。

```text
<program>     ::= <top_level_item>*
<top_level_item> ::= <atom> | <type_def> | <doc_or_pragma>

<atom>        ::= <symbol>
               |  <variable>
               |  <grounded_literal>
               |  "(" <atom>* ")"

<variable>    ::= "$" <name_rest>
<symbol>      ::= <name_start> <name_rest>*   (* 不与 variable / 数字 / 字符串规则冲突 *)

<grounded_literal> ::= <number>
                    | <string_token>          (* 由 Tokenizer 识别，如双引号字符串 *)
                    | <bool_token>            (* True | False *)

<type_def>    ::= "(" ":" <atom> <type_expr> ")"
               |  "(" "=" <pattern> <body> ")"
               |  (* 以及实现支持的其它顶层形式 *)

<type_expr>   ::= <atom>   (* 箭头类型等为嵌套 Expression *)

<doc_or_pragma> ::= "(@doc" ... ")" | "(" "pragma!" ... ")"
```

**注释**：行注释使用 `;`，从 `;` 至行尾忽略。

## 最小指令集（Minimal instruction set）

引擎保证（在启用默认 **stdlib** 时）可用的核心 **grounded** 与构造块包括但不限于：

| 类别 | 代表形式 |
|------|-----------|
| 相等与条件 | `==`, `if-equal` |
| 匹配 | `match` |
| 非确定性 | `superpose`, `capture` |
| 算术与比较 | `+`, `-`, `*`, `/`, `%`, `<`, `>`, `<=`, `>=` |
| 逻辑 | `and`, `or`, `not`, `xor` |
| 空间 | `new-space`, `add-atom`, `remove-atom`, `get-atoms`, `change-state!`, `get-state` |
| 模块 | `import!`, `include`, `bind!` |
| 元编程 | `pragma!`, `sealed` |
| 调试 | `trace!`, `println!`（等） |

大量常用控制结构（如 `chain`、`collapse`、`if`）在 **stdlib.metta** 中由上述原语定义。

## 求值语义（Evaluation semantics）

1. **表达式**：非 Grounded 的 **Expression** 通常按左到右尝试归约；子表达式是否严格 **eager** / **lazy** 取决于具体操作与规则。
2. **规则匹配**：顶层的 `(= lhs rhs)` 将模式 `lhs` 与当前项匹配；成功则展开为 `rhs`（可能带 **Bindings**）。
3. **Grounded 执行**：若头部为可执行的 **GroundedAtom**，则调用其 `execute`；可返回零个、一个或多个结果 Atom（多结果即分支）。
4. **错误**：失败可表现为未匹配、**ExecError**、或包装为 `Error` 表达式（取决于宿主与操作实现）。
5. **解释器栈**：`pragma! max-stack-depth <n>` 可限制求值深度（防止无限递归）。

## 类型规则（Typing）

- 表面语法支持 `(: name type)` 为 Atom 标注类型；箭头类型写作嵌套表达式，典型为 `(-> A B)`。
- **get-type**、**get-type-space**、**get-metatype** 等操作在运行时查询类型与 **metatype**（Symbol / Expression / Grounded 等）。
- 类型推断与检查随版本演进；完整规则以实现与测试为准（见 `python/tests`、`lib` 中 **type** 相关用例）。

## 错误模型（Error model）

- **词法/语法**：解析失败抛出语法错误（Python 中为 `SyntaxError` 带引擎消息）。
- **运行时**：**MeTTa runner** 可能累积错误字符串；Python API 在 `run` / `RunnerState` 中转为 `RuntimeError`。
- **Grounded 操作**：`IncorrectArgumentError`、`NoReduceError`（Python）影响是否继续归约；`MettaError` 可映射为 MeTTa 侧 `Error` 原子。

## 版本

本文档对应源码树版本 **0.2.10**；若行为与本文冲突，以仓库内测试与 **Rust** 实现为准。
