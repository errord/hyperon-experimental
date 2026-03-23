---
title: MeTTa 状态管理全链分析
order: 9
---

# 文档 9：状态管理（`new-state` / `get-state` / `change-state!` / `bind!`）

本文档追踪 **可变状态** 在 MeTTa 中的建模方式：`StateAtom`（`Rc<RefCell<(Atom, Atom)>>`）、grounded 算子 **`_new-state`** / **`get-state`** / **`change-state!`**、标准库 **`new-state` 的 MeTTa 包装**、**类型检查与 `BadArgType`**、以及 Python/C 边界行为。

---

## 1. 设计动机：immutable MeTTa 表面语法下的可变单元

MeTTa 程序中的 **表达式与重写规则** 通常以 **不可变** 方式处理；需要 **可更新存储** 时，引擎引入 **grounded `StateAtom`**：

- 对外仍是一个 **Atom**（可传入 `match`、放入空间、作为函数参数）。
- 对内用 **`Rc<RefCell<...>>`** 共享可变单元，使多个引用指向同一可变槽位。

这与 **空间突变**（`add-atom` 等）互补：空间修改的是 **知识库集合**；`StateAtom` 修改的是 **单个封装槽**。

---

## 2. `StateAtom` 内部：`Rc<RefCell<(Atom, Atom)>>`

定义于 `lib/src/metta/runner/stdlib/space.rs`：

```38:58:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
#[derive(Clone, PartialEq, Debug)]
pub struct StateAtom {
    state: Rc<RefCell<(Atom, Atom)>>
}

impl StateAtom {
    pub fn new(atom: Atom, typ: Atom) -> Self {
        Self{ state: Rc::new(RefCell::new((atom, typ))) }
    }
}

impl Display for StateAtom {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "(State {})", self.state.borrow().0)
    }
}

impl Grounded for StateAtom {
    fn type_(&self) -> Atom {
        self.state.borrow().1.clone()
    }
}
```

**元组字段语义**：

- **`.0`**：当前存储的 **值 atom**（可被 `change-state!` 替换）。
- **`.1`**：该状态单元的 **类型 atom**（通常为 `(StateMonad T)`），供 MeTTa 类型系统与 `Grounded::type_` 使用。

**`Clone` 与 `Rc`**：`StateAtom` 的 `Clone` 复制 `Rc` 句柄而非底层状态，故 `bind!` 或模式绑定得到 **别名** 时，突变对各方可见。

---

## 3. `_new-state`（GroundedFunctionAtom）与 `new_state` 闭包

### 3.1 Rust 函数 `new_state`

```61:72:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
fn new_state(args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
    let arg_error = "new-state expects atom as a first argument and non-empty list of types as a second argument";
    let atom = args.get(0).ok_or(arg_error)?;
    let typ = args.get(1)
        .and_then(|t| TryInto::<&ExpressionAtom>::try_into(t).ok())
        .and_then(|e| e.children().get(0))
        .ok_or(arg_error)?;
    Ok(vec![Atom::gnd(StateAtom::new(atom.clone(),
        Atom::expr([Atom::sym("StateMonad"), typ.clone()])))])
}
```

第二参数为 **`Expression`**，取其 **第一个子元素** 作为 `T`，构造类型 `(StateMonad T)`。

### 3.2 注册名 `_new-state`

```213:217:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
    tref.register_function(GroundedFunctionAtom::new(
            r"_new-state".into(),
            expr!("->" t "Expression" ("StateMonad" t)),
            |args: &[Atom]| -> Result<Vec<Atom>, ExecError> { new_state(args) }, 
        ));
```

MeTTa 层 **`new-state`** 在调用 `_new-state` 前负责从 **当前空间** 推断类型（见第 4 节）。

---

## 4. MeTTa 标准库：`new-state` 包装

```1026:1035:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc new-state
  (@desc "Creates a new state atom wrapping its argument")
  (@params (
    (@param "Atom to be wrapped")))
  (@return "Returns (State $value) where $value is an argument to a new-state"))
(: new-state (-> $t (StateMonad $t)))
(= (new-state $x)
   (chain (context-space) $space
     (let $t (collapse (get-type-space $space $x))
       (_new-state $x $t))))
```

**链路与解释器对应**：

1. `context-space` → `context_space`（`interpreter.rs` 954–964 行）。
2. `get-type-space` → `GetTypeSpaceOp`（`atom.rs` 433–446 行）在 **给定空间** 查询 `$x` 的类型。
3. `collapse` 将类型结果收拢为可传入 `_new-state` 的 **表达式**。
4. `_new-state` 构造 `StateAtom` 并返回 grounded atom。

---

## 5. `get-state`：`GetStateOp`

### 5.1 类型与执行

```74:96:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
#[derive(Clone, Debug)]
pub struct GetStateOp { }

grounded_op!(GetStateOp, "get-state");

impl Grounded for GetStateOp {
    fn type_(&self) -> Atom {
        Atom::expr([ARROW_SYMBOL, expr!("StateMonad" tgso), expr!(tgso)])
    }
    // ...
}

impl CustomExecute for GetStateOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let arg_error = "get-state expects single state atom as an argument";
        let state = args.get(0).ok_or(arg_error)?;
        let atom = Atom::as_gnd::<StateAtom>(state).ok_or(arg_error)?;
        Ok(vec![atom.state.borrow().0.clone()])
    }
}
```

**行为**：`borrow()` 读 `RefCell`，返回 **值的克隆**（`Atom` 的 `clone`），不转移所有权。

### 5.2 分词器注册

```220:221:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
    let get_state_op = Atom::gnd(GetStateOp{});
    tref.register_token(regex(r"get-state"), move |_| { get_state_op.clone() });
```

---

## 6. `change-state!`：`ChangeStateOp`

### 6.1 类型签名

```98:106:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
#[derive(Clone, Debug)]
pub struct ChangeStateOp { }

grounded_op!(ChangeStateOp, "change-state!");

impl Grounded for ChangeStateOp {
    fn type_(&self) -> Atom {
        Atom::expr([ARROW_SYMBOL, expr!("StateMonad" tcso), expr!(tcso), expr!("StateMonad" tcso)])
    }
```

即 **同型** 更新：第二个参数类型应与 monad 内 `tcso` 一致（由 MeTTa 类型层约束）。

### 6.2 `execute`：赋值与返回同一状态句柄

```113:121:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
impl CustomExecute for ChangeStateOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let arg_error = "change-state! expects a state atom and its new value as arguments";
        let atom = args.get(0).ok_or(arg_error)?;
        let state = Atom::as_gnd::<StateAtom>(atom).ok_or("change-state! expects a state as the first argument")?;
        let new_value = args.get(1).ok_or(arg_error)?;
        state.state.borrow_mut().0 = new_value.clone();
        Ok(vec![atom.clone()])
    }
}
```

**注意**：**此处不做** 值与 `StateMonad` 内部类型 `A` 的运行时校验；`borrow_mut().0` 直接覆盖。

### 6.3 测试中 `BadArgType` 的来源

同一文件模块测试 `state_ops`（约 302–322 行）在启用类型标注时：

```302:322:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
    fn state_ops() {
        let program = r#"
            (: a A)
            (: aa A)
            (: b B)
            (: F (-> $t $t))
            !(bind! &stateAB (new-state (F a)))
            !(change-state! &stateAB (F aa))
            !(get-state &stateAB)
            !(change-state! &stateAB (F b))
        "#;
        // ...
            vec![metta!((Error ({ChangeStateOp{}} {faa} (F b)) (BadArgType 2 A B)))],
```

解释：

- `new-state (F a)` 结合空间中的 `(: a A)`，推断状态携带 **A**。
- `(F b)` 中 `b` 为 **B**，与形式参数类型 **A** 冲突。
- **`BadArgType`** 由 MeTTa **类型检查 / 参数匹配** 路径产生（与 `interpret_args` 等对 grounded 调用的检查一致，参见 `interpreter.rs` 1352–1394 行附近及 `BadArgType` 构造），**早于** 或 **替代** 对 `ChangeStateOp::execute` 的成功调用。

**结论**：**类型安全** 主要由 **MeTTa 类型层** 保证；**Rust `execute`** 负责 **高效突变**。

---

## 7. `bind!`（状态变量与 token）

状态常配合 **`bind!`** 将符号（如 `&state`）绑定到解析器：

```246:277:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\module.rs
pub struct BindOp {
    tokenizer: Shared<Tokenizer>,
}
// ...
impl CustomExecute for BindOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let arg_error = || ExecError::from("bind! expects two arguments: token and atom");
        let token = <&SymbolAtom>::try_from(args.get(0).ok_or_else(arg_error)?).map_err(|_| "bind! expects symbol atom as a token")?.name();
        let atom = args.get(1).ok_or_else(arg_error)?.clone();

        let token_regex = Regex::new(token).map_err(|err| format!("Could convert token {} into regex: {}", token, err))?;
        self.tokenizer.borrow_mut().register_token(token_regex, move |_| { atom.clone() });
        unit_result()
    }
}
```

**Python 侧** 同类 API：`Tokenizer.register_token`（`base.py` 313–325 行）→ `hp.tokenizer_register_token`。

---

## 8. 与解释器 `eval` 的衔接

带 `StateAtom` 的 grounded 调用仍走 `eval_impl` 的 `execute` / `execute_bindings` 分支（`interpreter.rs` 504–525 行）。**无** 单独 `StateOp` 嵌入指令；状态是 **普通 grounded 数据**。

---

## 9. Python FFI：状态 atom 如何出现

### 9.1 一般 grounded 对象

`GroundedAtom.get_object()`（`atoms.py` 153–167 行）对 **非 CGrounded** 尝试 `_priv_gnd_get_object`。`StateAtom` 为 **纯 Rust** grounded，不经由 `atom_py` 暴露为 Python 类时，**通常不能** unwrap 为 Python 对象。

### 9.2 实用策略

- 在 Python 中把 **状态** 仍当作 **不透明 `Atom`** 传递；用 **`MeTTa.run`** 执行 `get-state` / `change-state!` 表达式。
- 若需 Python 可变状态，优先 **`GroundingSpaceRef` + add/remove** 或自定义 **`AbstractSpace`**（见文档 8）。

### 9.3 `G()` / `ValueAtom` 边界

`StateAtom` **不是** `ValueObject`；`OperationAtom` 包装的是 Python 可调用，与 Rust `StateAtom` 不同。

### 9.4 C API 层面

- 状态作为 **grounded atom** 出现时，与其他 `atom_t` 相同：`atom_free`、`atom_clone`（`c/src/atom.rs`）。
- **无** 单独 `state_t`；共享性由 Rust `Rc` 在 `clone` 时体现。

---

## 10. `c/src/atom.rs` 交叉引用（状态相关）

状态 **不** 增加新的 C 结构；相关能力：

- **`atom_gnd`**：通用 grounded 构造（270–272 行）。
- **匹配与相等**：若未来为 `StateAtom` 自定义 `match`，可走 grounded 接口；当前实现依赖默认 **Rust PartialEq** 等。

---

## 11. 文档块：`get-state` / `change-state!`（stdlib.metta）

```1044:1048:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc get-state
  (@desc "Gets a state as an argument and returns its wrapped atom. E.g. (get-state (State 5)) -> 5")
  (@params (
    (@param "State")))
  (@return "Atom wrapped by state"))
```

`change-state!` 文档在 1037–1042 行；**无** 额外 MeTTa 层 `(= (change-state! ...) ...)` 覆盖默认 grounded 行为。

---

## 12. 小结表

| 名称 | 角色 | 文件：行号 |
|------|------|------------|
| `StateAtom` | `Rc<RefCell<(值, 类型)>>` | `space.rs` 38–58 |
| `new_state` | 构造 `StateMonad` 包装 | `space.rs` 61–72 |
| `_new-state` | 分词器注册函数 | `space.rs` 213–217 |
| `new-state` (MeTTa) | 推断类型 + 调 `_new-state` | `stdlib.metta` 1031–1035 |
| `get-state` | 读副本 | `space.rs` 89–95 |
| `change-state!` | 写槽位 | `space.rs` 113–121 |
| `bind!` | tokenizer 注册 | `module.rs` 268–276 |

---

## 13. 线程与安全性说明

`RefCell` **非线程安全**；当前 MeTTa 解释器模型以 **单线程** 为主。若未来并行求值，需替换为 `Mutex` 或把状态隔离到 **每任务空间**。

---

## 14. 与 `Empty` / 错误传播

`get-state` 在参数非 `StateAtom` 时返回 `ExecError` 字符串错误，经 `eval_impl` 变为 **运行时错误 atom**（`interpreter.rs` 541–542 行路径）。

---

## 15. 调试与打印

`Display for StateAtom` 只打印 **当前值**（`space.rs` 49–52 行），不打印内部类型；调试类型需查 `type_()` 或 `get-type`。

---

## 16. 示例程序 walkthrough（对应测试）

1. `!(bind! &stateAB (new-state (F a)))`：`new-state` 推断 `(F a)` 中 `a:A` → `StateMonad A`；`bind!` 注册 token。
2. `!(change-state! &stateAB (F aa))`：`aa:A`，通过类型检查；`execute` 写 `.0`。
3. `!(get-state &stateAB)`：返回 `(F aa)`。
4. `!(change-state! &stateAB (F b))`：`b:B`，**类型检查失败** → `BadArgType`；`execute` **不** 成功执行到赋值。

---

## 17. 设计模式对照

| 模式 | MeTTa 中的类似物 |
|------|------------------|
| `IORef` / `Cell` | `StateAtom` |
| Reader monad | 显式 `&self` / `space` 参数 |
| ST monad | 本仓库 **未** 提供线性状态；需约定 |

---

## 18. 扩展：多状态与别名

由于 `Rc` 克隆，**同一 `StateAtom`** 可经 `superpose`、多分支绑定重复出现；突变 **全局可见**。推理控制需谨慎。

---

## 19. 与 `pragma!` 的关系

`pragma! type-check` 等影响类型检查强度（参见 `core.rs` 中 `PragmaOp` 与相关测试）。状态 API 的 **类型错误** 表现随之变化。

---

## 20. 附录：`StateMonad` 命名

`StateMonad` 为 **类型标记符号**，并非 Haskell `State` monad 的完整实现；无 `bind`/`return` 的通用组合子在本节算子集中提供。

---

## 21. 附录：相关 grounded 算子索引（非状态但常一起出现）

- **`get-type` / `get-type-space`**：`atom.rs` 353–446 行。
- **`collapse`**：与 `new-state` 类型列表交互（`stdlib.metta` 1033 行）。

---

## 22. 实现者备忘（扩展）

### 22.1 `new_state` 第二参数格式

必须为非空 `Expression`，且取 **第一个子** 为类型；若 `collapse` 产生意外形状，会在 `_new-state` 处失败。

### 22.2 `StateAtom` 的 `PartialEq`

`#[derive(PartialEq)]` 比较 **Rc 指针与内部**（Rust 默认对 `Rc` 结构体）；与 **逻辑相等** 未必一致，慎用 `==` 于含状态的单元测试。

### 22.3 与空间 `remove` 的交互

从空间 **移除** 含有 `StateAtom` 的表达式 **不** 自动 `Drop` 其他别名上的 `Rc`，除非所有引用释放。

### 22.4 序列化

若需跨进程持久化状态，需自定义 **grounded serialize**；当前 `StateAtom` 未在本文档检索到 C serializer 实现。

### 22.5 错误消息稳定性

`arg_error` 字符串参与用户可见错误；变更需同步测试（`space.rs` `state_ops`）。

### 22.6 `bind!` 与 regex

token 名解析为 **正则**（`module.rs` 274 行）；`&stateAB` 等需合法 regex。

### 22.7 与文档 7 `let` 的对比

`let` 使用 **`unify`** 绑定；`StateAtom` 使用 **命令式赋值**，语义 **不等价**。

### 22.8 与文档 8 `match` 的对比

可对 **含 `StateAtom` 的模式** 做匹配，但 **匹配不会** 自动解引用内部 cell。

### 22.9 教学用最小示例

```metta
(: counter Number)
(= (inc! $s) (change-state! $s (+ (get-state $s) 1)))
```

需额外 `new-state` 初始化数值与类型标注，略。

### 22.10 未来工作

`new_state` 内 TODO（`space.rs` 66–67 行）提及 grounded 多类型返回时 `_new-state` 需扩展。

---

## 23. Python `MeTTa` runner 使用状态（概念）

通过字符串执行，状态保留在 Rust 侧空间中；Python 不直接持有 `RefCell`；**真相来源** 为 Rust `DynSpace` + tokenizer 绑定。

---

## 24. C 侧无专用 API 的总结

| 需求 | 做法 |
|------|------|
| 创建状态 | 执行 MeTTa `new-state` 或构造含 `StateAtom` 的 Rust atom 并注入 |
| 读取 | 调用 `get-state` 算子 |
| 写入 | 调用 `change-state!` 算子 |

---

## 25. 读者自检问题

1. `StateAtom::type_` 返回什么？与 `borrow().1` 的关系？
2. 为何 `change-state!` 的 Rust 层不校验 `A`/`B`？
3. `bind!` 后 `&x` 与 `Atom::gnd(state.clone())` 共享突变的条件是什么？

---

## 26. 索引：`interpreter.rs` 类型检查锚点

函数应用参数解释中的 `if-equal` 与递归（节选）：

```1376:1394:d:\dev\hyperon-experimental\lib\src\metta\interpreter.rs
        once((
            Atom::expr([CHAIN_SYMBOL, Atom::expr([METTA_SYMBOL, args_head.clone(), types_head, space.clone()]), rhead.clone(),
                Atom::expr([EVAL_SYMBOL, Atom::expr([Atom::gnd(IfEqualOp{}), rhead.clone(), args_head,
                    recursion.clone(),
                    call_native!(return_on_error, Atom::expr([rhead, 
                        recursion
                    ]))
                ])])
            ]), bindings))
```

`BadArgType` 在 `check_if_function_type_is_applicable_` 中构造（约 1334–1338 行）。

---

## 27. 补充：状态算子注册一览

```206:224:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\space.rs
pub(super) fn register_context_independent_tokens(tref: &mut Tokenizer) {
    let new_space_op = Atom::gnd(NewSpaceOp{});
    tref.register_token(regex(r"new-space"), move |_| { new_space_op.clone() });
    // ...
    tref.register_function(GroundedFunctionAtom::new(
            r"_new-state".into(),
            expr!("->" t "Expression" ("StateMonad" t)),
            |args: &[Atom]| -> Result<Vec<Atom>, ExecError> { new_state(args) }, 
        ));
    let change_state_op = Atom::gnd(ChangeStateOp{});
    tref.register_token(regex(r"change-state!"), move |_| { change_state_op.clone() });
    let get_state_op = Atom::gnd(GetStateOp{});
    tref.register_token(regex(r"get-state"), move |_| { get_state_op.clone() });
    // ...
}
```

---

## 28. 补充：`BindOp` 测试

`module.rs` `bind_new_space_op`（约 306–316 行）演示 `register_token` 后 `find_token` 行为；状态变量绑定同理。

---

## 29. 术语中英对照

| 中文 | 英文标识 |
|------|-----------|
| 状态单元 | `StateAtom` |
| 状态单子类型 | `StateMonad` |
| 取状态 | `get-state` |
| 改状态 | `change-state!` |

---

## 30. 与文档 8 的边界

- **空间** 操作改变 **集合**；**状态** 操作改变 **单槽**。
- 二者均可经 `bind!` 绑定 token；`&self` 仅指向空间。

---

*文档结束。*
