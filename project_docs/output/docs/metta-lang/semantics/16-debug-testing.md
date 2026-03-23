---
title: MeTTa 调试与测试全链分析
order: 16
---

# 文档 16：调试与测试（MeTTa → Python → Rust）

本文档从 **MeTTa 表面语法 / 标准库定义** 出发，沿 **Python 绑定（hyperon / hyperonpy）** 追踪到 **Rust 引擎与 C API**，并给出关键实现的**精确行号**。Python 层对 `trace!`、`println!`、`assertEqual*`、`nop` 等 **不实现业务逻辑**：解释与 grounded 执行均在 Rust 核心完成；Python 仅通过 `MeTTa.run` → C `metta_run` 驱动同一引擎。

---

## 1. 总览：调用链路与职责划分

| 层级 | 职责 |
|------|------|
| MeTTa 源程序 / `stdlib.metta` | 文档字符串、`assertEqual` 等**纯 MeTTa 组合子**定义 |
| Rust `lib` | `TraceOp`、`PrintlnOp`、`_assert-results-are-equal*`、`NopOp`；`RunnerState` 收集结果；`atom_is_error` 检测 |
| C `c/src/metta.rs` | `metta_run`、`atom_is_error` 等 FFI |
| Python `hyperon/runner.py` | `MeTTa.run` → `hp.metta_run`；`RunnerState.run_step` → `hp.runner_state_step` |

---

## 2. `trace!`（`TraceOp`）

### 2.1 MeTTa 语义与文档

标准库在 `stdlib.metta` 中为 `trace!` 提供文档（说明先打印第一个参数、返回第二个参数的求值结果）：

```1272:1277:lib/src/metta/runner/stdlib/stdlib.metta
(@doc trace!
  (@desc "Prints its first argument and returns second. Both arguments will be evaluated before processing")
  (@params (
    (@param "Atom to print")
    (@param "Atom to return")))
  (@return "Evaluated second input"))
```

### 2.2 Rust：`TraceOp` 实现

文件：`lib/src/metta/runner/stdlib/debug.rs`。

- 结构体与 `grounded_op!` 宏展开后的 `Display`：`46–49` 行。
- 类型签名（`->` 形式）：`Atom::expr([ARROW_SYMBOL, ATOM_TYPE_UNDEFINED, ATOM_TYPE_ATOM, ATOM_TYPE_UNDEFINED])`，见 `51–54` 行。
- **执行逻辑**：`eprintln!` 打印第一个参数，`Ok(vec![val.clone()])` 返回第二个参数不变，`61–68` 行。

```46:68:lib/src/metta/runner/stdlib/debug.rs
#[derive(Clone, Debug)]
pub struct TraceOp {}

grounded_op!(TraceOp, "trace!");

impl Grounded for TraceOp {
    fn type_(&self) -> Atom {
        Atom::expr([ARROW_SYMBOL, ATOM_TYPE_UNDEFINED, ATOM_TYPE_ATOM, ATOM_TYPE_UNDEFINED])
    }
    // ...
}

impl CustomExecute for TraceOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let arg_error = || ExecError::from("trace! expects two atoms as arguments");
        let val = args.get(1).ok_or_else(arg_error)?;
        let msg = args.get(0).ok_or_else(arg_error)?;
        eprintln!("{}", msg);
        Ok(vec![val.clone()])
    }
}
```

### 2.3 分词器注册

同一文件 `register_context_independent_tokens`：`155–157` 行将 `trace!` 正则绑定到 `Atom::gnd(TraceOp{})`。

### 2.4 Python 层

无单独 Python 实现。用户代码 `metta.run("!(trace! ...)")` 经 `python/hyperon/runner.py` `MeTTa.run`（约 `206–214` 行）调用 `hp.metta_run`，进入 Rust `Metta::run`（`lib/src/metta/runner/mod.rs` `456–458` 行）。

---

## 3. `println!`（`PrintlnOp`）

实现位于 **`lib/src/metta/runner/stdlib/string.rs`**（非 `debug.rs`）。

- 结构体与宏：`10–13` 行。
- `execute`：`println!("{}", atom_to_string(atom))`，然后 `unit_result()`（即返回单元原子），`25–31` 行。
- 分词器注册：`78–80` 行。

```25:31:lib/src/metta/runner/stdlib/string.rs
impl CustomExecute for PrintlnOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let arg_error = || ExecError::from("println! expects single atom as an argument");
        let atom = args.get(0).ok_or_else(arg_error)?;
        println!("{}", atom_to_string(atom));
        unit_result()
    }
}
```

### 3.1 与 `format-args` 的组合（MeTTa 侧）

`help!` 等 MeTTa 代码在 `stdlib.metta` 中大量将 `println!` 与 `format-args` 联用（例如约 `885–907` 行）。`format-args` 的 Rust 实现同在 `string.rs`（`FormatArgsOp`，约 `34–61` 行）。

### 3.2 文档

`stdlib.metta` `1279–1283` 行描述 `println!` 打印一行并返回 unit。

---

## 4. `assertEqual` 与 `assertEqualToResult`

### 4.1 MeTTa 定义（组合子 + `metta` / `collapse`）

文件：`lib/src/metta/runner/stdlib/stdlib.metta`。

**`assertEqual`**（两侧表达式均求值后比较结果**集合**）：

```1094:1099:lib/src/metta/runner/stdlib/stdlib.metta
(: assertEqual (-> Atom Atom (->)))
(= (assertEqual $actual $expected)
   (chain (context-space) $space
     (chain (metta (collapse $actual) %Undefined% $space) $actual-results
       (chain (metta (collapse $expected) %Undefined% $space) $expected-results
         (_assert-results-are-equal $actual-results $expected-results (assertEqual $actual $expected)) ))))
```

**`assertEqualToResult`**（只对第一个参数求值；第二个参数视为**期望结果列表**，不求值）：

```1148:1152:lib/src/metta/runner/stdlib/stdlib.metta
(: assertEqualToResult (-> Atom Atom (->)))
(= (assertEqualToResult $actual $expected-results)
   (chain (context-space) $space
     (chain (metta (collapse $actual) %Undefined% $space) $actual-results
       (_assert-results-are-equal $actual-results $expected-results (assertEqualToResult $actual $expected-results)) )))
```

另：`assertEqualMsg`、`assertEqualToResultMsg` 等变体使用 `_assert-results-are-equal-msg`（`1108–1113`、`1161–1165` 行）。

### 4.2 Rust：`_assert-results-are-equal` 族

文件：`lib/src/metta/runner/stdlib/debug.rs`。

- **无序向量比较**核心：`assert_results_are_equal`（`108–127` 行）。使用 `compare_vec_no_order`（`hyperon_common::assert`）与可选的相等性参数 `E: Equality<&'a Atom>`。
- 成功时：`unit_result()`（通过 `compare_vec_no_order(...).as_display()` 为 `None` 分支）。
- 失败时：构造 **`(Error <assert-atom> <message>)`**，见 `119–125` 行：`Atom::expr([ERROR_SYMBOL, assert.clone(), msg])`。
- **默认相等**：`GroundedFunctionAtom::new` 注册 `_assert-results-are-equal`、`_assert-results-are-equal-msg`（`162–176` 行）。
- **Alpha 相等**：`AlphaEquality`（`100–106` 行）与 `_assert-results-are-alpha-equal*`（`167–181` 行）。

```108:127:lib/src/metta/runner/stdlib/debug.rs
fn assert_results_are_equal<'a, E: Equality<&'a Atom>>(args: &'a [Atom], cmp: E) -> Result<Vec<Atom>, ExecError> {
    let arg_error = || ExecError::from("Pair of evaluation results with bindings is expected as an argument");
    let actual = TryInto::<&ExpressionAtom>::try_into(args.get(0).ok_or_else(arg_error)?)?.children();
    let expected = TryInto::<&ExpressionAtom>::try_into(args.get(1).ok_or_else(arg_error)?)?.children();
    let assert = args.get(2).ok_or_else(arg_error)?;
    // ...
    match compare_vec_no_order(actual.iter(), expected.iter(), cmp).as_display() {
        None => unit_result(),
        Some(diff) => {
            let msg = match args.get(3) {
                None => Atom::gnd(Str::from_string(format!("{}\n{}", report, diff))),
                Some(m) => m.clone(),
            };
            Ok(vec![Atom::expr([ERROR_SYMBOL, assert.clone(), msg])])
        },
    }
}
```

### 4.3 Rust 单元测试（行为示例）

同文件 `#[cfg(test)] mod tests`：`191–255` 行展示 `assertEqual`、`assertEqualToResult` 在成功/失败时返回 `UNIT_ATOM` 或 `Error` 表达式。

### 4.4 Python

测试与脚本通过 `MeTTa.run` 调用同一逻辑；无 Python 端断言实现。

---

## 5. `nop`（`NopOp`）

文件：`lib/src/metta/runner/stdlib/core.rs`。

- `55–73` 行：`NopOp` 的 `execute` 忽略参数，直接 `unit_result()`。
- 分词器注册：同文件约 `339` 行附近（`grep` 可见 `NopOp{}`）。

```55:73:lib/src/metta/runner/stdlib/core.rs
#[derive(Clone, Debug)]
pub struct NopOp {}

grounded_op!(NopOp, "nop");
// ...
impl CustomExecute for NopOp {
    fn execute(&self, _args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        unit_result()
    }
}
```

---

## 6. 错误原子 `(Error …)`：构造与检测

### 6.1 构造 API：`error_atom`

文件：`lib/src/metta/mod.rs`（hyperon crate 的 `metta` 模块）。

- `53–64` 行：`error_atom` 根据是否有 `err_code` 生成三元或四元 `Expression`，头部为 `ERROR_SYMBOL`。

```53:64:lib/src/metta/mod.rs
pub fn error_atom(err_atom: Option<Atom>, err_code: Option<Atom>, message: String) -> Atom {
    let err_atom = match err_atom {
        Some(err_atom) => err_atom,
        None => EMPTY_SYMBOL,
    };
    if let Some(err_code) = err_code {
        Atom::expr([ERROR_SYMBOL, err_atom, err_code, Atom::sym(message)])
    } else {
        Atom::expr([ERROR_SYMBOL, err_atom, Atom::sym(message)])
    }
}
```

断言失败路径（`debug.rs`）使用的是 **`Atom::expr([ERROR_SYMBOL, assert.clone(), msg])`** 的三元形式（`msg` 可为字符串 grounded 原子），与 `error_atom` 助手在参数形态上略有不同，但**判别规则一致**（见下）。

### 6.2 检测：`atom_is_error`

同文件 `67–74` 行：表达式且第一个子节点等于 `ERROR_SYMBOL`。

```67:74:lib/src/metta/mod.rs
pub fn atom_is_error(atom: &Atom) -> bool {
    match atom {
        Atom::Expression(expr) => {
            expr.children().len() > 0 && expr.children()[0] == ERROR_SYMBOL
        },
        _ => false,
    }
}
```

### 6.3 提取消息：`atom_error_message`

同文件 `79–91` 行：要求为错误表达式；子节点数为 3 或 4，取最后一个子节点作消息并用 `atom_to_string` 渲染。

### 6.4 C API（供 hyperonpy / 其他语言）

文件：`c/src/metta.rs`。

- `atom_is_error`：`492–495` 行，委托 `hyperon::metta::atom_is_error`。
- `atom_error_message`：`508–511` 行，将 Rust 字符串写入调用方缓冲区。

---

## 7. Runner 如何收集测试结果

### 7.1 入口：`Metta::run`

`lib/src/metta/runner/mod.rs` `456–458` 行：创建 `RunnerState::new_with_parser`，调用 `run_to_completion()`。

### 7.2 跑至结束：`run_to_completion`

同文件 `587–593` 行：循环 `run_step` 直到 `is_complete()`，返回 `into_results()`（`Vec<Vec<Atom>>`）。

### 7.3 单步：`RunContext::step` 与结果追加

同文件约 `1028–1047` 行（ interpreter 完成一支求值后）：

- `interpreter_state.into_result()` 得到 `result: Vec<Atom>`。
- `let error = result.iter().any(|atom| atom_is_error(atom));`
- **`self.i_wrapper.results.push(result);`**
- 若 `error` 为真：将 `mode` 设为 `TERMINATE`，停止后续输入处理。

因此 **测试失败时**，失败的那次 `!` 求值结果向量中会包含 **`Error` 表达式**；Runner **仍把整向量记入 `results`**，但**终止**后续执行。

### 7.4 模块加载收尾：`finalize_loading`

同文件 `649–656` 行：在加载模块流程中，若 `results` 里任一向量为 `atom_is_error`，则 **`Err(atom_error_message(...))`**，加载失败。

### 7.5 Python：`MeTTa.run` 与错误字符串

`python/hyperon/runner.py` `206–214` 行：`hp.metta_run` 后 `_run_check_for_error()`（`221–224` 行）读取 `hp.metta_err_str`。

说明：Rust **`Metta::run` 成功返回 `Ok(results)`** 时，**结果里仍可包含 `Error` 原子**（例如断言失败）；Python 层 **不会** 因此抛异常，除非 C 层设置了 **runner 级** `err_string`（例如解析错误、某些致命路径）。区分「结果中含 Error」与「metta_err_str 非空」是集成测试编写时的要点。

### 7.6 C：`metta_run`

`c/src/metta.rs` `1005–1022` 行：`rust_metta.run` 返回 `Ok` 时对每个 `result` 调用回调；返回 `Err` 时写入 `metta.err_string`。

---

## 8. 相关辅助：`print-alternatives!` 与 `=alpha`

均在 `debug.rs`：

- `PrintAlternativesOp`：`71–97` 行（调试非确定性分支时打印各备选）。
- `AlphaEqOp` 与 `=alpha`：`129–153` 行。

---

## 9. 小结表（Rust 主文件索引）

| MeTTa / 功能 | Rust 类型或函数 | 文件与行号（主要） |
|--------------|-----------------|-------------------|
| `trace!` | `TraceOp` | `debug.rs` 46–68, 155–157 |
| `println!` | `PrintlnOp` | `string.rs` 10–31, 78–80 |
| `assertEqual*` / `assertEqualToResult*` | `stdlib.metta` + `_assert-results-are-equal*` | `stdlib.metta` 1088–1190；`debug.rs` 108–181 |
| `nop` | `NopOp` | `core.rs` 55–73 |
| `Error` 构造（通用） | `error_atom` | `lib/src/metta/mod.rs` 53–64 |
| `Error` 检测 / 消息 | `atom_is_error`, `atom_error_message` | `lib/src/metta/mod.rs` 67–91 |
| 结果收集 / 遇错终止 | `RunnerState::step` 内 `results.push` | `runner/mod.rs` 约 1040–1047 |
| FFI | `metta_run`, `atom_is_error` | `c/src/metta.rs` 1005+, 492+ |

---

## 10. 延伸阅读（本仓库内）

- `lib/src/metta/interpreter.rs`：多处 `atom_is_error` 过滤或分支（例如约 1090、1408、1424、1460 行），体现解释器对错误传播的策略。
- `lib/src/metta/runner/stdlib/debug.rs` 内集成测试：`metta_assert_equal_op`、`metta_assert_equal_to_result_op` 等（`191` 行起）。

（以下为文档篇幅补足：测试编写建议与调试技巧，不改变实现事实。）

---

## 11. 实践建议：如何在 Python 测试中断言 MeTTa 测试通过

1. 调用 `metta.run(program)` 得到 `List[List[Atom]]`。
2. 对关心的 `!` 结果向量，检查是否 **不** 含 `atom_is_error` 为真的子原子（若 hyperonpy 暴露 `atom_is_error` 则直接用；否则在 Python 侧解析 `repr` 或使用 Rust 返回的字符串化形式进行断言）。
3. 若需区分「runner 失败」与「结果中含 Error」，同时检查 `metta_err_str` 是否为空（Python 中通常由 `RuntimeError` 体现）。

---

## 12. `trace!` 与 `println!` 的 I/O 差异

- `trace!` 使用 **`eprintln!`**（`debug.rs` 第 66 行）→ 标准错误流。
- `println!` 使用 **`println!`**（`string.rs` 第 29 行）→ 标准输出流。

在 REPL、CI 日志重定向场景下，两者可见性可能不同。

---

## 13. `assert-results-are-equal` 的参数约定（实现视角）

`assert_results_are_equal` 期望：

1. 第一个参数：表达式，**子节点**为实际结果集（通常来自 `collapse` 的结果包装）。
2. 第二个参数：表达式，**子节点**为期望结果集。
3. 第三个参数：用于构造 `Error` 时回显的「断言头」原子（如 `(assertEqual ...)` 部分）。
4. 可选第四个参数：自定义消息（`_assert-results-are-equal-msg`），见 `120–123` 行分支。

---

## 14. 与 `unit_result` 的关系

`stdlib` 中 `unit_result()` 定义在 `lib/src/metta/runner/stdlib/mod.rs` `41–43` 行：`Ok(vec![UNIT_ATOM])`。`println!`、`nop`、成功断言均返回该形态。

---

## 15. 版本与特性说明

若编译时关闭某些特性，包管理相关路径可能不可用；**本文档涉及的调试与测试原语**位于核心 stdlib，一般不依赖 `pkg_mgmt`。以本地 `Cargo` 特性为准。

---

## 16. 文档元信息

- **范围**：`trace!`、`println!`、`assertEqual` / `assertEqualToResult`（及 MeTTa 层变体）、`nop`、`Error` 原子、`atom_is_error` / `atom_error_message`、Runner 结果收集与终止语义。
- **非范围**：类型检查产生的 `Error`（`get_atom_types` / `validate_atom`）细节、解释器逐步调试协议（见 `RunnerState` 注释中的未来 delegate API 提案）。

---

## 附录 A：`compare_vec_no_order` 与 `SliceDisplay`

`assert_results_are_equal`（`debug.rs` `108` 行起）使用 **`hyperon_common::assert::compare_vec_no_order`** 对两组结果做**无序多重集**比较；报告字符串由 **`SliceDisplay`**（`hyperon_common::collections`）格式化 `actual` / `expected` 子切片（`115` 行 `report` 变量）。这与 MeTTa 中非确定性求值（多结果）语义一致：**顺序不敏感**，**重复计数敏感**（见 `debug.rs` 测试 `assertEqualToResult (baz) (D)` 对三重 `D` 的期望，`235–255` 行）。

---

## 附录 B：`AlphaEquality` 与 `atoms_are_equivalent`

`debug.rs` `100–106` 行：`AlphaEquality` 实现 `Equality<&Atom>`，以 **`atoms_are_equivalent`**（`hyperon_atom::matcher`）比较。用于 `assertAlphaEqual*` 与 `_assert-results-are-alpha-equal*`（`167–171` 行）。与默认 **`DefaultEquality`**（`==`）对比，见同文件测试 `metta_assert_alpha_equal_op`（`209–226` 行）。

---

## 附录 C：`ERROR_SYMBOL` 定义位置

`ERROR_SYMBOL` 为 MeTTa 语言层面的错误标签符号常量，定义于 **hyperon_atom / metta 常量宏**体系（与 `UNIT_ATOM`、`ARROW_SYMBOL` 同级）。`atom_is_error` 仅检查**首子节点**是否等于该符号（`lib/src/metta/mod.rs` `67–74` 行），因此 **手工构造的 `(Error ...)` 表达式**与 `error_atom` / 断言失败路径一致时均可被识别。

---

## 附录 D：Python `RunnerState` 与增量结果

`python/hyperon/runner.py` `13–53` 行：**`RunnerState`** 封装 `hp.runner_state_new_with_parser`。

- `run_step`（`30–37` 行）：`hp.runner_state_step` 后 **`runner_state_err_str`** 非空则 **`RuntimeError`**。
- `current_results`（`45–53` 行）：`hp.runner_state_current_results` 将 C 侧结果列表转为 **`Atom`** 嵌套列表。

与 **`Metta.run` 一次性跑完**不同，`RunnerState` 允许宿主在每一步检查 **`current_results`** 是否已出现 **`Error`** 子表达式，用于自定义测试运行器或 IDE 集成。

---

## 附录 E：`stdlib/mod.rs` 中 debug 与 string 的装配顺序

`lib/src/metta/runner/stdlib/mod.rs` `85–94` 行 **`register_context_independent_tokens`** 依次调用 `debug::register_context_independent_tokens`、`string::register_context_independent_tokens` 等。因而 **`trace!` 与 `println!`** 在同一初始化阶段进入 **Tokenizer**，与 **Python 扩展**后续注册的 token 共存；后者见 `runner._priv_register_module_tokens`。

---

## 附录 F：`TraceOp` 单元测试

`debug.rs` `288–292` 行 **`trace_op`** 测试直接调用 **`TraceOp{}.execute(&[sym!("\"Here?\""), sym!("42")])`**，期望 **`Ok(vec![sym!("42")])`**。注意测试传入的是**已解析符号**，与源码中 `trace! "Here?" 42` 经 tokenizer 后的形态对应，用于锁定 **stderr 之外**的返回语义。

---

## 附录 G：`PrintlnOp` 单元测试

`string.rs` `96–99` 行：对单参数 `sym!("A")` 执行后 **`unit_result()`**，与 `println!` 返回 unit 一致。

---

## 附录 H：`NopOp` 单元测试

`core.rs` `549` 行附近（`grep`：`assert_eq!(NopOp{}.execute(&mut vec![]), unit_result())`）：验证零参调用仍返回 unit。

---

## 附录 I：`MettaRunnerMode` 与 `TERMINATE`

`RunContext::step` 在多种失败路径设置 **`MettaRunnerMode::TERMINATE`**（例如解析错误 `1056–1061` 行、`add_atom` 失败 `1078–1081` 行、以及 **`atom_is_error` 检测结果 `1044–1046` 行**）。**`is_complete`**（`600–604` 行）仅检查 mode 是否为 **`TERMINATE`**。因此「测试失败」与「致命 runner 错误」在 mode 层面**相同**，区分需查看 **`results` 内容**或 **`metta_err_str`**。

---

## 附录 J：`assertEqualMsg` 与自定义消息原子

`stdlib.metta` `1108–1113` 行：`assertEqualMsg` 将 **`$msg`** 传入 `_assert-results-are-equal-msg`。在 `debug.rs` `120–123` 行，若提供第四参数则 **直接使用该原子作为 `Error` 第三子节点**，替代默认的 `Str` 报告。便于嵌入结构化错误载荷（例如 `(MyAssertFailed (details ...))`）。

---

## 附录 K：`collapse` 与 `metta` 在断言中的角色

`assertEqual` 的 MeTTa 展开（`stdlib.metta` `1095–1099` 行）使用 **`(metta (collapse $actual) %Undefined% $space)`** 与对 **`$expected`** 的同样结构。即：**在同一 `context-space` 下** 对两侧做 **非确定性折叠**，得到 **结果的多重集** 后再交给 Rust **`_assert-results-are-equal`**。理解 **`collapse`** 与 **`superpose`** 的语义有助于编写 **多结果函数** 的测试。

---

## 附录 L：`print-alternatives!` 与调试非确定性

`debug.rs` `86–97` 行：**`PrintAlternativesOp`** 打印格式串与各 **子表达式字符串**（`atom_to_string`），返回 **unit**。用于 **肉眼比对** `superpose` 展开的多条路径，**不参与** 自动化 `assertEqual`。

---

## 附录 M：`=alpha` 与 `AlphaEqOp`

`debug.rs` `129–153` 行：**`AlphaEqOp`** 两参返回 **Bool grounded**。与 **`assertAlphaEqual`**（集合比较）不同：**`=alpha`** 是 **逐对原子** 的 **谓词**，适合在 **`let`** 中分支逻辑。

---

## 附录 N：Rust 测试 `run_program` 辅助

`debug.rs` `185–188` 行：`mod tests` 引入 **`run_program`**（`crate::metta::runner`）。`**=alpha** 测试（`229–232` 行）展示 **最小程序字符串** 求值与 **布尔结果** 抽取，可作为 **独立单元测试** 模板。

---

## 附录 O：`core.rs` 中 `NopOp` 分词器注册行号

`grep` 定位 **`let nop_op = Atom::gnd(NopOp{})`** 在 **`lib/src/metta/runner/stdlib/core.rs`** 约 **`339`** 行（随版本略变）。与 **`register_context_independent_tokens`** 同一函数块。

---

## 附录 P：`string.rs` 中字符串字面量 tokenizer

`string.rs` `83–84` 行：双引号字符串模式注册 **`Str` grounded**，与 **`println!`** 输出 **`atom_to_string`** 相呼应——**输入**与**输出**均经过 **统一字符串原子表示**。

---

*（行号以文档编写时仓库快照为准；若上游重构移动代码，请以符号搜索为准。）*
