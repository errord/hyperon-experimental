---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 标准库完整参考（Core + stdlib.metta）

下列操作在默认 **MeTTa** 环境（加载 **CoreLibLoader**）中可用。**签名**列采用 **MeTTa** 箭头类型直觉；部分 **Grounded** 在实现里标注为 `%Undefined%` 返回，表示由解释器按多结果语义处理。

---

## 核心与控制

| 操作 | 概念签名 | 描述 | 示例 |
|------|-----------|------|------|
| `nop` | ` (->)` | 无操作，返回 **Unit** | `(nop)` |
| `pragma!` | ` (->)` | 设置解释器参数；键为 **Symbol** | `(pragma! max-stack-depth 100)` |
| `==` | `(-> $t $t Bool)` | 结构相等 | `(== a a)` |
| `if-equal` | `(-> Atom Atom Atom Atom)` | 若 atom 与 pattern **alpha** 等价则选 then 否则 else | `(if-equal x $a y z)` |
| `sealed` | `(-> Expression Atom Atom)` | 将表达式中未列在忽略列表的变量重命名为唯一变量 | `(sealed ($x) (+ $x $y))` |
| `match` | `(-> Space Atom Atom ...)` | 在 **Space** 上查询 pattern，用 **template** 实例化 | `(match &self (foo $x) $x)` |
| `superpose` | `(-> Expression ...)` | 将子表达式展开为并行分支 | `(superpose (1 2 3))` |
| `capture` | `(-> Atom Atom)` | 在给定 **Space** 上下文中捕获求值（与 **pragma** 配合） | 见测试用例 |

---

## 元求值与折叠（部分为 stdlib.metta）

| 名称 | 描述 |
|------|------|
| `metta` | 对 Atom 在指定类型与 **Space** 下求值（**stdlib.metta**） |
| `collapse` | 将多分支求值结果折叠为单一表达式形式 |
| `collapse-bind` | 类似 `collapse`，保留 **Bindings** 信息 |
| `chain` | 顺序组合求值（**stdlib.metta**） |
| `eval` | 对表达式一步或多步归约（**stdlib.metta**） |
| `_minimal-foldl-atom` | 内部 **fold** 原语（列表聚合） |

---

## 算术与比较（arithmetics）

| 操作 | 签名直觉 | 描述 | 示例 |
|------|-----------|------|------|
| `+` | `(-> Number* Number)` | 求和 | `(+ 1 2 3)` |
| `-` | 二元 | 减法 | `(- 5 2)` |
| `*` | 变元 | 乘法 | `(* 2 3)` |
| `/` | 二元 | 除法 | `(/ 6 2)` |
| `%` | 二元 | 取模 | `(% 7 3)` |
| `<` `>` `<=` `>=` | 二元 **Bool** | 序比较 | `(< 1 2)` |
| `and` `or` `not` `xor` | 逻辑 | 布尔运算 | `(and True False)` |
| `True` `False` | — | 布尔字面量（**Tokenizer**） | `True` |

---

## 数学函数（math）

| 操作 | 描述 |
|------|------|
| `pow-math` `sqrt-math` `abs-math` `log-math` | 幂、平方根、绝对值、对数 |
| `trunc-math` `ceil-math` `floor-math` `round-math` | 取整族 |
| `sin-math` `cos-math` `tan-math` | 三角函数 |
| `asin-math` `acos-math` `atan-math` | 反三角函数 |
| `isnan-math` `isinf-math` | 浮点分类 |
| `PI` `EXP` | 常数 **Grounded** |

---

## Atom 工具（atom）

| 操作 | 描述 | 示例思路 |
|------|------|-----------|
| `get-type` | 查询 Atom 的类型 | 与类型空间联用 |
| `get-type-space` | 在空间上下文中查询类型 | |
| `get-metatype` | **Symbol** / **Expr** / **Grounded** 等元类型 | |
| `min-atom` `max-atom` | 对表达式中 **Number** 求最小/最大 | `(max-atom (1 5 2))` |
| `size-atom` | 子项个数 | |
| `index-atom` | 按下标取子表达式 | |
| `unique-atom` | 按结构去重子项 | |
| `union-atom` | 连接两个表达式子列表 | |
| `intersection-atom` | 子项交集（结构敏感） | |
| `subtraction-atom` | 子项差集 | |

---

## Space 与状态（space）

| 操作 | 描述 | 示例 |
|------|------|------|
| `new-space` | 构造新 **GroundingSpace** | `(bind! &m (new-space))` |
| `add-atom` | 向 **Space** 添加 Atom | `(add-atom &m (foo 1))` |
| `remove-atom` | 移除 Atom | |
| `get-atoms` | 列出空间中所有 Atom | |
| `change-state!` | 更新命名 **state** | 见教程 **state** |
| `get-state` | 读取命名 **state** | |

| 操作 | 描述 |
|------|------|
| `&self` | 当前模块的 **Space**（**Tokenizer** 注入） |

---

## 模块（module）

| 操作 | 描述 |
|------|------|
| `import!` | 按名称/路径加载模块 |
| `include` | 包含 **MeTTa** 源文件 |
| `bind!` | 将符号绑定到 Atom（常用于 **Space** 引用） |
| `mod-space!` | 取得模块关联 **Space** |
| `print-mods!` | 打印已加载模块（调试） |

---

## 字符串与 IO（string）

| 操作 | 描述 |
|------|------|
| `println!` | 打印一行 |
| `format-args` | 格式化字符串构造 |
| 双引号字符串 | **Tokenizer** 识别为 **String** **Grounded** |

---

## 调试（debug）

| 操作 | 描述 |
|------|------|
| `trace!` | 跟踪求值 |
| `print-alternatives!` | 打印当前非确定分支 |
| `=alpha` | **Alpha** 等价比较（调试用） |

---

## 包管理（可选 feature `pkg_mgmt`）

| 操作 | 描述 |
|------|------|
| `register-module!` | 注册可解析模块源 |
| `git-module!` | 自 **Git** 拉取模块 |

---

## Python 附加标准库（`hyperon.stdlib`）

由 Python 模块注册，随 **pip** 安装的 `hyperon` 包加载：

| 操作 / Token | 描述 |
|--------------|------|
| `repr` | `Atom` → 字符串表示 |
| `parse` | 字符串 → `Atom`（经 **Tokenizer**） |
| `stringToChars` / `charsToString` | 字符串与 **Char** 列表互转 |
| `\'x\'` | 单字符 **Char** 字面量 |
| `regex:"..."` | 正则可匹配 **Grounded**（`RegexMatchableObject`） |

另含 `py-atom` 等桥接（见 `python/hyperon/stdlib.py` 与测试）。

---

## 使用说明

1. ** arity**：上表未写 arity 的操作以源码 `execute` 错误消息为准（如 `match` 需 **Space**、**pattern**、**template**）。
2. **版本差异**：`pkg_mgmt` 相关操作仅在对应 **Rust feature** 打开时存在。
3. **stdlib.metta** 中大量 `=` 规则会引入别名（如 `if`、`let`）；若名称冲突，以实际加载顺序与测试为准。
