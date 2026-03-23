---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `stdlib/arithmetics.rs` — 算术、比较与布尔接地运算

## 文件职责

- 通过宏 **`def_binary_number_op!`** 批量生成二元数值算子的 `Grounded` + `CustomExecute` 实现。
- 通过宏 **`def_binary_bool_op!`** 生成二元布尔算子。
- 单独实现 **`DivOp`**（整数除零错误）、**`NotOp`**（一元非）。
- 在 **Tokenizer** 中注册 **数字字面量**（整数、小数、科学计数法）与 **`True`/`False`**，并注册运算符 token。

## 接地运算与词法

| MeTTa / 词法 | Rust 类型 | 类型签名 | 行为摘要 |
|--------------|-----------|----------|----------|
| `+` | `SumOp` | `Number → Number → Number` | `Number::promote` 后整数或浮点相加 |
| `-` | `SubOp` | 同上 | 减 |
| `*` | `MulOp` | 同上 | 乘 |
| `/` | `DivOp` | 同上 | 除；**整数除数为 0** 返回 `DivisionByZero`；浮点 `/ 0.0` 得无穷（由 IEEE 语义，测试中配合 `isinf-math`） |
| `%` | `ModOp` | 同上 | 取模 |
| `<` `>` `<=` `>=` | `LessOp` 等 | `Number → Number → Bool` | 比较 |
| `and` | `AndOp` | `Bool → Bool → Bool` | 逻辑与 |
| `or` | `OrOp` | 同上 | 逻辑或 |
| `xor` | `XorOp` | 同上 | 按位异或（注释说明 Python 侧故意保留以做转换测试） |
| `not` | `NotOp` | `Bool → Bool` | 逻辑非 |
| 数字字面量 | — | — | `register_fallible_token` 解析为 `Number` |
| `True` / `False` | — | — | 解析为接地 `Bool` |

**注册**：全部为 **上下文无关** token。

## 核心结构体

均由宏或手写生成 **`#[derive(Clone, PartialEq, Debug)]`** 的空结构体，并实现 **`Display`**（算术算子显示为 `+`、`-` 等符号）。

## `CustomExecute` 要点

- **`def_binary_number_op`**：`Number::from_atom` 失败 → `ExecError::IncorrectArgument`；`promote` 后仅在 `Integer/Integer` 或 `Float/Float` 分支运算。
- **`DivOp`**：单独处理 **整数除零**；浮点依赖 Rust/`f64` 语义。
- **布尔算子**：从原子提取 `Bool` 包装，失败则参数错误。

## 与 MeTTa 语义的对应关系

- 提供 MeTTa 程序中最基础的 **Grounded 数值与布尔代数**，供 `if`、`比较链、算术规则等使用；类型签名使用全局 `Number` / `Bool` 类型原子，与类型检查器协同。
- 字面量注册使 **源码中的数字与 True/False** 无需额外 `quote` 即可成为接地值。

## 小结

`arithmetics.rs` 是 stdlib 的 **标量计算核心**：一致的类型提升规则、明确的整数除零错误，以及完整的比较与布尔运算；实现高度 **宏驱动**，便于与 Python/其它宿主的行为对齐测试。
