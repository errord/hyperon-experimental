---
title: 字符串操作（MeTTa → Python → Rust）
order: 12
---

# 文档 12：字符串操作全链实现

本文档区分 **Rust 核心** 与 **Python 扩展** 的字符串相关原语：

| 能力 | 主要实现语言 | 源文件 |
|------|----------------|--------|
| **`println!`**、**`format-args`**、**`sort-strings`**、双引号 **grounded `Str`** 分词 | Rust | `lib/src/metta/runner/stdlib/string.rs` |
| **`repr`**、**`parse`**、**`stringToChars`**、**`charsToString`**、**`Char` 字面量分词** | Python | `python/hyperon/stdlib.py` |
| **`Str` 类型**、**`atom_to_string`**、**`StrSerializer`** | Rust | `hyperon-atom/src/gnd/str.rs` |
| **字符串字面量转义**、**无 tokenizer 时的词法形态** | Rust | `lib/src/metta/text.rs` |
| **`sealed`**（变量唯一化，常与含字符串的模板联用） | Rust + MeTTa | `lib/src/metta/runner/stdlib/core.rs`；`stdlib.metta` |

---

## 1. Rust：`string.rs` 总览

文件：`lib/src/metta/runner/stdlib/string.rs`。

### 1.1 `PrintlnOp`（`println!`）

**第 10–32 行**。

- **`grounded_op!(PrintlnOp, "println!")`**（第 13 行）配合 **`mod.rs` 宏**（第 23–37 行）。
- **类型**：`-> %Undefined% Unit`（**`ARROW_SYMBOL`, `ATOM_TYPE_UNDEFINED`, `UNIT_TYPE`**，第 16–17 行）。
- **`execute`**（第 25–31 行）：
  - 恰好 **一个** 参数；否则 **`ExecError::from("println! expects single atom as an argument")`**（第 27 行）。
  - 使用 **`atom_to_string(atom)`**（第 29 行）格式化为 **Rust `String`**，再 **`println!`** 输出到标准输出（第 29 行）。
  - 返回 **`unit_result()`**（第 30 行），即 **`Ok(vec![UNIT_ATOM])`**（`mod.rs` 第 41–43 行）。

**`atom_to_string`** 定义见 **`str.rs`**（下一节）。

### 1.2 `FormatArgsOp`（`format-args`）

**第 34–62 行**。

- **`grounded_op!(FormatArgsOp, "format-args")`**（第 37 行）。
- **类型**：`-> String Expression String`（第 42–43 行）：**格式串**、**参数表达式**、**结果串**。
- **依赖**：**`dyn_fmt::AsStrFormatExt`**（第 39 行），对 **`&str`** 提供 **`.format(...)`**（第 59 行）。
- **`execute`**（第 51–61 行）：
  1. 第一参数：**`Str::from_atom`**（第 54 行）；失败则 **`format-args expects format string as a first argument and expression as a second argument`**（第 53 行）。
  2. 第二参数：转为 **`&ExpressionAtom`**（第 55 行）。
  3. 对子节点逐个 **`atom_to_string`**（第 56–58 行），得到 **`Vec<String>`**。
  4. **`format.format(args.as_slice())`**（第 59 行）—— 占位符为 **`{}`**（与 **`dyn_fmt`** 约定一致）。
  5. 结果 **`Str::from_string(res)`** 包装为 grounded（第 60 行）。

### 1.3 `sort-strings`

**第 64–76 行** 定义函数 **`sort_strings`**（非 `grounded_op` 宏生成）。

- 第一个参数须为 **`ExpressionAtom`**，子项均为 **`Str`** grounded（第 66–70 行）。
- **`strings.sort()`**（第 72 行）按 **`&str`** 默认序排序。
- 返回 **`Atom::expr(sorted)`**（第 74–75 行），子节点为新的 **`Str`** 原子。

**注册**：见 **第 85–89 行** 的 `GroundedFunctionAtom::new`，名 **`sort-strings`**，类型 **`(-> Expression Expression)`**。

### 1.4 `register_context_independent_tokens`

**第 78–90 行**：

- **`println!`**、**`format-args`**：与其它算子相同，**`Atom::gnd` + `register_token`**（第 79–82 行）。
- **双引号串整体匹配**：正则 **`(?s)^".*"$`**（第 83 行），回调 **去掉首尾字符**（假定首尾为 `"`），**`Str::from_string`**（第 83–84 行）。  
  - **`(?s)`**：`.` 匹配换行，故 **多行字符串** 可被该规则命中（若整 token 被识别为一条带引号的串）。  
  - 注意：该规则与 **S 表达式解析器** 产出的 token 形态配合使用；解析器先按 **`parse_string`** 规则构造 **带转义展开的 `parsed_text`**，再交给 tokenizer（见 **第 3 节**）。

---

## 2. Rust：`Str` 与 `atom_to_string`（`str.rs`）

文件：`hyperon-atom/src/gnd/str.rs`。

### 2.1 类型与存储

- **`ATOM_TYPE_STRING`**：符号 **`String`**（第 6 行）。
- **`Str(ImmutableString)`**（第 10 行）：底层 **`hyperon_common::immutable_string::ImmutableString`**，可为 **字面量** 或 **堆分配**（**`from_str` / `from_string`**，第 14–19 行）。

### 2.2 `Grounded` 与序列化

- **`type_`** → **`ATOM_TYPE_STRING`**（第 37–40 行）。
- **`serialize`**：**`serializer.serialize_str(self.as_str())`**（第 42–44 行）。

### 2.3 `StrSerializer`（第 90–110 行）

- 实现 **`serial::Serializer::serialize_str`**，写入内部 **`Option<Str>`**（第 95–99 行）。
- **`ConvertingSerializer`**：**`check_type`** 要求 **`gnd.type_() == ATOM_TYPE_STRING`**（第 102–105 行）；**`into_type`** 取出 **`Str`**（第 107–109 行）。
- **`Str::try_from(&Atom)`**（第 59–64 行）经 **`StrSerializer::convert`** 完成 **从任意 grounded atom 的受支持序列化路径** 到 **`Str`** 的转换。

### 2.4 `atom_to_string`（第 112–118 行）

```rust
pub fn atom_to_string(atom: &Atom) -> String {
    match atom {
        Atom::Grounded(gnd) if gnd.type_() == ATOM_TYPE_STRING =>
            Str::from_atom(atom).unwrap().as_str().into(),
        _ => atom.to_string(),
    }
}
```

- **grounded 且运行时类型为 `String`**：返回 **字符串内容本身**（不含 Rust `Debug` 式的额外引号层）。
- **其它原子**：回退 **`atom.to_string()`**。

**`PrintlnOp` / `FormatArgsOp`** 依赖此函数（`string.rs` 第 29、57 行），故 **MeTTa 中 `println!` 对 `Str` 的打印** 与 **对符号/表达式的打印** 行为不同。

### 2.5 `Display` 与 `strip_quotes` / `unescape`

- **`Display for Str`**：**`{:?}` 风格打印内部 `str`**（第 47–50 行），测试 **`str_display_escape`**（第 140–143 行）。
- **`strip_quotes`**（第 74–88 行）：若首尾为 `"`，返回中间子串；否则原样返回。
- **`unescape`**（第 120–126 行）：基于 **`unescaper`** 库，**去掉外层引号并解释转义**；测试见 **第 146–149 行**。

---

## 3. Rust：解析器中的字符串与转义（`text.rs`）

文件：`lib/src/metta/text.rs`。

### 3.1 词法类型

- **`SyntaxNodeType::StringToken`**（第 112–113 行）：**双引号** 界定的字面量。
- **`parse_token`**（第 520–531 行）：若下一字符为 **`"`**，走 **`parse_string`**（第 522–524 行）。

### 3.2 `parse_string`（第 534–589 行）

流程概要：

1. 起始 **`"`**（第 538–543 行）；缺失则 **不完整节点** **`"Double quote expected"`**（第 541–542 行）。
2. 循环读字符直至 **未转义的闭合 `"`**（第 544–548 行），将 **外层引号** 保留在 **`token` 字符串** 中（第 539、546–547 行）。
3. **反斜杠转义**（第 550–582 行）：
   - **`'` `"` `\`** → 对应字符（第 556 行）
   - **`n` `r` `t`** → 换行、回车、制表（第 557–559 行）
   - **`x`** → **两位十六进制**，值须 **≤ 0x7F**（第 560–565、592–608 行）；否则 **无效转义**（第 561–563 行）
   - **`u`** → **`\u{...}`** 形式 Unicode（第 566–571、611–636 行）
   - 其它 → **无效转义**（第 572–574 行）
4. **未闭合**：**`"Unclosed String Literal"`**（第 587–588 行）。

### 3.3 与 `Tokenizer` 的交接

**`SyntaxNode::as_atom`**（第 208–219 行）：对 **`StringToken` / `WordToken`**，将 **`parsed_text` 整串** 交给 **`tokenizer.find_token`**；若命中构造器则 **构造 grounded / 特殊 atom**，否则 **`Atom::sym(token_text)`**。

因此：

- **未注册** 双引号 **`Str`** 规则时，`"te st"` 类 token 常成为 **符号原子**（测试 **`test_text_quoted_string`**，**第 708–711 行**：**`expr!("\"te st\"")`** — 注意此处 **符号名含引号字符**）。
- **注册** `string.rs` 第 83–84 行规则后，**完整双引号串** 可变为 **`Str` grounded**。

### 3.4 转义相关测试（同文件 **第 714–727、783–793、816–857 行**）

覆盖 **`\t` `\n`、`\x1b`、转义引号、`\x7F`、非法 `\xFF`**、**`\u{0123}`** 成功与多种失败写法等。

---

## 4. 核心库注册顺序（`mod.rs`）

**`register_context_independent_tokens`**（`lib/src/metta/runner/stdlib/mod.rs` **第 85–94 行**）中：

- **`math::register_context_independent_tokens`**（第 89 行）在 **`string::...`**（第 91 行）**之前**。
- **`string::register_context_independent_tokens`** 在 **`arithmetics`** 之后，为 **字符串字面量与 I/O 类原语** 追加规则。

**`stdlib/mod.rs` 集成测试 `test_string_parsing`**（**第 747–767 行**）在 **`EnvBuilder::test_env()`** 下运行，此时 **核心 string 分词与 `id` 规则** 均已加载，故 **`"test"`** 等被解析为 **`Str`** grounded。

---

## 5. Python：`stdlib.py` 文本原语

文件：`python/hyperon/stdlib.py`。

### 5.1 `text_ops`（第 61–86 行）

装饰器 **`@register_atoms(pass_metta=True)`**（第 61 行），在 **`_priv_register_module_tokens`**（`runner.py` 第 372–392 行）执行时向 **tokenizer** 注册：

| 键（正则） | `OperationAtom` | 行为摘要 |
|------------|-----------------|----------|
| **`repr`** | 第 74–75 行 | **`lambda a: [ValueAtom(repr(a), 'String')]`**，**`unwrap=False`** |
| **`parse`** | 第 76 行 | **`parseImpl(s, metta)`** |
| **`stringToChars`** | 第 77–78 行 | 子项为 **`ValueAtom(Char(c))`** |
| **`charsToString`** | 第 79–80 行 | 拼接子节点字符 |

类型签名数组：**`['Atom', 'String']`**、**`['String', 'Atom']`** 等（第 75–80 行），供类型检查使用。

### 5.2 `parseImpl`（第 51–58 行）

- 从 grounded atom 取 **Python `str`**：**`atom.get_object().content`**（第 53 行）。
- 使用 **`repr(s)[1:-1]`** 剥去 Python 外层引号，将 **中间层** 交给 **`SExprParser(...).parse(metta.tokenizer())`**（第 56 行）。
- 返回 **单元素列表** 含解析得到的 **atom**；异常 → **`IncorrectArgumentError`**（第 57–58 行）。

**全链**：MeTTa **`parse`** 调用 → **Python 函数** → **`SExprParser`**（`base.py` 第 374–380 行）→ **`hyperonpy` `CSExprParser::parse`**（`hyperonpy.cpp` 第 709–712 行附近）→ **Rust 解析器**。

### 5.3 `stringToChars` / `charsToString`（第 77–80 行）

- **`stringToChars`**：**`str(s)[1:-1]`** 去掉 **字符串值的表示** 两端引号，再迭代 Python 字符（**每个字符** 包装为 **`ValueAtom(Char(c))`**）。
- **`charsToString`**：对每个子 atom **`str(c)[1:-1]`** 取单字符，再 **`"".join(...)`**，返回 **`ValueAtom(..., 'String')`**。

与 **Rust `Str`** 无直接类型共享；经 **hyperonpy** 在边界处转为 **Rust atom** 时再映射到相应 grounded 表示。

### 5.4 `type_tokens`（第 88–93 行）

- **`\'[^\']\'`**：单字符 **`Char`**（第 91 行）。
- **`regex:"[^"]*"`**：**`RegexMatchableObject`**（第 92 行）。

测试见 **`python/tests/test_stdlib.py`** **第 20–48 行**（**`repr` / `parse` / `stringToChars` / `charsToString`**）。

### 5.5 `Char` 类（第 11–27 行）

**`__repr__`** 为 **`'{self.char}'`** 风格（第 21–22 行），与 **`stringToChars`** 使用 **`ValueAtom(Char)`** 时的显示一致。

---

## 6. Python：`MeTTa.run` 与 `stdlib` 加载顺序

1. **`MeTTa.__init__`**（`runner.py` 第 132 行）→ **`metta_new_with_stdlib_loader`**（`hyperonpy.cpp` 第 1096–1098 行）。
2. Rust **`CoreLibLoader`** 先注册 **Rust tokenizer**（含 **`string.rs`**、`arithmetics.rs` 等），并解析 **`stdlib.metta`**。
3. **`_priv_load_module_stdlib`**（`runner.py` 第 354–356 行）再 **`import hyperon.stdlib`** 并注册 **Python atoms/tokens**。

因此 **同名 token** 若 Rust 与 Python **均注册**，**后注册者覆盖先注册者**（在 **`Tokenizer::find_token` 自尾向前** 的语义下，**后 `move_back` / append 的规则优先**，见 **`text.rs` 第 74–80 行** 与 **`Tokenizer::move_back` 注释** **第 66–71 行**）。**`stdlib.metta` 第 1311–1312 行** 注释提醒 **`+` 等与 Python 双实现时文档工具的问题**；字符串侧 **`repr`/`parse`** 以 **Python** 为主实现。

---

## 7. `sealed` 与字符串模板

### 7.1 Rust：`SealedOp`（`core.rs` 第 76–113 行）

- **`execute`**（第 91–111 行）：第二参数 **`term_to_seal`** 中，**不在** 第一参数 **忽略列表** 内的 **`VariableAtom`** 经 **`CachingMapper` + `make_unique()`** 替换（第 98–105 行）。
- **返回** 单元素向量，为 **重写变量后的表达式**（第 108、111 行）。

### 7.2 MeTTa：`stdlib.metta` 中的使用

**`filter-atom` / `map-atom`** 实现中（约 **第 458–480 行**）对 **`$filter` / `$map` 表达式** 使用 **`(sealed ($var) ...)`**，避免 **外层模式变量** 与 **内层模板变量** 错误绑定。

**与字符串的关系**：模板中可含 **`Str` grounded** 或 **符号**；**`sealed` 不解析字符串内容**，只改 **变量节点**。若需 **在含 `$x` 的 quoted 数据上防捕获**，应使用 **`quote`/`unquote`** 与 **`sealed`** 组合（参见 **`stdlib/mod.rs` `metta_quote_unquote` 测试** 第 347–357 行）。

### 7.3 分词注册

**`core.rs` 第 343–344 行**：**`sealed`** → **`SealedOp`**。

---

## 8. `format-args` 在 `stdlib.metta` 中的文档

**`lib/src/metta/runner/stdlib/stdlib.metta` 第 1285–1290 行** **`@doc format-args`**：说明 **`{}`** 占位与子表达式中 atom 的对应关系；实现以 **`string.rs` 第 51–61 行** 为准。

---

## 9. 交叉对比：`repr`（Python）与 Rust 打印

- **Python `repr`**（`stdlib.py` 第 74–75 行）：对 **任意 atom** 取 **Python 层 `repr(a)`**，再作为 **`ValueAtom(..., 'String')`**。**`python/tests/test_grounded_type.py` 第 47–54 行** 对比 **Rust 与 Python** 对不可见字符的 **`repr`** 差异。
- **Rust `println!`**（`string.rs` 第 29 行）：使用 **`atom_to_string`**，对 **`Str`** 打印 **裸内容**（**`str.rs` 第 112–118 行**）。

---

## 10. 速查行号

| 主题 | 文件 | 行号（约） |
|------|------|------------|
| `PrintlnOp` | `string.rs` | 10–32, 79–80 |
| `FormatArgsOp` | `string.rs` | 34–62, 81–82 |
| `sort-strings` | `string.rs` | 64–76, 85–89 |
| 双引号 → `Str` | `string.rs` | 83–84 |
| `Str` / `StrSerializer` / `atom_to_string` | `str.rs` | 全文；`atom_to_string` 112–118 |
| `parse_string` 转义 | `text.rs` | 534–636 |
| `repr` / `parse` / chars | `stdlib.py` | 51–86, 88–93 |
| `sealed` | `core.rs` | 76–113, 343–344 |
| 核心注册顺序 | `mod.rs` | 85–94 |

---

## 11. FAQ

**Q：MeTTa 源码里的 `"hello"` 何时是 `Str`，何时是带引号的符号？**  
A：取决于 **tokenizer** 是否包含 **`string.rs` 第 83–84 行** 的规则及 **匹配顺序**。**仅 `SExprParser` + 空 tokenizer** 时，常见为 **符号**（**`text.rs` 第 708–711 行**）。

**Q：`format-args` 的占位符必须是 `{}` 吗？**  
A：由 **`dyn_fmt`** 决定；当前实现调用 **`.format(args.as_slice())`**（**`string.rs` 第 59 行**），与 **`stdlib.metta` 文档** 一致。

**Q：Python `parse` 与 Rust 内建解析有何关系？**  
A：**`parse`** 在 Python 中 **二次调用** **`SExprParser`**，使用 **当前 runner 的 tokenizer**，因此 **扩展 token**（Rust 或 Python 注册）均会影响解析结果（**`stdlib.py` 第 56 行**）。

**Q：`sealed` 会密封字符串里的 `$var` 吗？**  
A：**不会**自动解析字符串内部文本；仅遍历 **原子树中的 `VariableAtom` 节点**（**`core.rs` 第 101–105 行**）。

---

## 12. 测试与验证建议

- **Rust 字符串分词与转义**：**`text.rs` `mod tests`**（第 695 行起）；**`str.rs` 第 136–158 行**。
- **Rust 核心集成**：**`stdlib/mod.rs` `test_string_parsing`**（第 747–767 行）。
- **Python stdlib**：**`python/tests/test_stdlib.py`**（第 20–48 行）。
- **Grounded 类型**：**`python/tests/test_grounded_type.py`**（**`repr`**、**`Number`** 等）。

---

## 13. 实现者备忘：维护 `string.rs` 时注意

1. **`atom_to_string`** 与 **`Str::Display`** 语义不同；修改其一需检查 **`PrintlnOp`/`FormatArgsOp`** 输出是否仍符合预期。  
2. **双引号正则 `(?s)^".*"$`** 要求 **整个 token** 匹配；若未来 lexer 改为 **不含外层引号的 string token**，需同步调整回调（**第 83–84 行**）。  
3. **Python `charsToString`** 假设子节点 **`str(c)[1:-1]`** 为单字符（**`stdlib.py` 第 79 行**）；与 **Rust `Char` token**（**第 91 行**）组合使用时需保持 **表示一致**。  
4. **`sort-strings`** 错误消息固定为 **`sort-strings expects expression with strings as a first argument`**（**`string.rs` 第 65 行**）；与 **`TryInto` 失败** 共用同一字符串（第 66 行）。

---

以上行号针对 **`hyperon-experimental`** 当前树；若分支移动实现，请用符号搜索（**`PrintlnOp`**, **`FormatArgsOp`**, **`text_ops`**, **`parse_string`**）重新对齐。
