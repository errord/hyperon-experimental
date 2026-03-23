---
title: MeTTa 文档系统全链分析
order: 15
---

# 文档 15：文档系统（@doc / help! / help-space!）

本文档说明：文档**不是**单独的 Rust `DocOp` 算子，而是以**普通原子**形式存放在 atom space 中的 `@doc` 表达式；`get-doc`、`help!`、`help-space!` 在 `stdlib.metta` 中通过 `unify`、`case`、`match` 等与类型与 `println!` 组合实现。Python 与 C 路径与常规 MeTTa 程序相同：经 Runner 解析与解释器执行，无独立 Python Doc API。

---

## 1. 核心结论：文档即数据原子

- `@doc`、`@desc`、`@params`、`@param`、`@return` 等在 `stdlib.metta` 中被声明为**带类型的符号/构造子**（`:` 声明），并与「被文档化的函数/原子」的 `=` 规则**并列**存在于同一模块 space。
- 查询文档时，算法在**给定的 space**（通常是 `top` 模块 space 或去掉依赖的模块主空间）上做模式匹配，把 `(@doc ...)` 与被查名称关联起来。
- **没有** `lib/src/.../doc.rs` 一类专门算子；`help!` 的副作用来自 grounded `println!`（`stdlib/string.rs`）。

---

## 2. `@doc` 与辅助构造子的类型声明（精确行号）

下列片段全部来自 `stdlib.metta` 的「Documentation formatting functions」一节。

### 2.1 `@doc` 本体

```709:718:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc @doc
  (@desc "Used for documentation purposes. Function documentation starts with @doc")
  (@params (
    (@param "Function name")
    (@param "Function description. Starts with @desc")
    (@param "(Optional) parameters description starting with @params which should contain one or more @param symbols")
    (@param "(Optional) description of what function will return. Starts with @return")))
  (@return "Function documentation using @doc-formal"))
(: @doc (-> Atom DocDescription DocInformal))
(: @doc (-> Atom DocDescription DocParameters DocReturnInformal DocInformal))
```

说明：

- 重载 arity：`@doc` 既可接「名称 + 描述 + 可选 @params/@return」，也可接更长形式；类型用 `DocDescription`、`DocParameters` 等**文档专用类型符号**区分。

### 2.2 `@desc`：描述字段

```720:725:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc @desc
  (@desc "Used for documentation purposes. Description of function starts with @desc as a part of @doc")
  (@params (
    (@param "String containing function description")))
  (@return "Function description"))
(: @desc (-> String DocDescription))
```

### 2.3 `@param`：参数说明（含形式化重载）

```727:733:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc @param
  (@desc "Used for documentation purposes. Description of function parameter starts with @param as a part of @params which is a part of @doc")
  (@params (
    (@param "String containing parameter description")))
  (@return "Parameter description"))
(: @param (-> String DocParameterInformal))
(: @param (-> DocType DocDescription DocParameter))
```

### 2.4 `@return`：返回值说明

```735:741:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc @return
  (@desc "Used for documentation purposes. Description of function return value starts with @return as a part of @doc")
  (@params (
    (@param "String containing return value description")))
  (@return "Return value description"))
(: @return (-> String DocReturnInformal))
(: @return (-> DocType DocDescription DocReturn))
```

### 2.5 `@params`：参数列表容器

```782:787:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc @params
  (@desc "Used for function documentation purposes. Contains several @param entities with description of each @param")
  (@params (
    (@param "Several (@param ...) entities")))
  (@return "DocParameters containing description of all parameters of function in form of (@params ((@param ...) (@param ...) ...))"))
(: @params (-> Expression DocParameters))
```

### 2.6 `@doc-formal`：规范化输出形状（供 `help!` 打印）

```743:755:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc @doc-formal
  (@desc "Used for documentation purposes. get-doc returns documentation starting with @doc-formal symbol. @doc-formal contains 6 or 4 parameters depending on the entity being described (functions being described using 6 parameters, atoms - 4 parameters)")
  (@params (
    (@param "Function/Atom name for which documentation is to be displayed. Format (@item name)")
    (@param "Contains (@kind function) or (@kind atom) depends on entity which documentation is displayed")
    (@param "Contains type notation of function/atom")
    (@param "Function/atom description")
    (@param "(Functions only). Description of function parameters")
    (@param "(Functions only). Description of function's return value")))
  (@return "Expression containing full documentation on function"))
(: @doc-formal (-> DocItem DocKindFunction DocType DocDescription DocParameters DocReturn DocFormal))
(: @doc-formal (-> DocItem DocKindAtom DocType DocDescription DocFormal))
(: @doc-formal (-> DocItem DocKindFunction DocType DocDescription DocFormal))
```

辅助：`@item`、`@type`、`(@kind function)`、`(@kind atom)` 等同文件 757–780 行。

---

## 3. 文档原子的**存储形态**（作者如何写）

### 3.1 函数：典型四段式

示例（文件开头即出现）：

```1:7:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc =
  (@desc "A symbol used to define reduction rules for expressions.")
  (@params (
    (@param "Pattern to be matched against expression to be reduced")
    (@param "Result of reduction or transformation of the first pattern") ))
  (@return "Not reduced itself unless custom equalities over equalities are added") )
(: = (-> $t $t %Undefined%))
```

空间中**实际存在**的原子包括：

1. 一条 `(@doc = (@desc ...) (@params ...) (@return ...))`（作为普通表达式原子加入 space）。
2. 一条 `(: = (-> $t $t %Undefined%))` 类型声明。
3. 以及后续的 `(= ...)` 规则（若有）。

三者通过**首符号 `=`** 关联；`get-doc` 在 space 中查找以 `@doc` 开头且第二个子项为被文档化名称的模式。

### 3.2 仅类型、无等式重写规则的符号

例如 `ErrorType`：

```9:10:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(@doc ErrorType (@desc "Type of the atom which contains error"))
(: ErrorType Type)
```

此处 `@doc` 为二元形式：`(@doc ErrorType (@desc "..."))`，无 `@params` / `@return`。

---

## 4. `get-doc`：从 space **查询**并归一化为 `@doc-formal`

### 4.1 入口：按 metatype 分支

```795:800:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(: get-doc (-> SpaceType Atom %Undefined%))
(= (get-doc $space $atom)
  (let $meta-type (get-metatype $atom)
    (case $meta-type (
      (Expression (get-doc-atom $space $atom))
      ($_ (get-doc-single-atom $space $atom)) ))))
```

- 若查询名本身是**表达式**（少见），走 `get-doc-atom`。
- 否则走 `get-doc-single-atom`（函数名或原子名）。

### 4.2 `get-doc-single-atom`：区分「函数类型」与普通原子

```809:813:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(= (get-doc-single-atom $space $atom)
  (let $type (get-type-space $space $atom)
    (if (is-function $type)
      (get-doc-function $space $atom $type)
      (get-doc-atom $space $atom) )))
```

依赖：

- `get-type-space`：grounded 算子，`atom.rs` 中 `GetTypeSpaceOp`（433–446 行）。
- `is-function`：`stdlib.metta` 371–385 行，内部用 `get-metatype`、`size-atom`、`decons-atom` 判断箭头类型。

### 4.3 `get-doc-function`：在 space 上与 `@doc` **统一**

```823:828:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(= (get-doc-function $space $name $type)
  (unify $space (@doc $name $desc (@params $params) $ret)
    (let $type' (if (== $type %Undefined%) (undefined-doc-function-type $params) (cdr-atom $type))
    (let ($params' $ret') (get-doc-params $params $ret $type')
      (@doc-formal (@item $name) (@kind function) (@type $type) $desc (@params $params') $ret')))
    Empty ))
```

语义要点：

- `(unify $space (@doc $name ...))` 并不是把 space 当成「值」与表达式统一；在 MeTTa 实现中，该模式由解释器对 **`unify` 与 space 参数**的特殊处理支持，使「在当前 space 中查找匹配的 `@doc` 原子」生效（与 `type-cast` 等同源模式一致）。
- 若找不到匹配，结果为 `Empty`。

`get-doc-params`（850–860 行）把 `@param` 字符串与 `cdr-atom` 后的函数类型分量 zip 成带 `(@type ...)` 的形式，供 `help-param!` 打印。

### 4.4 `get-doc-atom`：表达式名或普通原子

```869:875:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(= (get-doc-atom $space $atom)
  (let $type (get-type-space $space $atom)
    (unify $space (@doc $atom $desc)
      (@doc-formal (@item $atom) (@kind atom) (@type $type) $desc)
      (unify $space (@doc $atom $desc' (@params $params) $ret)
        (get-doc-function $space $atom %Undefined%)
        Empty ))))
```

先尝试「短 `@doc`」，再尝试「长 `@doc`」并回退到函数文档路径。

---

## 5. `help!`（HelpOp）：打印 `get-doc` 结果

**说明**：仓库中 `help!` 在 `stdlib.metta` 以**等式**定义；若存在同名 grounded `HelpOp`，以 runner 实际注册的 tokenizer 为准。用户可见行为由下列 MeTTa 规则描述。

### 5.1 无参：默认 `corelib`

```888:889:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(: help! (-> (->)))
(= (help!) (help! corelib))
```

### 5.2 有参：`help-internal!` + `case` 匹配 `@doc-formal` 形状

```883:910:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(: help! (-> Atom (->)))
(= (help! $atom)
  (case (help-internal! $atom) (
    (Empty (println! (format-args "No documentation found for {}" ($atom))))
    ($other $other) )))

(: help-internal! (-> Atom (->)))
(= (help-internal! $atom)
  (let $top-space (mod-space! top)
  (case (get-doc $top-space $atom) (
    ((@doc-formal (@item $item) (@kind function) (@type $type) (@desc $descr)
                 (@params $params)
                 (@return (@type $ret-type) (@desc $ret-desc)))
      (let () (println! (format-args "Function {}: {} {}" ($item $type $descr)))
      (let () (println! (format-args "Parameters:" ())
      (let () (for-each-in-atom $params help-param!)
      (let () (println! (format-args "Return: (type {}) {}" ($ret-type $ret-desc)))
      () )))))
    ((@doc-formal (@item $item) (@kind function) (@type $type) (@desc $descr))
      (let () (println! (format-args "Function {} (type {}) {}" ($item $type $descr)))
      () ))
    ((@doc-formal (@item $item) (@kind atom) (@type $type) (@desc $descr))
      (let () (println! (format-args "Atom {}: {} {}" ($item $type $descr)))
      () ))
    (Empty Empty)
    ($other (Error $other "Cannot match @doc-formal structure") )))))
```

链：

1. `mod-space!`：加载模块并返回 space（`stdlib/module.rs` 183–196 行）。
2. `get-doc`：§4。
3. `println!` / `format-args`：grounded（`stdlib/string.rs`）。
4. `for-each-in-atom` + `help-param!`：941–943、952–957 行。

### 5.3 `Symbol` 重载：把整个模块的文档打出来

```912:916:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(: help-internal! (-> Symbol (->)))
(= (help-internal! $mod)
  (case (module-space-no-deps (mod-space! $mod)) (
    ((Error $atom $msg) Empty)
    ($space (help-space! $space)) )))
```

即：`!(help! mymod)` → `mod-space!` 取模块 space → `module-space-no-deps` 去掉依赖子空间（`stdlib/module.rs` 199–207 行）→ `help-space!`。

---

## 6. `help-space!`：枚举 space 中所有 `@doc`

定义（注意文件中存在**两条** `(= (help-space! $space) ...)`，后一条覆盖/并列行为取决于 space 中规则叠加方式；二者分别匹配「带 @params/@return」与「仅 @desc」的 `@doc`）：

```923:933:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
(: help-space! (-> SpaceType (->)))
(= (help-space! $space)
    (let $_ (collapse
      (unify $space (@doc $name (@desc $desc) $params $ret)
        (let () (println! (format-args "{}\n\t{}" ($name $desc))) Empty)
        Empty )) ())
(= (help-space! $space)
    (let $_ (collapse
      (unify $space (@doc $name (@desc $desc))
        (let () (println! (format-args "{}\n\t{}" ($name $desc))) Empty)
        Empty )) Empty))
```

语义：

- `collapse` 收集所有使 `unify` 成功的分支（与 `superpose` / 非确定性求值配合）。
- 每个匹配打印一行「名称 + 缩进描述」。

---

## 7. 与 `get-type` / `get-metatype` 的衔接（Rust）

文档系统依赖的类型查询在 Rust 中实现：

- `get-type-space` → `GetTypeSpaceOp` → `get_atom_types`（`atom.rs` 433–446；`types.rs` 327–334）。
- `get-metatype` → `GetMetaTypeOp` → `types::get_meta_type`（`atom.rs` 409–415；`types.rs` 606–612）。

`help!` 打印的「type」字符串来自 `@type` 包装后的原子，其底层仍是对 space 中 `(: ...)` 的查询结果。

---

## 8. Python 路径

- 用户在 Python 中执行 `metta.run("!(help! +)")` 与 Rust REPL 相同：`'!(help! +)'` → `SExprParser` → `RunnerState` → 解释器执行 `help!` 规则 → 调用 `println!` 等 grounded 算子。
- `hyperon.runner.Metta` 无单独的 `help()` 方法；文档查询逻辑全部在 MeTTa 源码 `METTA_CODE` / `stdlib.metta` 中。

`CoreLibLoader` 将 `include_str!("stdlib.metta")` 载入 corelib 模块（`stdlib/mod.rs` 102、117 行起），因此上述定义在**默认 Runner** 中可用。

---

## 9. 已知限制（源码内 TODO）

`stdlib.metta` 中的注释：

```1305:1312:d:\dev\hyperon-experimental\lib\src\metta\runner\stdlib\stdlib.metta
; TODO: help! not working for &self (segmentation fault)
; TODO: help! not working for operations which are defined in both Python and
; Rust standard library: +, -, *, /, %, <, >, <=, >=, ==
```

含义：`get-doc`/`help!` 依赖 space 中**唯一、可匹配**的 `@doc` 与 `(: ...)`；`&self` 或重复注册 token 时可能出现查找失败或实现缺陷。

---

## 10. 小结表

| 概念 | 实现性质 | 主要位置 |
|------|----------|----------|
| `@doc` / `@desc` / `@params` / `@param` / `@return` | Space 中的普通原子 + `:` 类型声明 | `stdlib.metta` 706–787 行等 |
| `get-doc` | MeTTa 等式（`unify` + `get-type-space`） | `stdlib.metta` 795–875 行 |
| `help!` | MeTTa 等式 + `println!` | `stdlib.metta` 877–910 行 |
| `help-space!` | MeTTa 等式 + `collapse` + `unify` | `stdlib.metta` 918–933 行 |
| 类型查询 | Rust grounded / `types.rs` | `atom.rs`, `types.rs` |

---

## 11. 参考路径

- `lib/src/metta/runner/stdlib/stdlib.metta` — 文档与 `help!` 的完整定义与行号引用基准
- `lib/src/metta/runner/stdlib/string.rs` — `println!`、`format-args`
- `lib/src/metta/runner/stdlib/module.rs` — `mod-space!`、`module-space-no-deps`
- `lib/src/metta/runner/stdlib/atom.rs` — `get-type`、`get-type-space`、`get-metatype`
- `lib/src/metta/types.rs` — `get_atom_types`、`get_meta_type`
- `python/hyperon/runner.py` — Runner 入口
