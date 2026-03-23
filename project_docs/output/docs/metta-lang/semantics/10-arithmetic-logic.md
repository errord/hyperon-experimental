---
title: 算术与逻辑运算（MeTTa → Python → Rust）
order: 10
---

# 文档 10：算术与逻辑运算全链实现

本文档从 **MeTTa 表面语法** 出发，沿 **词法/分词 → 求值 → 底层类型** 追踪 `+`、`-`、`*`、`/`、`%`、比较、`and`/`or`/`not`、`==`、`if-equal` 等特性的实现位置，并说明 **Python（hyperon）** 侧如何与同一套 Rust 核心交互。

---

## 1. 总览：代码落在哪些 crate / 文件

| 层级 | 路径 | 作用 |
|------|------|------|
| 分词注册（算术/比较/布尔） | `lib/src/metta/runner/stdlib/arithmetics.rs` 第 162–199 行 | 将 `+`、数字字面量、`True`/`False` 等映射为 **grounded 操作原子** 或 **Number/Bool** |
| 分词注册（`==`、`if-equal`） | `lib/src/metta/runner/stdlib/core.rs` 第 336–346 行 | `==` → `EqualOp`，`if-equal` → `IfEqualOp` |
| 核心库装载顺序 | `lib/src/metta/runner/stdlib/mod.rs` 第 85–94 行 | `register_context_independent_tokens` 依次调用 `math`、`arithmetics`、`string`、`core` 等子模块的注册函数 |
| 数字/布尔 grounded 类型 | `hyperon-atom/src/gnd/number.rs`、`hyperon-atom/src/gnd/bool.rs` | `Number`（`Integer`/`Float`）、`Bool`、`PartialEq` 与序列化 |
| 原子相等（`==` 语义基础） | `hyperon-atom/src/lib.rs` 第 981–990 行；`hyperon-atom/src/gnd/mod.rs` 第 88–108 行 | `Atom` 的 `PartialEq`；grounded 比较走 `gnd_eq` |
| 结构等价（`if-equal`） | `hyperon-atom/src/matcher.rs` 第 1204 行起 `atoms_are_equivalent` | 与 `==` 不同的等价关系 |
| Python 入口 | `python/hyperon/runner.py` 第 107–132、206–214 行；`python/hyperonpy.cpp` 第 1096–1121 行 | `MeTTa` 构造、`metta_run` 进入 Rust 解释器 |
| Python 扩展 stdlib | `python/hyperon/stdlib.py` | **不**实现 `+`/`-` 等；与字符串相关的 `repr`/`parse` 等见文档 12 |

---

## 2. 二元算术宏：`def_binary_number_op!`

源码宏定义位于 `arithmetics.rs` **第 10–48 行**。

### 2.1 宏展开后的共同结构

对每个操作符，宏生成：

1. **结构体** `pub struct $name {}`（第 12–13 行模板）。
2. **`Display`**：打印为字面操作符（如 `+`）（第 15–18 行）。
3. **`Grounded::type_`**：类型为 `-> Number Number Number`（比较类为 `-> Number Number Bool`），使用 `ARROW_SYMBOL`、`ATOM_TYPE_NUMBER`、`ATOM_TYPE_BOOL` 等（第 21–24 行）。
4. **`CustomExecute::execute`**（第 31–45 行）：
   - 用 `args.get(0/1).and_then(Number::from_atom)` 取两个参数；失败返回 `ExecError::IncorrectArgument`（第 33–35 行）。
   - 调用 **`Number::promote(a, b)`**（第 37 行）做 **Integer→Float 提升**（规则见第 4 节）。
   - 在 **同为 Integer 或同为 Float** 的分支上执行 Rust 运算符 `$op`（第 38–41 行）。
   - 结果包装为 `Atom::gnd(res)`（第 44 行）。

### 2.2 由宏实例化的运算

同一文件 **第 50–57 行**：

- `SumOp` → `+`（第 50 行）
- `SubOp` → `-`（第 51 行）
- `MulOp` → `*`（第 52 行）
- `ModOp` → `%`（第 53 行）
- `LessOp` / `GreaterOp` / `LessEqOp` / `GreaterEqOp` → `<` `>` `<=` `>=`，返回类型参数为 `Bool`（第 54–57 行）

> 说明：用户材料中若写作 “ArithOp”，本仓库中的实际名称为 **`def_binary_number_op!`**；比较运算与算术共用该宏，仅 **返回类型** 与 **Rust 运算符** 不同。

---

## 3. 除法 `DivOp`（单独实现，非宏）

`/` 在 **第 127–160 行** 单独实现，原因包括：**整数除零** 要返回明确错误，而 `%` 等宏生成路径不处理该语义。

- **类型**：`-> Number Number Number`（第 136–139 行）。
- **参数解析**：`Number::from_atom`（第 149–150 行）；错误信息为 `"Divide expects two numbers: dividend and divisor"`（第 148 行）。
- **提升**：`Number::promote(dividend, divisor)`（第 152 行）。
- **整数除零**：`(Number::Integer(_), Number::Integer(0))` → `Err(ExecError::from("DivisionByZero"))`（第 154–155 行）。
- **正常路径**：整数 `/`、浮点 `/`（第 155–156 行）。

MeTTa 层测试见同文件 **第 218–221 行**：`(/ 5 0)` 与 `Error ... DivisionByZero` 的断言；浮点 `(/ 5.0 0.0)` 不产生该错误，而与 `isinf-math` 配合（第 221 行）。

---

## 4. `Number`：内部表示与提升规则

文件：`hyperon-atom/src/gnd/number.rs`。

### 4.1 枚举与类型常量

- **`Number`**：`Integer(i64)` 或 `Float(f64)`（第 8–11 行）。
- **`ATOM_TYPE_NUMBER`**：符号 `Number`（第 5 行）。

### 4.2 `promote` 与 `widest_type`

- **`Number::promote(a, b)`**（第 85–88 行）：先算 **最宽类型** `NumberType::widest_type`，再对 `a`、`b` 分别 **`cast`**。
- **`widest_type`**（第 116–122 行）：任一为 `Float` 则结果为 `Float`，否则 `Integer`。

### 4.3 `cast` 与 `Into` 转换

- **`cast`**（第 101–105 行）：目标为 `Integer` 时用 `Into<i64>`，为 `Float` 时用 `Into<f64>`。
- **`Into<f64> for Number`**（第 50–56 行）：`Integer` 转 `f64` 为 `n as f64`。
- **`Into<i64> for Number`**（第 41–47 行）：`Float` 转 `i64` 为 `n as i64`（截断）。

因此 **算术宏中** 两操作数经 `promote` 后只会在 **两 Integer** 或 **两 Float** 上运算（`arithmetics.rs` 第 38–41 行），不会出现混合分支，最后的 `_ => panic!`（第 41 行）为防御性代码。

### 4.4 `Number` 的相等性（影响 `==` 对数字原子）

`PartialEq for Number`（**第 13–26 行**）在比较前 **同样调用 `promote`**。因此 **整数 2 与浮点 2.0** 作为两个 `Number` 值比较时，会先提升到 `Float` 再比。

> 这与“仅语法层类型”的直觉不同；文档 11 中若干数学函数单测用 `Integer(2)` 与 `Float(2.0)` 断言相等，即依赖此行为。

### 4.5 字面量分词（进入 `Number` 的路径）

`arithmetics.rs` **第 163–168 行** 在 **`register_context_independent_tokens`** 中注册：

- 整数正则 → `Number::from_int_str`（第 163–164 行）
- 小数 / 科学计数 → `Number::from_float_str`（第 165–168 行）

解析实现见 `number.rs` **`from_int_str` / `from_float_str`**（第 75–83 行）。

---

## 5. 比较运算：`<` `>` `<=` `>=`

仍由 **`def_binary_number_op!`** 生成（`arithmetics.rs` 第 54–57 行），执行路径与 `+` 相同：**`Number::promote`** 后做 Rust 比较，结果 **`Bool`** 包装为 grounded（宏第 44 行，`$ret_type` 为 `Bool`）。

返回类型签名中为 `ATOM_TYPE_BOOL`（宏第 23 行）。

---

## 6. 布尔运算：`and` / `or` / `not`（及 `xor`）

### 6.1 二元布尔宏 `def_binary_bool_op!`

`arithmetics.rs` **第 59–90 行**：类型 `-> Bool Bool Bool`（第 72 行），从参数取 `Bool::from_atom`（第 83–84 行），结果 `Bool(a OP b)`（第 86 行）。

实例化（**第 92–96 行**）：

- `AndOp` → 显示 `and`，运算 `&&`（第 92 行）
- `OrOp` → `or`，`||`（第 93 行）
- `XorOp` → `xor`，`^`（第 96 行）；注释写明 **Python 有意省略 xor 以便做转换测试**（第 95–96 行）

### 6.2 `NotOp`

**第 99–125 行**：一元，`-> Bool Bool`（第 110 行），`Bool(!a)`（第 123 行）。

### 6.3 `Bool` 类型与 `True`/`False` 分词

文件：`hyperon-atom/src/gnd/bool.rs`。

- **`Bool(pub bool)`**（第 8 行）；**`ATOM_TYPE_BOOL`**（第 5 行）。
- **`from_str`**：`"True"` / `"False"`（第 11–16 行）。
- **`BoolSerializer`**（第 64–83 行）：通过 `serialize_bool` 反序列化回 `Bool`。
- **`Grounded::serialize`**（第 59–61 行）：写入布尔值。

分词：`arithmetics.rs` **第 169–170 行**，正则 `True|False` → `Bool::from_str`。

### 6.4 `Display` 与原子打印

`bool.rs` **第 45–51 行**：`True` / `False` 字符串。

---

## 7. 原子相等：`==`（`EqualOp`）

### 7.1 实现位置

`lib/src/metta/runner/stdlib/core.rs` **第 115–137 行**。

- **`type_`**：`(-> t t Bool)` 的多态箭头（第 121–122 行），使用 `expr!(t)`。
- **`execute`**：取两个参数 `a`、`b`，返回 **`Atom::gnd(Bool(a == b))`**（第 136 行）。

此处的 **`a == b`** 是 Rust 对 **`Atom` 的 `PartialEq`**（见下节），即 **结构相等**（同构、同内容），**不是** `atoms_are_equivalent`。

### 7.2 `Atom::PartialEq` 与 grounded 的 `gnd_eq`

`hyperon-atom/src/lib.rs` **第 981–990 行**：

- 符号/表达式/变量：各子类型的 `PartialEq`。
- **Grounded**：`gnd::gnd_eq(&**gnd, &**other)`（第 987 行）。

`hyperon-atom/src/gnd/mod.rs` **第 88–108 行** `gnd_eq`：

1. 若 **`a.eq_gnd(b)`** 为真则返回真（第 93–95 行）。
2. 类型不同则假（第 96–98 行）。
3. 对 **`String` / `Number` / `Bool`** 分别用 `Str`/`Number`/`Bool` 的 **`TryFrom` + `==`**（第 99–104 行）。
4. 其他 grounded 类型默认 **false**（第 105–106 行）。

**`Number`** 比较时仍带 **promote**（`number.rs` 第 13–26 行），故 **`== 2 2.0`** 在值为 2 与 2.0 时可认为 **相等**（在成功求值为两 `Number` 的前提下）。

### 7.3 分词注册

`core.rs` **第 345–346 行**：`==` → `EqualOp` 原子克隆。

### 7.4 参数错误信息（实现细节）

`EqualOp::execute` 第 132 行使用 `concat!(stringify!($op), " expects two arguments")`。阅读源码时请注意 **`$op` 并非本块宏参数**；若编译通过，其行为以本地工具链为准。参数不足时仍走 **`args.get(...).ok_or_else(arg_error)?`**（第 133–134 行）。

---

## 8. 条件选择：`if-equal`（`IfEqualOp`）

`core.rs` **第 170–197 行**。

- **类型**：四元：`Atom Atom Atom Atom -> ?`（第 175–176 行），返回 **`then` 或 `else` 分支原子的克隆**（第 192–195 行）。
- **判定**：**`hyperon_atom::matcher::atoms_are_equivalent(atom, pattern)`**（第 192 行），定义见 **`hyperon-atom/src/matcher.rs` 第 1204 行起**。

与 **`==`** 的差异（概念上）：

- **`==`**：返回 **Bool 原子**，基于 **`Atom::PartialEq`**。
- **`if-equal`**：返回 **分支表达式**，基于 **`atoms_are_equivalent`**（对变量重命名等更“等价”）。

`stdlib.metta` 中大量 **`eval`/`chain` 组合子** 使用 `if-equal`（例如约第 295–420 行一带），用于控制求值与元类型分支。

### 8.1 分词注册

`core.rs` **第 337–338 行**：`if-equal` → `IfEqualOp`。

---

## 9. 算术与逻辑：MeTTa 中的分词注册（汇总）

`arithmetics.rs` **`register_context_independent_tokens`** **第 162–199 行**：

| 正则 / 模式 | 构造 |
|-------------|------|
| 整数 / 浮点 / 科学计数 | `Number::from_int_str` / `from_float_str`（第 163–168 行） |
| `True|False` | `Bool::from_str`（第 169–170 行） |
| `\+` `\*` `/` `%` `<` `>` `<=` `>=` | 各 `Op` 的 `Atom::gnd` 克隆（第 172–189 行） |
| `and` `or` `not` `xor` | 同上（第 190–198 行） |

**调用链**：`mod.rs` 第 90 行 `arithmetics::register_context_independent_tokens(tref)` 在 **核心库加载** 时执行；此前 **`math`**（第 89 行）已注册 `pow-math` 等（见文档 11）。

**分词优先级**：`text.rs` 中 `Tokenizer::find_token` **从向量尾部向前** 查找第一个全串匹配（**第 74–80 行**），因此 **后注册的规则优先**。若 Python 模块追加同名字面规则，可能覆盖 Rust 默认行为（`stdlib.metta` 第 1311–1312 行注释亦提及 Rust/Python 双实现冲突时的文档问题）。

---

## 10. Python 侧：算术如何进入 Rust（hyperonpy）

### 10.1 `MeTTa` 初始化

`python/hyperon/runner.py` **第 110–132 行**：

- 默认 **`hp.metta_new_with_stdlib_loader(_priv_load_module_stdlib, space.cspace, env_builder)`**（第 132 行）。

`hyperonpy.cpp` **第 1096–1098 行**：将 Python 的 `stdlib_loader` 与 Rust **`metta_new_with_stdlib_loader`** 连接。

### 10.2 运行程序

`runner.py` **`MeTTa.run`** **第 206–214 行**：构造 `SExprParser`，调用 **`hp.metta_run(self.cmetta, parser.cparser)`**。

`hyperonpy.cpp` **第 1117–1120 行**：`metta_run` 将解析器传入 Rust，结果拷贝回 Python 的 `list`。

### 10.3 解析与分词器

- **`SExprParser.parse`**（`runner.py` 第 163–168 行）使用 **`self.tokenizer()`**，其来自 **`hp.metta_tokenizer`**（`runner.py` 第 145–147 行；`hyperonpy.cpp` 第 1105–1106 行）。
- 因此 **`+` `1` `True` 等 token** 在 **默认环境** 下由 **Rust `CoreLibLoader`** 注册的规则解析为 **grounded 算子与值**，而非纯 Python 实现。

### 10.4 Python `stdlib` 模块的角色

`python/hyperon/stdlib.py` **第 61–86 行** 的 `@register_atoms` 主要注册 **`repr` / `parse` / `stringToChars` / `charsToString`** 等，**不包含** `+` `-` `*`。

`_priv_load_module_stdlib`（`runner.py` **第 354–356 行**）调用 **`_priv_register_module_tokens("hyperon.stdlib", ...)`**，在 **Rust 已注册核心 token 之后** 再挂载 Python 扩展（**第 372–392 行**）。

### 10.5 类型常量在 Python 中的暴露

`hyperonpy.cpp` **第 1044–1046 行**：`CAtomType` 上暴露 **`NUMBER`**、**`BOOL`**、**`STRING`** 等，供 `parse_single(...).get_grounded_type()` 等测试使用（参见 `python/tests/test_grounded_type.py` 中对 `+`、`*`、`False` 的引用）。

---

## 11. 与 `sealed` 的间接关系（算术文档边界说明）

**`sealed`** 本身定义在 **`core.rs` 第 76–113 行**，用于对表达式中的 **变量做唯一化**（除忽略列表外），与 **`stdlib.metta`** 中 `filter-atom`/`map-atom` 等组合子配合（约第 458–480 行）。

它不专门操作 **字符串类型**，但在含 **字符串原子与变量** 的模板中可用于避免变量捕获；详见 **文档 12** 中与 **`sealed`**、字符串组合子并列的说明。

---

## 12. 小结表

| MeTTa | Rust 结构体 | 主要源码行号 | 备注 |
|-------|-------------|--------------|------|
| `+` `-` `*` `%` | `SumOp` 等（宏生成） | `arithmetics.rs` 10–57, 172–181 | `promote` 后运算 |
| `/` | `DivOp` | 127–160, 178–179 | 整数除零错误 |
| `<` `>` `<=` `>=` | `LessOp` 等 | 54–57, 182–189 | 返回 `Bool` |
| `and` `or` `xor` | `AndOp` 等 | 59–96, 190–198 | `xor` 注释：Python 省略 |
| `not` | `NotOp` | 99–125, 194–195 | 一元 |
| `==` | `EqualOp` | `core.rs` 115–137, 345–346 | `Atom::PartialEq` |
| `if-equal` | `IfEqualOp` | `core.rs` 170–197, 337–338 | `atoms_are_equivalent` |
| 数字字面量 | — | `arithmetics.rs` 163–168；`number.rs` 75–83 | `i64`/`f64` |
| `True`/`False` | — | `arithmetics.rs` 169–170；`bool.rs` 全文 | `BoolSerializer` |

---

## 13. 自测与回归参考

- **算术/比较/布尔**：`arithmetics.rs` **`mod tests`** **第 201–285 行**。
- **除零**：第 218–221 行。
- **类型与 `metta` 调用**：`stdlib/mod.rs` 内大量集成测试（如第 206–207 行对 `BadType` 与 `+` 的说明）。

以上行号均相对于仓库 **`hyperon-experimental`** 当前版本；若上游移动实现，请以 `git blame` 与同名符号为准。

---

## 14. 解释器中求值路径（从应用到 grounded 结果）

本节补全「算术表达式如何真正执行」的 Rust 侧轮廓，便于与 `lib/src/metta/interpreter.rs` 对照阅读。

1. **源码进入 runner**：`CoreLibLoader::load`（`stdlib/mod.rs` **第 117–127 行**）在初始化模块时 **`register_all_corelib_tokens`**（第 97–99 行），再解析内置 **`METTA_CODE`**（`stdlib.metta`）。
2. **表达式形态**：解析后 `(+ 1 2)` 成为 **`ExpressionAtom`**，子节点为 grounded 的 **`SumOp`** 与两个 **`Number`**（由分词器产生）。
3. **Grounded 执行**：各 `*Op` 实现 **`CustomExecute::execute`**（`arithmetics.rs` 第 31–45 行等）。解释器在归约函数应用时识别 **`as_execute`** 并调用（具体分发逻辑见 `interpreter.rs` 中 `CALL_NATIVE` / grounded 操作分支，例如约第 296–307 行、第 447 行一带对特殊操作符的列举）。
4. **错误传播**：`DivOp` 返回的 **`ExecError::from("DivisionByZero")`** 会作为 MeTTa 的 **`Error`** 形式出现在结果中（与 `run_program` 测试一致，`arithmetics.rs` 第 220 行）。

Python 调用 **`metta.run("!(+ 1 2)")`** 时，不经过 Python 函数实现 `+`；**整条归约链在 Rust** 内完成，Python 仅负责 **传字符串、取回 `Atom` 列表**（`runner.py` 第 206–214 行；`hyperonpy.cpp` 第 1117–1120 行）。

---

## 15. `stdlib.metta` 中的文档字符串（交叉引用）

算术与比较运算的 **用户文档** 写在 **`lib/src/metta/runner/stdlib/stdlib.metta`** 约 **第 1311–1381 行**（`@doc +`、`-`、`*`、`/`、`%`、`<` `>` `<=` `>=`、`==`）。其中 **第 1311–1312 行** 注释说明：部分运算在 **Rust 与 Python** 双侧可能存在实现时，`help!` 类工具的行为尚不完整。阅读实现时应 **以 Rust `arithmetics.rs` / `core.rs` 为准**。

---

## 16. 常见问题（FAQ）

**Q：`xor` 在 Python 环境里能用吗？**  
A：Rust 核心注册了 **`xor`**（`arithmetics.rs` 第 197–198 行）。Python 侧注释称 **有意省略** 以便测试（第 95–96 行）；若仅加载默认核心库，MeTTa 中仍可出现 `xor` token，除非被其他模块覆盖。

**Q：`==` 与 `match` / `unify` 有何不同？**  
A：`==` 返回 **Bool** 且基于 **`Atom::PartialEq`**。`match`（`core.rs` 第 140–166 行）在空间上查询模式；`unify` 在 `stdlib.metta` 层构造，语义为合一与分支选择，与本文档范围不同。

**Q：为何文档写 Integer→Float「提升」？**  
A：术语对应 `Number::promote` 与 `NumberType::widest_type`（`number.rs` 第 85–88、116–122 行）。混合类型二元运算统一升到 **Float** 再算；**除法** 整数分支仍用整数除法（`arithmetics.rs` 第 155 行）。
