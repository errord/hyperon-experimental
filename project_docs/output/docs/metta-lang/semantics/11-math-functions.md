---
title: 数学函数（MeTTa → Python → Rust）
order: 11
---

# 文档 11：数学函数全链实现

本文档覆盖 **`pow-math`**、**`sqrt-math`**、**`abs-math`**、**`log-math`**、取整族、三角/反三角、**`isnan-math`**、**`isinf-math`**，以及常量 **`PI`**、**`EXP`** 在 **`lib/src/metta/runner/stdlib/math.rs`** 中的实现，并说明 **`grounded_op!` 宏**、**`f64` 转换**与**定义域错误（NaN/Inf）**行为。

**Python**：默认 MeTTa 环境中这些名称均在 **Rust 核心** 注册；**`python/hyperon/stdlib.py`** 不包含同名数学原语。Python 侧路径与文档 10 相同：**`hp.metta_run`** 驱动 Rust 解释器（`python/hyperon/runner.py` 第 206–214 行；`python/hyperonpy.cpp` 第 1117–1120 行）。

---

## 1. 文件与注册入口

| 内容 | 路径与行号 |
|------|------------|
| 全部数学 grounded 算子与测试 | `lib/src/metta/runner/stdlib/math.rs` |
| 装载时注册 | 同文件 **`register_context_independent_tokens`** **第 408–445 行** |
| 核心库汇总注册 | `lib/src/metta/runner/stdlib/mod.rs` **第 89 行** `math::register_context_independent_tokens(tref)` |
| 算子显示名 / `PartialEq` 桩 | `lib/src/metta/runner/stdlib/mod.rs` **`grounded_op!` 宏** **第 23–37 行** |

> 用户材料中的 “MathOp 宏” 在本仓库拆为：每个结构体旁的 **`grounded_op!(StructName, "token")`**（仅 `Display` 与 **永远为真的 `PartialEq`**），**执行逻辑**在各结构体的 **`CustomExecute`** 中手写。

---

## 2. `grounded_op!` 宏模式（`mod.rs`）

**第 23–37 行**：

- **`PartialEq::eq`**：两实例恒为 `true`（第 25–28 行）—— 便于 MeTTa 测试里比较 **错误表达式** 中的操作原子占位。
- **`Display`**：写入字面字符串 `$disp`（第 31–34 行）。

数学各结构体在 **`math.rs`** 中均先写 **`#[derive(Clone, Debug)]`** 与 **`grounded_op!(XxxMathOp, "...")`**，再分别 **`impl Grounded` / `CustomExecute`**。

---

## 3. 类型签名通则

多数一元函数类型为 **`-> Number Number`**（参数一个 `Number`，返回一个 `Number`），在各自 **`Grounded::type_`** 中写为：

```rust
Atom::expr([ARROW_SYMBOL, ATOM_TYPE_NUMBER, ATOM_TYPE_NUMBER])
```

二元 **`pow-math`**、**`log-math`** 为 **`-> Number Number Number`**（三元组：箭头 + 三类型），见 **`PowMathOp`** 第 14–16 行、**`LogMathOp`** 第 94–96 行。

**`isnan-math` / `isinf-math`** 返回 **Bool**：**`-> Number Bool`**（第 360–362、387–389 行）。

---

## 4. `pow-math`（`PowMathOp`）

**第 10–37 行**。

### 4.1 参数与错误消息

- 需 **两个** `Number`：`base`、`pow`（第 23–25 行）。
- 任一无法解析为数字：`ExecError::from("pow-math expects two arguments: number (base) and number (power)")`（第 23 行）。

### 4.2 指数分支

- **`base`** 先转为 **`f64`**：`?.into()`（第 24 行），即 **`Into<f64> for Number`**（`number.rs` 第 50–56 行）。
- **`pow` 为 `Integer`**：尝试 **`TryInto::<i32>::try_into(n)`**（第 28–31 行）。成功则 **`base.powi(n)`**（第 29 行）；失败则 **`ExecError::from("power argument is too big, try using float value")`**（第 30 行）。
- **`pow` 为 `Float`**： **`base.powf(f)`**（第 33 行）。

### 4.3 返回值类型

- 统一 **`Ok(vec![Atom::gnd(Number::Float(res))])`**（第 35 行）。  
  因此即使 **`powi`** 得到数学上的整数，**存储仍为 `Float`**。集成测试 **`metta_pow_math`**（第 453–457 行）对 **`5^2`** 的期望与 **`Number::Integer(5_i64.pow(2))`** 比较时，依赖 **`Number` 的 `PartialEq` 提升**（见文档 10）。

### 4.4 分词

**第 409–410 行**：`pow-math` 正则 → `PowMathOp` 克隆。

---

## 5. `sqrt-math`（`SqrtMathOp`）

**第 39–60 行**。

- 单参数转 **`f64`**（第 57 行），**`input.sqrt()`**（第 58 行），**结果 `Number::Float(...)`**（第 58 行）。
- **负数实数平方根**：Rust **`f64::sqrt`** 对负数为 **NaN**，**不**返回 `ExecError`；测试 **`metta_sqrt_math`** **第 463 行** 用 **`isnan-math`** 检测。
- 分词：**第 411–412 行**。

---

## 6. `abs-math`（`AbsMathOp`）

**第 62–86 行**。

- **`Integer`**：**`n.abs()`**，保持 **`Number::Integer`**（第 82 行）。
- **`Float`**：**`f.abs()`**，**`Number::Float`**（第 83 行）。
- 分词：**第 413–414 行**。

---

## 7. `log-math`（`LogMathOp`）

**第 88–110 行**。

- 两参数均转 **`f64`**：`base`、`input`（第 106–107 行）。
- 使用 **`input.log(base)`**（第 108 行）（Rust **`f64::log`**）。
- **定义域错误**：如 **`log(0,0)`** 得 **NaN**；**`log(5,0)`** 得 **负无穷**；测试见 **第 475–478、597–607 行**，用 **`isnan-math` / `isinf-math`** 断言，而非 `ExecError`。
- 分词：**第 415–416 行**。

---

## 8. 取整族：`trunc-math` / `ceil-math` / `floor-math` / `round-math`

### 8.1 共同模式

各 **`execute`**（**Trunc** 第 127–135、**Ceil** 第 153–161、**Floor** 第 179–187、**Round** 第 205–213 行）：

- **`Integer` 输入**：原样返回 **`Number::Integer(n)`**（短路，避免无意义的 “浮点化”）。
- **`Float` 输入**：调用 **`f.trunc()` / `f.ceil()` / `f.floor()` / `f.round()`**，包装为 **`Number::Float(...)`**。

### 8.2 与测试中的 “整数形态” 结果

单测常写 **`Number::Integer(2)`** 与 **`trunc-math 2.4`** 结果相等（**第 483、489、496、503 行**等）。实现实际返回 **`Float(2.0)`** 时，**`Atom` 层面**仍可能判等，因 **`gnd_eq` → `Number` 的 `PartialEq` 会做 promote**（文档 10、`number.rs` 第 13–26 行）。阅读源码时请以 **返回分支** 为准，勿仅依赖测试字面类型。

### 8.3 分词

**第 417–424 行**：`trunc-math`、`ceil-math`、`floor-math`、`round-math` 依次注册。

---

## 9. 三角与反三角（弧度）

以下均在 **`execute` 内**把参数 **`Into<f64>`** 后调用 **`f64` 方法**，并 **`Number::Float`** 包装结果。

| MeTTa | 结构体 | 方法 | 主要行号 |
|-------|--------|------|----------|
| `sin-math` | `SinMathOp` | `.sin()` | 216–237，注册 425–426 |
| `asin-math` | `AsinMathOp` | `.asin()` | 239–260，427–428 |
| `cos-math` | `CosMathOp` | `.cos()` | 262–283，429–430 |
| `acos-math` | `AcosMathOp` | `.acos()` | 285–306，431–432 |
| `tan-math` | `TanMathOp` | `.tan()` | 308–329，433–434 |
| `atan-math` | `AtanMathOp` | `.atan()` | 331–352，435–436 |

**定义域**：**`asin` / `acos`** 在 **实数域外** 产生 **NaN**，与 **`sqrt-math`** 类似，**不**转为 `ExecError`；测试用近似相等或小阈值比较（**第 509–547 行**）。

---

## 10. `isnan-math` / `isinf-math`

### 10.1 `IsNanMathOp`（第 354–378 行）

- **`Integer`**：恒 **`false`**（第 374 行）（整数不视为 NaN）。
- **`Float`**：**`f.is_nan()`**（第 375 行）。
- 返回 **`Bool(res)`**（第 377 行）。
- 类型 **`-> Number Bool`**（第 360–362 行）。
- 分词：**第 437–438 行**。

### 10.2 `IsInfMathOp`（第 381–405 行）

- **`Integer`**：**`false`**（第 401 行）。
- **`Float`**：**`f.is_infinite()`**（第 402 行）。
- 分词：**第 439–440 行**。

二者用于 **检测 `log-math` / `sqrt-math` / 除法** 等产生的 **非有限数**，而非依赖异常。

---

## 11. 常量 `PI` 与 `EXP`

**第 441–444 行**：

- **`PI`** → **`Number::Float(std::f64::consts::PI)`**
- **`EXP`** → **`Number::Float(std::f64::consts::E)`**

无独立结构体，闭包直接构造 **grounded `Number`**。

---

## 12. `f64` 转换与数值稳定性小结

1. **显式 `Into<f64>`**：**`pow-math`（底）**、**`sqrt`/`sin` 族**、**`log-math`（两参）** 在入口使用（见各 `execute` 首行 `let ...: f64 = ...?.into()`）。
2. **保持 `Number` 分支**：**`abs-math`**、**取整四函数** 对 **整数** 保留 **`Integer`**，减少无谓浮点。
3. **整数幂**：**`pow-math`** 对 **整数指数** 用 **`powi`**，避免 **`powf`** 的精度损失；超大整数指数失败则提示改用 **float**（第 30 行）。

---

## 13. 错误处理分类

| 类别 | 机制 | 示例位置 |
|------|------|----------|
| 参数个数/类型不符 | **`ExecError::from("... expects ...")`** | 各 `execute` 的 `arg_error` 闭包 |
| 幂指数过大（整数） | 明确 **`ExecError`** | `PowMathOp` 第 28–31 行；测试 第 455、569 行 |
| 数学定义域（实数） | **`f64` 的 NaN/Inf**；用 **`isnan-math`/`isinf-math`** 或算术比较检测 | `sqrt` 负参；`log` 第 476–478 行 |
| 整数除零 | **不属于** `math.rs`；见 **`DivOp`**（文档 10） | `arithmetics.rs` 第 154–155 行 |

本模块 **普遍不** 在 **`sqrt(NaN)`** 这类情况抛 **Rust panic**；依赖 **IEEE 754** 语义。

---

## 14. 与 `Number` grounded 类型的关系

所有数学算子通过 **`Number::from_atom`**（`number.rs` 第 90–92 行）从 **`Atom`** 取数，失败则 **`ExecError`**。  
**`Grounded for Number`**（`number.rs` 第 135–146 行）声明运行时类型为 **`Number`**；**`serialize`** 写 **`i64`/`f64`**（第 140–144 行），供跨语言 **hyperonpy** 边界使用（与 C API 序列化一致，细节见 `hyperonpy` 中 atom 拷贝路径）。

---

## 15. Python / hyperonpy 全链（无 Python 数学原语时）

1. **`MeTTa.__init__`**（`runner.py` 第 110–132 行）创建 Rust runner 并加载 **`_priv_load_module_stdlib`**。
2. **`metta.run("!(sin-math 0)")`**（第 206–214 行）→ **`metta_run`**（`hyperonpy.cpp` 第 1117–1120 行）。
3. **分词**：tokenizer 上已有 **`math.rs`** 注册的 **`sin-math`**（**第 425–426 行**）。
4. **求值**：Rust **`CustomExecute::execute`** 返回的 **`Atom`** 列表拷贝到 Python（`copy_lists_of_atom` 回调，同文件第 1118–1119 行）。
5. Python **`stdlib.py`** **不**定义 `sin-math`；若用户用 **`register_token`** 覆盖同名符号，才会走 Python 路径。

---

## 16. 测试索引（`math.rs`）

| 测试名 | 起始行 | 覆盖 |
|--------|--------|------|
| `metta_pow_math` | 453 | 整数幂、指数过大、浮点幂、非数字参数 |
| `metta_sqrt_math` | 461 | 开方、负数 NaN、错误参数 |
| `metta_abs_math` | 468 | |
| `metta_log_math` | 475 | NaN / Inf |
| `metta_trunc_math` | 482 | |
| `metta_ceil_math` | 488 | 正负边界 |
| `metta_floor_math` | 495 | |
| `metta_round_math` | 502 | |
| `metta_sin_math` … `metta_atan_math` | 509–547 | |
| `metta_isnan_math` / `metta_isinf_math` | 551–561 | |
| `*_math_op` 单元测试 | 565–739 | 直接调用 `.execute` |

---

## 17. 速查表（行号）

| 符号 | `execute` | `register` |
|------|-----------|------------|
| `pow-math` | 21–36 | 409–410 |
| `sqrt-math` | 54–59 | 411–412 |
| `abs-math` | 77–85 | 413–414 |
| `log-math` | 103–109 | 415–416 |
| `trunc-math` | 127–135 | 417–418 |
| `ceil-math` | 153–161 | 419–420 |
| `floor-math` | 179–187 | 421–422 |
| `round-math` | 205–213 | 423–424 |
| `sin-math` | 231–236 | 425–426 |
| `asin-math` | 254–259 | 427–428 |
| `cos-math` | 277–282 | 429–430 |
| `acos-math` | 300–305 | 431–432 |
| `tan-math` | 323–328 | 433–434 |
| `atan-math` | 346–351 | 435–436 |
| `isnan-math` | 369–378 | 437–438 |
| `isinf-math` | 396–405 | 439–440 |
| `PI` / `EXP` | — | 441–444 |

---

## 18. FAQ

**Q：为何 `pow-math` 总是返回 `Float`？**  
A：**第 35 行** 写死 **`Number::Float(res)`**，与 **`powi`/`powf`** 分支无关。

**Q：`log-math` 参数顺序？**  
A：**第 106–107 行**：**第一参数为底 `base`**，**第二为真数 `input`**，对应 **`input.log(base)`**。

**Q：与 C 标准库 `log` 单参自然对数有何不同？**  
A：此处是 **双参换底** 形式；若需 **ln**，需令 **`base == e`**（可用 **`EXP`** 常量，第 443–444 行）。

**Q：Python 能否拦截 `sqrt-math`？**  
A：可以，在 **后注册** 的 tokenizer 规则中覆盖同名 token（注意 **`Tokenizer::find_token`** 后进先匹配，`text.rs` 第 74–80 行）。

---

以上行号以本仓库 **`hyperon-experimental`** 为参照；函数行为以 **`math.rs`** 与 **`f64`** 标准库为准。

---

## 19. 与算术模块 `DivOp` 的衔接（浮点除零）

**`math.rs`** 不负责 **`/`**。浮点 **`(/ x 0.0)`** 在 **`arithmetics.rs` `DivOp`**（第 152–157 行）中按 **IEEE 规则** 得到 **Inf**，不触发 **`DivisionByZero`**（该错误仅针对 **整数除数 0**，第 154–155 行）。  
因此 **`isinf-math`**（第 396–405 行）常用于诊断此类结果；集成示例见 **`arithmetics.rs` 测试** 第 221 行 **`(/ 5.0 0.0)`** 与 **`isinf-math`** 的组合。

---

## 20. 源码阅读顺序建议

1. 阅读 **`mod.rs` `grounded_op!`**（第 23–37 行），理解 **测试与错误消息里操作原子的比较方式**。  
2. 打开 **`math.rs`**，自 **`PowMathOp`** 向下顺读 **`execute`**，注意 **`Into<f64>`** 与 **`Number::Float` 返回** 的分岔。  
3. 对照 **`number.rs` `Number::from_atom` / `promote` / `PartialEq`**，理解为何测试中 **Integer 与 Float** 可互换断言。  
4. 在 Python 中 **`metta.parse_single("sin-math")`** 验证 tokenizer 已绑定 grounded 操作符（与 **`test_grounded_type.py`** 思路一致）。  
5. 若修改数学库，**同步更新** **`register_context_independent_tokens`** 中的 **正则字符串**（第 408–445 行），否则词法层无法识别新 token。

---

## 21. 与设计取舍相关的注释（仓库内）

- **`Number::PartialEq`**（`number.rs` 第 15–18 行）注释指出：**提升后比较** 有助于 atom 相等，但可能在 **其它 Rust 容器** 中与 **Float/Integer 混用** 时带来意外；数学测试广泛依赖当前语义。  
- **`gnd_eq`**（`hyperon-atom/src/gnd/mod.rs` 第 89–92 行）注释称其为 **hack**，未来可能由模块级相等谓词替代；当前 **`==` 与数学比较** 仍建基于此路径。

---

## 22. 空参数与错误消息一致性

各算子的 **`arg_error`** 字符串在 **`metta_*` 测试** 中与 **`Error (...)`** 结果严格对齐（例如 **`metta_sin_math`** 第 512 行）。新增运算时应 **复制此模式**，在 **`execute`** 与 **`#[test]`** 中保持 **同一英文消息**，避免仅运行时崩在 **`Option::unwrap`**。
