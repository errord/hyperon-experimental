---
title: MeTTa 原子操作全链分析
order: 13
---

# 文档 13：原子操作（MeTTa → Python → Rust）

本文档按「表面语法 / stdlib 包装 → 解释器或 grounded 算子 → 类型与空间」的顺序，给出当前 `hyperon-experimental` 仓库中的**精确行号**。Python 侧多数原子级能力不单独暴露 API，而是通过 `MeTTa.run` / `MeTTa.evaluate_atom` 进入 C 绑定，最终执行与 Rust 相同的解释器与 grounded 算子。

## 1. 总览：词法注册与 Runner 入口

### 1.1 Rust：与上下文无关的 atom 相关 token

`unique-atom`、`union-atom`、`intersection-atom`、`subtraction-atom`、`min-atom`、`max-atom`、`size-atom`、`index-atom`、`get-metatype`、`get-type-space` 等在 `register_context_independent_tokens` 中注册：

```454:475:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\atom.rs
pub(super) fn register_context_independent_tokens(tref: &mut Tokenizer) {
    let get_type_space_op = Atom::gnd(GetTypeSpaceOp{});
    tref.register_token(regex(r"get-type-space"), move |_| { get_type_space_op.clone() });
    let get_meta_type_op = Atom::gnd(GetMetaTypeOp{});
    tref.register_token(regex(r"get-metatype"), move |_| { get_meta_type_op.clone() });
    // ... min-atom, max-atom, size-atom, index-atom, unique-atom, subtraction-atom, intersection-atom, union-atom
}
```

`get-type` 需要当前模块的 `DynSpace`，故在 `register_context_dependent_tokens` 中注册：

```449:452:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\atom.rs
pub(super) fn register_context_dependent_tokens(tref: &mut Tokenizer, space: &DynSpace) {
    let get_type_op = Atom::gnd(GetTypeOp::new(space.clone()));
    tref.register_token(regex(r"get-type"), move |_| { get_type_op.clone() });
}
```

### 1.2 Rust：`&self` 与 stdlib 总注册

`&self` 解析为当前模块空间的 grounded 句柄，与 atom 算子共用同一 tokenizer 管线：

```64:83:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\mod.rs
fn register_context_dependent_tokens(tref: &mut Tokenizer, tokenizer: Shared<Tokenizer>, space: &DynSpace, metta: &Metta) {
    atom::register_context_dependent_tokens(tref, space);
    // ...
    let self_atom = Atom::gnd(space.clone());
    tref.register_token(regex(r"&self"), move |_| { self_atom.clone() });
}
```

### 1.3 Python：进入 Runner

`MeTTa.run` 将程序交给 C 层 `metta_run`，错误经 `metta_err_str` 抛出；不逐算子包装：

```206:214:d:\dev\hyperon-experimental\python\hyperon\runner.py
    def run(self, program, flat=False):
        """Runs the MeTTa code from the program string containing S-Expression MeTTa syntax"""
        parser = SExprParser(program)
        results = hp.metta_run(self.cmetta, parser.cparser)
        self._run_check_for_error()
        if flat:
            return [Atom._from_catom(catom) for result in results for catom in result]
        else:
            return [[Atom._from_catom(catom) for catom in result] for result in results]
```

`evaluate_atom` 在开启 `type-check` 时使用与 `get-type` 相同的类型推导入口 `get_atom_types`（见下文 §2.1 与 `mod.rs`）。

---

## 2. `get-type`（GetTypeOp）与 `get-type-space`（GetTypeSpaceOp）

### 2.1 类型推导核心：`types::get_atom_types`

`GetTypeOp::execute` 在可选第二参数为 space 时调用 `Atom::as_gnd::<DynSpace>`，否则使用构造时保存的 `self.space`，然后调用：

```376:391:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\atom.rs
impl CustomExecute for GetTypeOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        // ...
        let types = get_atom_types(space, atom);
        if types.iter().all(AtomType::is_error) {
            Ok(vec![EMPTY_SYMBOL])
        } else {
            Ok(types.into_iter().filter(AtomType::is_valid).map(AtomType::into_atom).collect())
        }
    }
}
```

`get_atom_types` 公共 API 与内部实现：

```327:334:d:\dev\hyperon-experimental\lib\src\metta\types.rs
pub fn get_atom_types(space: &DynSpace, atom: &Atom) -> Vec<AtomType> {
    let atom_types = get_atom_types_internal(space, atom);
    if atom_types.is_empty() {
        vec![AtomType::undefined()]
    } else {
        atom_types
    }
}
```

```376:410:d:\dev\hyperon-experimental\lib\src\metta\types.rs
fn get_atom_types_internal(space: &DynSpace, atom: &Atom) -> Vec<AtomType> {
    let types = match atom {
        Atom::Variable(_) => vec![],
        Atom::Grounded(gnd) => { /* gnd.type_() */ },
        Atom::Symbol(_) => query_types(space, atom).into_iter().map(AtomType::value).collect(),
        Atom::Expression(expr) if expr.children().len() == 0 => vec![],
        Atom::Expression(expr) => {
            let type_info = ExprTypeInfo::new(space, expr);
            let mut types = get_tuple_types(space, atom, &type_info);
            let applications = get_application_types(atom, expr, type_info);
            types.extend(applications.into_iter());
            types
        },
    };
    types
}
```

`GetTypeSpaceOp` 显式接受 `(space atom)` 并同样调用 `get_atom_types`：

```433:446:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\atom.rs
impl CustomExecute for GetTypeSpaceOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let space = Atom::as_gnd::<DynSpace>(space).ok_or("get-type-space expects a space as the first argument")?;
        let atom = args.get(1).ok_or_else(arg_error)?;
        let types = get_atom_types(space, atom);
        // 与 GetTypeOp 相同的 Empty / 过滤逻辑
    }
}
```

### 2.2 MeTTa：`type-cast` 等对 `get-type` 的调用

`stdlib.metta` 中 `type-cast` 通过 `get-type` 与 space 交互（行号见该文件内 `(get-type $atom $space)` 一带）。

### 2.3 Runner 层类型检查

`Metta::evaluate_atom` 在 `type-check` 为 `auto` 时调用 `get_atom_types`：

```467:477:d:\dev\hyperon-experimental\lib\src\metta\runner\mod.rs
    pub fn evaluate_atom(&self, atom: Atom) -> Result<Vec<Atom>, String> {
        // ...
        if self.type_check_is_enabled()  {
            let types = get_atom_types(&self.module_space(ModId::TOP), &atom);
            if types.iter().all(AtomType::is_error) {
                return Ok(types.into_iter().map(AtomType::into_error_unchecked).collect());
            }
        }
        interpret(self.space().clone(), &atom)
    }
```

解释器在 `INTERPRET` 模式下对当前模块 space 做类型检查时同样使用 `get_atom_types`：

```1086:1092:d:\dev\hyperon-experimental\lib\src\metta\runner\mod.rs
                            if self.metta.type_check_is_enabled() {
                                let types = get_atom_types(&self.module().space(), &atom);
                                if types.iter().all(AtomType::is_error) {
                                    self.i_wrapper.interpreter_state = Some(InterpreterState::new_finished(/* ... */));
                                    return Ok(())
                                }
                            }
```

---

## 3. `get-metatype`（GetMetaTypeOp）

### 3.1 Grounded 算子

```409:415:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\atom.rs
impl CustomExecute for GetMetaTypeOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let atom = args.get(0).ok_or_else(arg_error)?;
        Ok(vec![get_meta_type(&atom)])
    }
}
```

### 3.2 语义：Symbol / Variable / Expression / Grounded

`get_meta_type` 在 `types.rs` 中按原子种类返回常量类型原子：

```606:612:d:\dev\hyperon-experimental\lib\src\metta\types.rs
pub fn get_meta_type(atom: &Atom) -> Atom {
    match atom {
        Atom::Symbol(_) => ATOM_TYPE_SYMBOL,
        Atom::Variable(_) => ATOM_TYPE_VARIABLE,
        Atom::Grounded(_) => ATOM_TYPE_GROUNDED,
        Atom::Expression(_) => ATOM_TYPE_EXPRESSION,
    }
}
```

类型检查中函数应用路径也会把「参数的 metatype」与 `ATOM_TYPE_ATOM` 成对使用（`get_application_types` 内对 `get_meta_type` 的调用，约 `types.rs` 514 行附近）。

---

## 4. `unique-atom`（UniqueAtomOp）：基于 matcher 的去重

```29:41:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\atom.rs
impl CustomExecute for UniqueAtomOp {    
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {    
        let expr = TryInto::<&ExpressionAtom>::try_into(args.get(0).ok_or_else(arg_error)?)?;    
        let mut atoms: Vec<Atom> = expr.children().into();    
        let mut seen: Vec<Atom> = Vec::new();    
        atoms.retain(|x| {    
            let not_contained = !seen.iter().any(|seen_atom| atoms_are_equivalent(seen_atom, x));    
            if not_contained { seen.push(x.clone()) };    
            not_contained    
        });    
        Ok(vec![Atom::expr(atoms)])    
    }    
}
```

MeTTa 层 `unique` 将非确定性结果 `collapse` 后调用 `unique-atom` 再 `superpose`：

```629:630:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(= (unique $arg) (let $c (collapse $arg) (let $u (unique-atom $c) (superpose $u))))
```

---

## 5. `union-atom`（UnionAtomOp）

```61:70:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\atom.rs
impl CustomExecute for UnionAtomOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let mut lhs: Vec<Atom> = TryInto::<&ExpressionAtom>::try_into(args.get(0).ok_or_else(arg_error)?)?.children().into();
        let rhs: Vec<Atom> = TryInto::<&ExpressionAtom>::try_into(args.get(1).ok_or_else(arg_error)?)?.children().into();
        lhs.extend(rhs);
        Ok(vec![Atom::expr(lhs)])
    }
}
```

Stdlib `union`：`collapse` 两侧再 `union-atom`（`stdlib.metta` 639–641 行）。

---

## 6. `intersection-atom`（IntersectionAtomOp）与 `subtraction-atom`（SubtractionAtomOp）

二者共享 `atom_to_trie_key`：将原子编码为 `MultiTrie` 的键；符号与表达式结构用 `TrieToken::Exact` / 括号；变量与部分 grounded 用 `Wildcard` 或序列化哈希（见 88–114 行）。

**交集**：在 RHS 上建索引，遍历 LHS 保留在 RHS 中仍**可匹配**且按桶消费一次的元素（117–165 行）。

**差集**：同样用 RHS 索引，从 LHS 中删除能在 RHS 中消费到的元素（302–349 行）。

---

## 7. `size-atom`（SizeAtomOp）与 `index-atom`（IndexAtomOp）

```251:257:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\atom.rs
impl CustomExecute for SizeAtomOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let children = TryInto::<&ExpressionAtom>::try_into(args.get(0).ok_or_else(arg_error)?)?.children();
        let size = children.len();
        Ok(vec![Atom::gnd(Number::Integer(size as i64))])
    }
}
```

```275:284:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\atom.rs
impl CustomExecute for IndexAtomOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let children = TryInto::<&ExpressionAtom>::try_into(args.get(0).ok_or_else(arg_error)?)?.children();
        let index = args.get(1).and_then(Number::from_atom).ok_or_else(arg_error)?;
        match children.get(Into::<i64>::into(index) as usize) {
            Some(atom) => Ok(vec![atom.clone()]),
            None => Err(ExecError::from("Index is out of bounds")),
        }
    }
}
```

---

## 8. `min-atom` / `max-atom`

二者要求表达式子项均可转为 `Number`，分别用 `f64::min` / `f64::max` 聚合；`min` 初值为 `INFINITY`，`max` 为 `NEG_INFINITY`（183–233 行）。

---

## 9. `sort-atom`（SortAtomOp）说明

在当前仓库的 `lib/` 下**未找到**名为 `sort-atom` 的 grounded 算子或 tokenizer 注册。与「排序」最接近的实现是 **`sort-strings`**：在 `string.rs` 中以 `GroundedFunctionAtom` 注册，对表达式中每个子原子要求为 `Str`，排序后重组为表达式：

```64:88:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\string.rs
fn sort_strings(args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
    // ...
    strings.sort();
    let sorted: Vec::<Atom> = strings.into_iter()
        .map(|s| Atom::gnd(Str::from_string(s.into()))).collect();
    Ok(vec![Atom::expr(sorted)])
}
// register: r"sort-strings"
```

`stdlib.metta` 中有 `@doc sort-strings`（约 1292–1296 行）。若文档或外部提示词中出现 `sort-atom`，应视为**尚未在本仓库实现**或与 `sort-strings` 混淆。

---

## 10. `car-atom` / `cdr-atom`（stdlib.metta）→ `decons-atom`（解释器）

### 10.1 MeTTa 定义

```570:590:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(: car-atom (-> Expression %Undefined%))
(= (car-atom $atom)
  (chain (decons-atom $atom) $ht (unify ($head $_) $ht
    $head
    (Error (car-atom $atom) "car-atom expects a non-empty expression as an argument") )))

(: cdr-atom (-> Expression Expression))
(= (cdr-atom $atom)
  (chain (decons-atom $atom) $ht (unify ($_ $tail) $ht
    $tail
    (Error (cdr-atom $atom) "cdr-atom expects a non-empty expression as an argument") )))
```

### 10.2 Rust 最小解释器：`decons-atom` / `cons-atom`

调度入口（`interpret_step` 内）：

```435:440:d:\dev\hyperon-experimental\lib\src\metta\interpreter.rs
            Some([op, ..]) if *op == DECONS_ATOM_SYMBOL => {
                decons_atom(stack, bindings)
            },
            Some([op, ..]) if *op == CONS_ATOM_SYMBOL => {
                cons_atom(stack, bindings)
            },
```

`decons_atom` 实现 head/tail 分裂：

```843:855:d:\dev\hyperon-experimental\lib\src\metta\interpreter.rs
fn decons_atom(stack: Stack, bindings: Bindings) -> Vec<InterpretedAtom> {
    let expr = match_atom!{
        decons ~ [_op, Atom::Expression(expr)] if expr.children().len() > 0 => expr,
        _ => { /* 错误 */ }
    };
    let mut children = expr.into_children();
    let head = children.remove(0);
    let tail = children;
    finished_result(Atom::expr([head, Atom::expr(tail)]), bindings, prev)
}
```

`stdlib.metta` 中 `(: decons-atom (-> Expression Atom))` 与 `@doc` 见约 98–103 行。

### 10.3 单元测试

`atom.rs` 中 `metta_car_atom` / `metta_cdr_atom`（约 489–507 行）通过 `run_program` 验证 MeTTa 层行为。

---

## 11. `switch`：并非独立 `SwitchOp`，而是 stdlib 中的 MeTTa 组合

**本仓库不存在**名为 `SwitchOp` 的 Rust grounded 结构体。`switch` 在 `stdlib.metta` 中由 `switch-minimal`、`switch-internal` 与解释器原语 `chain`、`decons-atom`、`unify`、`eval`、`if-equal` 组合而成。

核心定义（含与 `case` / `Empty` 的差异说明）：

```339:365:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(: switch (-> %Undefined% Expression %Undefined%))
(= (switch $atom $cases)
   (id (switch-minimal $atom $cases)))

(: switch-minimal (-> Atom Expression Atom))
(= (switch-minimal $atom $cases)
  (function (chain (decons-atom $cases) $list
    (chain (eval (switch-internal $atom $list)) $res
      (chain (eval (if-equal $res NotReducible Empty $res)) $x (return $x)) ))))

(= (switch-internal $atom (($pattern $template) $tail))
  (function (unify $atom $pattern
    (return $template)
    (chain (eval (switch-minimal $atom $tail)) $ret (return $ret)) )))
```

Rust 侧对应的原语执行函数：

- `chain`：`687:702:d:\dev\hyperon-experimental\lib\src\metta\interpreter.rs`
- `unify`：`809:841:d:\dev\hyperon-experimental\lib\src\metta\interpreter.rs`
- `decons_atom`：同上 §10.2

`case` 则在求值第一参数后处理 `Empty` 与非空分支（`stdlib.metta` 1224–1232 行；解释器层配合 `collapse-bind` / `superpose-bind`）。

---

## 12. Python 侧小结

| 层级 | 作用 |
|------|------|
| `hyperon.runner.Metta.run` / `evaluate_atom` | 经 `hyperonpy` 调用 Rust runner |
| `RunContext`（Python） | `load_module`、`register_token` 等 C API，与 atom 算子无一一对应 |
| `ext.register_atoms` / `register_tokens` / `grounded` | 扩展 tokenizer；与 corelib 内置 `*-atom` 并行存在时需注意重复注册（参见 `stdlib.metta` 中关于 `help!` 的 TODO 注释） |

内置 `*-atom` 算子均在 Rust `stdlib/atom.rs` 注册，不经 Python 定义。

---

## 13. 参考索引（文件路径）

- Rust grounded 与类型：`lib/src/metta/runner/stdlib/atom.rs`，`lib/src/metta/types.rs`
- 解释器原语：`lib/src/metta/interpreter.rs`
- Stdlib MeTTa 源码：`lib/src/metta/runner/stdlib/stdlib.metta`
- 字符串排序：`lib/src/metta/runner/stdlib/string.rs`
- Python Runner：`python/hyperon/runner.py`
