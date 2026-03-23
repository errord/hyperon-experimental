---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# Python API 快速入门

## 安装

见 `installation.md`。

## 运行 **MeTTa** 代码

```python
from hyperon.runner import MeTTa

metta = MeTTa()
print(metta.run("(+ 40 2)", flat=True))
```

## 构造 **Atom**

```python
from hyperon import E, S, V, G, ValueAtom

expr = E(S("+"), ValueAtom(1), ValueAtom(2))
print(metta.evaluate_atom(expr))
```

## 注册自定义操作

```python
from hyperon.atoms import OperationAtom, ValueAtom

def triple(x):
    return 3 * x

metta.register_atom("triple", OperationAtom("triple", triple, ["Number", "Number"]))
print(metta.run("(triple 10)", flat=True))
```

## 自定义 **Tokenizer**

```python
metta.register_token(r"foo\d+", lambda t: ValueAtom(int(t[3:])))
```

**正则**语法遵循 **Rust** `regex` crate。

## 单步调试

```python
from hyperon.runner import RunnerState

state = RunnerState(metta, "(+ 1 1)")
while not state.is_complete():
    state.run_step()
    print(state.current_results())
```

## 进一步阅读

- `../python-api/runner.md`、`../python-api/atoms.md`、`../python-api/base.md`
- `../extension-dev/python-extension.md`
