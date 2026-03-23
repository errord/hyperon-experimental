---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `stdlib/math.rs` — 数学库函数与常量

## 文件职责

对 **`Number`** 提供超越初等算术的 **浮点为主** 的数学函数：幂、开方、对数、取整 family、三角与反三角、NaN/Inf 检测；并注册 **`PI`**、**`EXP`**（自然常数 e）为接地浮点常量。

## 接地运算一览

| MeTTa 名 | Rust 类型 | 类型签名 | 行为摘要 |
|----------|-----------|----------|----------|
| `pow-math` | `PowMathOp` | `Number → Number → Number` | 底数转 `f64`；指数为整数且可 `i32` 则用 `powi`，否则 `powf`；整数指数过大报错提示改用 float |
| `sqrt-math` | `SqrtMathOp` | `Number → Number` | `f64` 平方根（负数得 NaN） |
| `abs-math` | `AbsMathOp` | `Number → Number` | 整数/浮点分别 `abs` |
| `log-math` | `LogMathOp` | `Number → Number → Number` | `input.log(base)`（`f64` 方法） |
| `trunc-math` | `TruncMathOp` | `Number → Number` | 整数原样；浮点 `trunc` |
| `ceil-math` | `CeilMathOp` | 同上 | `ceil` |
| `floor-math` | `FloorMathOp` | 同上 | `floor` |
| `round-math` | `RoundMathOp` | 同上 | `round` |
| `sin-math` / `cos-math` / `tan-math` | 各 `*MathOp` | `Number → Number` | 三角函数，`f64` |
| `asin-math` / `acos-math` / `atan-math` | 同上 | 同上 | 反三角 |
| `isnan-math` | `IsNanMathOp` | `Number → Bool` | 整数恒 false；浮点 `is_nan()` |
| `isinf-math` | `IsInfMathOp` | `Number → Bool` | 整数恒 false；浮点 `is_infinite()` |
| `PI` | 词法 | — | `std::f64::consts::PI` |
| `EXP` | 词法 | — | `std::f64::consts::E` |

**注册**：均为 **上下文无关**。

## 核心结构体

每个运算一个 **`#[derive(Clone, Debug)]`** 单元结构体 + `grounded_op!` 的 `Display` 实现。

## `CustomExecute` 要点

- 多数一元函数将输入转为 **`f64`** 再调用 **`std` 浮点方法**；结果常包装为 **`Number::Float`**（测试中与整数理想值比较时可能仍为 `Float` 或经归一化显示为 `Integer`，以运行时为准）。
- **`pow-math`** 在指数为大整数时 **拒绝 `powi`**，避免溢出或不当转换，引导用户使用浮点指数。
- **对数 / 除法相关**：边界情况产生 **NaN 或 Inf**，由 `isnan-math` / `isinf-math` 探测（与 `arithmetics` 中浮点除零行为衔接）。

## 与 MeTTa 语义的对应关系

- 提供 **宿主级数学能力**，名称带 `-math` 后缀以区别于可能由纯 MeTTa 定义的符号。
- 与 **`Bool`**、**比较运算** 组合可写数值断言与科学计算脚本；常量 **`PI`/`EXP`** 支持无需字符串解析的精确浮点常数。

## 小结

`math.rs` 是 **浮点数学与检测原语** 的薄封装：实现直截了当，错误策略偏“返回 NaN/Inf 并由谓词检测”；与 `arithmetics.rs` 分工明确（后者为代数与布尔基础，此处为超越函数与舍入）。
