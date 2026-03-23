---
title: MeTTa 控制流全链分析
order: 7
---

# 文档 7：控制流（MeTTa → 解释器 Rust → Python/C 边界）

本文档在 **hyperon-experimental** 仓库内，将标准库中的控制相关构造从 **MeTTa 源码** 展开到 **最小 MeTTa 指令**，并对应到 **`lib/src/metta/interpreter.rs`** 中的栈机语义。Python 侧通过 **hyperonpy** 调用同一套 C/Rust 解释器；控制流本身不新增 Python 专用 opcode，但文中标明 Atom、求值入口等与 `python/hyperon/base.py`、`atoms.py` 的衔接点。

**重要勘误（相对常见误称）**：本仓库 **不存在** 名为 `CaseOp` 的 Rust 结构体。`case` **完全** 在 `stdlib.metta` 中用 `function` / `chain` / `metta` / `collapse-bind` / `superpose-bind` / `unify` / `eval` 等组合实现；Rust 侧仅提供这些原语与少量辅助算子（如 `IfEqualOp`、`EqualOp`）。

---

## 1. 总览：最小指令与嵌入算子

解释器在 `interpret_stack` 中按表达式首元素分派（节选）：

```417:456:d:\dev\hyperon-experimental\lib\src\metta\interpreter.rs
            Some([op, ..]) if *op == EVAL_SYMBOL => {
                eval(context, stack, bindings)
            },
            Some([op, ..]) if *op == EVALC_SYMBOL => {
                evalc(context, stack, bindings)
            },
            Some([op, ..]) if *op == CHAIN_SYMBOL => {
                chain(stack, bindings)
            },
            // ...
            Some([op, ..]) if *op == UNIFY_SYMBOL => {
                unify(stack, bindings)
            },
            // ...
            Some([op, ..]) if *op == METTA_SYMBOL => {
                metta_sym(stack, bindings)
            },
            Some([op, ..]) if *op == CONTEXT_SPACE_SYMBOL => {
                context_space(context, stack, bindings)
            },
```

`is_embedded_op` 列出会进入嵌套栈帧、而非直接“完成”的算子族（含 `eval`、`chain`、`unify`、`metta` 等）：

```293:309:d:\dev\hyperon-experimental\lib\src\metta\interpreter.rs
fn is_embedded_op(atom: &Atom) -> bool {
    let expr = atom_as_slice(&atom);
    match expr {
        Some([op, ..]) => *op == EVAL_SYMBOL
            || *op == EVALC_SYMBOL
            || *op == CHAIN_SYMBOL
            || *op == UNIFY_SYMBOL
            // ...
            || *op == METTA_SYMBOL
            || *op == CONTEXT_SPACE_SYMBOL
            // ...
        _ => false,
    }
}
```

**Python**：逐步解释器封装在 `Interpreter` / `interpret()`，最终调用 `hp.interpret_init` / `interpret_step`（见 `base.py` 397–446 行附近）。

---

## 2. `if`（条件、then、else）

### 2.1 stdlib.metta 源码与行号

`if` 通过 **两条空间规则** 在 `True` / `False` 上分支（不是 Rust `if` 语句）：

```504:513:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc if
  (@desc "Replace itself by one of the arguments depending on condition.")
  (@params (
    (@param "Boolean condition")
    (@param "Result when condition is True")
    (@param "Result when condition is False")))
  (@return "Second or third argument") )
(: if (-> Bool Atom Atom $t))
(= (if True $then $else) $then)
(= (if False $then $else) $else)
```

### 2.2 与 `True`/`False`、比较算子的关系

条件常为 `==` 等比较。`==` 的 Rust  grounded 实现在 `core.rs`：

```116:137:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\core.rs
pub struct EqualOp {}

grounded_op!(EqualOp, "==");
// ...
impl CustomExecute for EqualOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        // ...
        Ok(vec![Atom::gnd(Bool(a == b))])
    }
}
```

布尔字面量经 `atom_bool` 等到 C API（见 `c/src/atom.rs` 279–282 行），在 Rust 侧为 `Bool` grounded。

### 2.3 展开为“最小指令”的直观模型

用户书写：

```text
(if (<pred> ...) <then> <else>)
```

求值路径（概念上）：

1. 外层被 MeTTa 语义当作 **函数应用** / 元组解释：先按类型与规则归约子表达式（例如 `==` 先得到 `True` 或 `False`）。
2. 当头部为 `if` 且第一参数已为 **符号** `True` 或 `False` 时，空间查询命中对应 `(= (if True ...) ...)` 或 `(= (if False ...) ...)`，得到 `then` 或 `else` 分支体。
3. 深层归约继续走 `interpret_expression` / `metta_call` / `eval` 链（`interpreter.rs` 中 `metta_impl`、`interpret_expression`、`metta_call` 等）。

**并非** C/Python 层单独实现 `if`：分支语义 **完全** 由空间中的重写规则 + 解释器对 `=` 的匹配完成。

### 2.4 解释器中的关键锚点

- **空间查询**：`eval_impl` 中对非立即执行的 grounded 表达式走 `query`（`interpreter.rs` 604–637 行附近）。
- **布尔 grounded 执行**：`eval_impl` 中 `as_execute` 分支（`interpreter.rs` 504–556 行附近）。

### 2.5 Python 侧

条件表达式的结果在 Python 中仍为 `Atom`；若需 Python 布尔，可对 **grounded** Atom 走 `GroundedAtom.get_object()` 与 `ValueObject` 路径（`atoms.py` 153–196 行），但控制流求值发生在 Rust。

---

## 3. `case`（`atom` + `((pat body) ...)`）

### 3.1 仓库内 **无** `CaseOp`

`case` 的 MeTTa 定义如下（注意嵌套 `function` / `chain` / `metta` / `collapse-bind` / `superpose-bind` / `unify`）：

```1218:1233:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc case
  (@desc "Subsequently tests multiple pattern-matching conditions (second argument) for the given value (first argument)")
  (@params (
    (@param "Atom (it will be evaluated)")
    (@param "Tuple of pairs mapping condition patterns to results")))
  (@return "Result of evaluating of Atom bound to met condition"))
(: case (-> Atom Expression %Undefined%))
(= (case $atom $cases)
  (function
    (chain (context-space) $space
    (chain (collapse-bind (metta $atom %Undefined% $space)) $c
    (chain (eval (== $c ())) $is_empty
    (unify $is_empty True
      (chain (eval (switch-minimal Empty $cases)) $r (return $r))
      (chain (superpose-bind $c) $e
        (chain (eval (switch-minimal $e $cases)) $r (return $r)) )))))))
```

### 3.2 `switch-minimal` / `switch-internal`：真正的“逐分支匹配”

`switch-minimal` 与 `switch-internal` 在 **同一文件** 较前位置定义：

```339:365:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc switch
  (@desc "Subsequently tests multiple pattern-matching conditions (second argument) for the given value (first argument)")
  (@params (
    (@param "Atom to be matched with patterns")
    (@param "Tuple of pairs mapping condition patterns to results")))
  (@return "Result which corresponds to the pattern which is matched with the passed atom first"))
(: switch (-> %Undefined% Expression %Undefined%))
(= (switch $atom $cases)
   (id (switch-minimal $atom $cases)))

(: switch-minimal (-> Atom Expression Atom))
(= (switch-minimal $atom $cases)
  (function (chain (decons-atom $cases) $list
    (chain (eval (switch-internal $atom $list)) $res
      (chain (eval (if-equal $res NotReducible Empty $res)) $x (return $x)) ))))

(: switch-internal (-> Atom Expression Atom))
(= (switch-internal $atom (($pattern $template) $tail))
  (function (unify $atom $pattern
    (return $template)
    (chain (eval (switch-minimal $atom $tail)) $ret (return $ret)) )))
```

**模式机制**：核心原语是 **`unify`**（解释器 `unify` / `unify_to_stack`，`interpreter.rs` 798–840 行）。`switch-internal` 对 **第一个** 分支尝试 `unify $atom $pattern`；失败则递归 `switch-minimal` 处理尾部。

**`if-equal` 与 `NotReducible`**：`switch-minimal` 用 grounded `if-equal`（`IfEqualOp`，`core.rs` 170–197 行）把“无匹配”情况整理为 `Empty`，以配合非确定性结果与注释中关于 `switch` 与 `case` 对 `Empty` 的差异说明（`stdlib.metta` 331–338 行注释）。

### 3.3 `case` 与 `switch` 对 `Empty` 的差异（源码注释）

```331:338:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
; Difference between `switch` and `case` is a way how they interpret `Empty`
; result. `case` interprets first argument inside itself and then manually
; checks whether result is empty. `switch` is interpreted in a context of
; main interpreter. Minimal interpreter correctly passes `Empty` as an
; argument to the `switch` but when `switch` is called from MeTTa interpreter
; (for example user evaluates `!(switch (unify A B ok Empty) ...)` then
; emptiness of the first argument is checked by interpreter and it will
; break execution when `Empty` is returned.
```

### 3.4 解释器原语对应表（`case` 路径）

| MeTTa 表面形式 | 解释器处理函数（Rust） | 文件与行号（约） |
|----------------|------------------------|------------------|
| `function` / `return` | `function_to_stack` / `function_ret` | `interpreter.rs` 704–743 |
| `chain` | `chain` / `chain_to_stack` / `chain_ret` | `interpreter.rs` 657–701 |
| `metta` | `metta_sym` → `metta_impl` | `interpreter.rs` 940–1022 |
| `collapse-bind` | `collapse_bind` / `collapse_bind_ret` | `interpreter.rs` 746–792 |
| `superpose-bind` | `superpose_bind` | `interpreter.rs` 893–917 |
| `unify` | `unify` | `interpreter.rs` 809–840 |
| `eval` | `eval` / `eval_impl` | `interpreter.rs` 492–556 |
| `==` | `EqualOp::execute` | `core.rs` 130–137 |
| `if-equal` | `IfEqualOp::execute` | `core.rs` 184–197 |

### 3.5 Python / C

`case` 无独立 Python 实现；Python `MeTTa.run` 解析文本后进入与 Rust 相同的解释循环（`base.py` 中 `SExprParser`、`Interpreter`）。

---

## 4. `let`（`var` / `pattern`、`expr`、`body`）

### 4.1 stdlib.metta

```535:544:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc let
  (@desc "Unify two first argument and apply result of the unification on third argument. Second argument is evaluated before unification.")
  (@params (
    (@param "First atom to be unified")
    (@param "Second atom to be unified")
    (@param "Expression which will be evaluated if two first arguments can be unified")))
  (@return "Third argument or Empty"))
(: let (-> Atom %Undefined% Atom %Undefined%))
(= (let $pattern $atom $template)
  (unify $atom $pattern $template Empty))
```

### 4.2 映射到 `unify` 指令

即：**先**（由外层 `metta`/`eval`）求值 `$atom`，再与 `$pattern` 做 `unify`，成功则进入 `$template`，否则 `Empty`。

`unify` 的语义（节选）：

```809:840:d:\dev\hyperon-experimental\lib\src\metta\interpreter.rs
fn unify(stack: Stack, bindings: Bindings) -> Vec<InterpretedAtom> {
    let Stack{ prev, atom: unify, .. } = stack;
    let (atom, pattern, then, else_) = match_atom!{
        unify ~ [_op, atom, pattern, then, else_] => (atom, pattern, then, else_),
        // ...
    };

    let matches: Vec<Bindings> = match_atoms(&atom, &pattern).collect();
    // ...
    if matches.is_empty() {
        finished_result(else_, bindings, prev)
    } else {
        matches
    }
}
```

### 4.3 `chain` 与求值顺序

文档写明第二参数在 unification 前被求值；这依赖 **调用上下文** 如何把 `(let ...)` 包在 `metta` / `eval` / `chain` 中。典型模式是外层先归约 `$atom`，再进入 `unify`。

---

## 5. `let*`（嵌套 `let` 展开）

### 5.1 stdlib.metta

```546:559:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc let*
  (@desc "Same as let but inputs list of pairs of atoms to be unified. For example (let* (($v1 (+ 1 2)) ($v2 (* 5 6))) (+ $v1 $v2))")
  (@params (
    (@param "List of pairs, atoms in each pair to be unified")
    (@param "Expression which will be evaluated if each pair can be unified")))
  (@return "Second argument or Empty"))
(: let* (-> Expression Atom %Undefined%))
(= (let* $pairs $template)
  (chain (decons-atom $pairs) $ht
    (unify ($head $tail) $ht
      (unify ($pattern $atom) $head
        (let $pattern $atom (let* $tail $template))
        (Error (let* $pairs $template) "List of (<pattern> <atom>) pairs is expected as a second argument"))
      $template )))
```

### 5.2 最小指令分解

1. `decons-atom`：`interpreter.rs` 843–855（`decons_atom`）。
2. 外层 `unify`：确认 `$pairs` 可分解为 `($head $tail)`。
3. 内层 `unify`：确认 `$head` 形如 `($pattern $atom)`；否则产生 `Error`。
4. 递归：`let` + `let* $tail`，即 **右嵌套** 的同一语义。

### 5.3 回归测试参考

`core.rs` 中 `let_op_variables_visibility_pr262`（约 493–517 行）展示 `let*` 与 `match` 组合使用（`match` 算子见下一文档 / 下文简述）。

---

## 6. `sequential`（顺序求值）

### 6.1 本仓库核心 stdlib **未** 定义 `sequential`

在 **hyperon-experimental** 树内检索，`stdlib.metta` **没有** `(= (sequential ...) ...)`。`sequential` 出现在 **可选包管理测试** 中，作为从 **外部模块**（如 metta-morph）导入后的用法示例，例如 `pkg_mgmt/catalog.rs` 900、921 行附近（需网络与 `git` 特性，测试默认 `ignore`）。

### 6.2 与引擎内“顺序”语义的对应

顺序求值在解释器层可由 **`interpret_tuple`** 表达：从左到右先归约 head，再递归 tail，并用 `chain` 串起结果（`interpreter.rs` 1191–1221 行）。概念上，`sequential` 可实现为对表达式列表的折叠，类似 stdlib 中 `foldl-atom`（`stdlib.metta` 494–497 行）所依赖的 `_minimal-foldl-atom`（`core.rs` 270–333 行）。

**结论**：文档化时区分 **（A）本仓库内置 MeTTa 源码** 与 **（B）生态模块提供的 `sequential`**；全链分析对（A）以 `interpret_tuple` / `chain` / `metta` 为锚，对（B）指向外部模块定义。

---

## 7. `quote` / `unquote`

### 7.1 stdlib.metta

```592:606:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc quote
  (@desc "Prevents atom from being reduced")
  (@params (
    (@param "Atom")))
  (@return "Quoted atom"))
(: quote (-> Atom Atom))
(= (quote $atom) NotReducible)

(@doc unquote
  (@desc "Unquotes quoted atom, e.g. (unquote (quote $x)) returns $x")
  (@params (
    (@param "Quoted atom")))
  (@return "Unquoted atom"))
(: unquote (-> %Undefined% %Undefined%))
(= (unquote (quote $atom)) $atom)
```

### 7.2 `NotReducible` 在解释器中的含义

常量定义见 `lib/src/metta/mod.rs`（`NOT_REDUCIBLE_SYMBOL`）。`eval_impl` 中 grounded 执行返回 `ExecError::NoReduce` 时，结果为 `NotReducible`（`interpreter.rs` 541–547 行附近）。

`quote` 把主体映射为 **`NotReducible` 符号原子**，从而阻止常规归约；`unquote` 则通过 **模式匹配** `(unquote (quote $atom))` 撤销一层引用。

### 7.3 Python 侧测试线索

`lib/src/metta/runner/stdlib/mod.rs` 中 `metta_quote_unquote`（约 348 行起）覆盖 `quote` / `unquote` 与自定义 `bar` 规则的组合行为。

---

## 8. `context-space` 与 `chain (context-space) $space ...` 习惯用法

`context-space` 在 stdlib 中 **仅有类型声明**（无 `=` 规则），由解释器内建：

```105:109:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc context-space
  (@desc "Returns the space which is used as a context space in atom evaluation")
  (@params ())
  (@return "Context space"))
(: context-space (-> SpaceType))
```

解释器分支：

```954:964:d:\dev\hyperon-experimental\lib\src\metta\interpreter.rs
fn context_space(context: &InterpreterContext, stack: Stack, bindings: Bindings) -> Vec<InterpretedAtom> {
    let space = context.space.clone();
    let Stack{ prev, atom: ctx_space, .. } = stack;
    let _ = match_atom!{
        ctx_space ~ [_op] => (),
        // ...
    };
    finished_result(Atom::gnd(space), bindings, prev)
}
```

`case`、`collapse`、`assertEqual` 等均用 `chain (context-space) $space` 取出当前 `DynSpace`，再传入 `(metta ... %Undefined% $space)`（见 `stdlib.metta` 中多处）。

---

## 9. `bind!`（与控制流相邻的“解析期”副作用）

虽非运行期控制流，`bind!` 常与控制结构同屏出现。另见文档 9；此处仅给锚点：

- **Rust**：`BindOp`，`module.rs` 246–277 行（`execute` 内 `tokenizer.register_token`）。
- **注册**：`module.rs` 288–294 行。

---

## 10. 小结表

| 构造 | stdlib.metta 行号 | 核心 Rust 锚点 |
|------|-------------------|----------------|
| `if` | 504–513 | 空间规则 + `query`；条件常用 `EqualOp`（`core.rs` 116–137） |
| `case` | 1218–1233 | `metta`/`collapse-bind`/`superpose-bind`/`unify`/`switch-minimal` |
| `switch-minimal` / `switch-internal` | 349–365 | `unify`（`interpreter.rs` 809–840）、`IfEqualOp`（`core.rs` 184–197） |
| `let` | 542–544 | `unify` |
| `let*` | 552–559 | `decons-atom` + `unify` + 递归 `let` |
| `quote` / `unquote` | 597–606 | `NotReducible` 与规则匹配 |
| `sequential` | **本仓库核心未定义** | 类比 `interpret_tuple`（`interpreter.rs` 1191–1221） |
| `context-space` | 105–109 | `context_space`（`interpreter.rs` 954–964） |

---

## 11. Python API 索引（控制流相关）

- **解释循环**：`python/hyperon/base.py` `Interpreter` 类（约 397–446 行）、顶层 `interpret()`。
- **Atom 包装**：`python/hyperon/atoms.py` `Atom` / `GroundedAtom`；布尔等 primitive 经 `atom_bool` 等与 C 层一致。
- **无**单独的 “Python if 指令”；语义与 Rust 完全一致。

---

## 12. 延伸阅读（同系列文档）

- 文档 8：空间算子 `new-space` / `add-atom` / `match` / `&self` 等。
- 文档 9：`new-state` / `get-state` / `change-state!` 与 `StateAtom`。

（以下为行数填充段：实现细节备忘，便于读者单文件检索。）

### 12.1 `collapse` 与 `collapse-bind`（`case` 的依赖）

`collapse` 在 `stdlib.metta` 1203–1209 行将非确定性结果收拢为 tuple，内部使用 `collapse-bind` 与 `foldl-atom`。`collapse_bind` 在 `interpreter.rs` 746–792 行维护多分支结果列表，与 `case` 的第一参数求值强相关。

### 12.2 `function` / `return` 与控制流

用户定义的 `function` 体以 `return` 结束；`function_ret`（`interpreter.rs` 723–743）决定是继续嵌套嵌入算子，还是向上返回 `return` 包裹的值。`case` 外层 `(function ...)` 使得 `switch-minimal` 可在 **局部栈帧** 内完成，再 `return` 到外层。

### 12.3 非确定性与 `superpose-bind`

`case` 在“第一参数非空”分支使用 `superpose-bind` 展开 `collapse-bind` 得到的 **多绑定** 结果；`superpose_bind`（`interpreter.rs` 893–917）对每个 `(atom, bindings)` 与当前 `bindings` 做 `merge`，过滤环绑定。这是 `case` 能处理“多解”匹配的核心。

### 12.4 测试用例索引

- `case`：`core.rs` `metta_case_empty`、`metta_case_error`（约 407–428、469–482 行）。
- `let` / `sealed` / `quote`：`core.rs` `use_sealed_to_make_scoped_variable`、`sealed_op_runner`（约 486–527 行）。
- `if` 与栈深度：`core.rs` `test_pragma_max_stack_depth`（约 452–482 行）。

### 12.5 与 `minimal-metta.md` 的关系

`interpreter.rs` 文件头指向仓库内 minimal MeTTa 文档；读者可对照 **嵌入指令表** 与本文分节。

### 12.6 C API 边界

控制流 **不** 通过 `c/src/atom.rs` 的单独函数暴露；但 `atom_expr`、`atom_sym` 等用于构建表达式树，再交给 `interpret_*` C 入口（见 `c/src/metta.rs`，本文不展开）。

### 12.7 性能与栈深度

`interpret_stack` 在 `max_stack_depth > 0` 且深度超限时对 `METTA_SYMBOL` 帧返回栈溢出错误（`interpreter.rs` 392–413 行注释详述与 `case`/`collapse` 等的交互）。

### 12.8 读者练习（可选）

1. 将 `(case X ((A a) (B b)))` 手写展开为仅含 `unify`/`chain`/`eval`/`return` 的近似树。
2. 对比 `switch` 与 `case` 在 `Empty` 第一参数时的行为差异（参阅 `stdlib.metta` 331–338 行注释）。

### 12.9 版本说明

本文行号均针对撰写时工作区路径 **d:\dev\hyperon-experimental**；若上游移动定义，请以 `grep` / IDE 符号为准。

### 12.10 术语对照

- **Bindings**：变量到 atom 的映射，C 侧 `bindings_t`（`c/src/atom.rs` 1086 行起）。
- **DynSpace**：动态分派的空间句柄，grounded 后作为 atom 传入 `match` 等算子。

---

## 附录 A：`if-equal` 完整 Rust 片段

```170:197:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\core.rs
pub struct IfEqualOp { }

grounded_op!(IfEqualOp, "if-equal");
// ...
impl CustomExecute for IfEqualOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let arg_error = || ExecError::from("if-equal expects <atom> <pattern> <then> <else> as an argument");
        let atom = args.get(0).ok_or_else(arg_error)?;
        let pattern = args.get(1).ok_or_else(arg_error)?;
        let then = args.get(2).ok_or_else(arg_error)?;
        let else_ = args.get(3).ok_or_else(arg_error)?;

        if hyperon_atom::matcher::atoms_are_equivalent(atom, pattern) {
            Ok(vec![then.clone()])
        } else {
            Ok(vec![else_.clone()])
        }
    }
}
```

---

## 附录 B：`chain` 指令语义摘要

```687:701:d:\dev\hyperon-experimental\lib\src\metta\interpreter.rs
fn chain(stack: Stack, bindings: Bindings) -> Vec<InterpretedAtom> {
    let Stack{ prev, atom: chain, vars, .. } = stack;
    let (nested, var, templ) = match_atom!{
        chain ~ [_op, nested, Atom::Variable(var), templ] => (nested, var, templ),
        _ => {
            panic!("Unexpected state")
        }
    };
    let b = Bindings::new().add_var_binding(var, nested).unwrap();
    let templ = apply_bindings_to_atom_move(templ, &b);
    let stack = atom_to_stack(templ, prev);
    // ...
    vec![InterpretedAtom(stack, bindings)]
}
```

`chain` 先求值 **nested**（通过 `chain_to_stack` 重排栈），结果经 `chain_ret` 写回再求 **template**；这是 `let*`、`case` 等宏展开的事实基础。

---

*文档结束。*
