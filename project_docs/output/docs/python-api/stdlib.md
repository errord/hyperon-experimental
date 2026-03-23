---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 模块 `hyperon.stdlib` — 公共 API

Python 层附加标准库：在 **MeTTa** 初始化时通过 `_priv_load_module_stdlib` 自动加载（导入 `hyperon.stdlib` 并扫描注册函数）。

## 类型与辅助类

### `Char`

单字符类型；`str(char)` / `repr` 与相等比较。

### `RegexMatchableObject(MatchableObject)`

- 内容字符串可把 `[[`/`]]`/`~` 转成括号与空格。
- `match_(atom)`：若模式为 `regex:<pattern>`，对 **String** **Atom** 做不区分大小写匹配。

## 注册函数

### `@register_atoms(pass_metta=True) def text_ops(metta)`

注册：

| Token | 操作 | 行为概要 |
|-------|------|-----------|
| `repr` | `repr` | **Atom** → **String**（`repr` 文本） |
| `parse` | `parse` | **String** → 解析为 **Atom** |
| `stringToChars` | 字符串 → **Char** 子表达式 |
| `charsToString` | **Char** 子表达式 → **String** |

### `@register_tokens def type_tokens()`

- `\'.\'`：单引号 **Char** 字面量。
- `regex:"..."`：**RegexMatchableObject** **Grounded**。

## 模块解析辅助

- `import_from_module(path, mod=None)`
- `find_py_obj(path, mod=None)`
- `get_py_atom(path, typ=AtomType.UNDEFINED, unwrap=True, mod=None)`

用于从 Python 路径解析对象并包装为 **Atom**（具体行为见源码与 `test_stdlib.py`）。

## 依赖说明

该模块依赖 `hyperon.atoms`、`hyperon.base`、`hyperon.ext`；扩展自己的 **stdlib** 时可仿照其 `@register_atoms` / `@register_tokens` 模式。
