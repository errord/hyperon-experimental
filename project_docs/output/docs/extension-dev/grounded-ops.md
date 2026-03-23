---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# Grounded 操作开发

## Python：`OperationAtom` 与 `OperationObject`

```python
from hyperon.atoms import OperationAtom, ValueAtom, E, S, AtomType

def add(a: int, b: int):
    return a + b

op = OperationAtom("my-add", add, ["Number", "Number", "Number"], unwrap=True)
```

- **`type_names`**：箭头类型链，用于文档与部分检查；最后一项为返回类型。
- **`unwrap=False`**：`lambda a, b: [E(S("foo"), a)]` 等形式，完全控制 **Atom** 级行为。

## 返回约定

- **`unwrap=True`**：可返回 Python 标量、`None`（→ **UNIT**）、或可调用（包装为新的 **OperationAtom**）。
- **`unwrap=False`**：必须返回 **iterable**，元素为 **Atom**。

## 高级：`MatchableObject`

对需要参与 **Space** **match** 的值，子类化 `MatchableObject` 并实现 `match_(atom) -> list[dict]`（绑定字典列表，依实现而定）。

## Rust 侧（参考）

核心 **stdlib** 在 `lib/src/metta/runner/stdlib/*.rs` 中注册 **GroundedFunctionAtom**；若向上游贡献内置操作，需同步 **tokenizer** 注册与测试。

## 错误与类型

- 参数错误：抛 `IncorrectArgumentError` 或返回空结果，视期望的归约语义而定。
- 使用 `MettaError("msg")` 让 `OperationObject.execute` 生成 `(Error msg)` 风格原子。

## 参见

- `python-extension.md`
- `../metta-lang/stdlib-reference.md`
