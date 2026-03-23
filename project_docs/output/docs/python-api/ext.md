---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 模块 `hyperon.ext` — 公共 API

为 **MeTTa** Python 扩展提供装饰器与注册类型标记。

## `RegisterType`（枚举）

- `ATOM`：装饰函数返回 `{regex: Atom}` 映射。
- `TOKEN`：装饰函数返回 `{regex: lambda token -> Atom}` 映射。

## `register_atoms(*args, **kwargs)`

装饰器：将函数返回值注册为 **Atom** 映射。

- `pass_metta=True`：调用时传入 `MeTTa` 实例（用于依赖 **Tokenizer** 的操作，如 `parse`）。

被装饰函数应返回 `dict[str, Atom]`（键为正则模式）。

## `register_tokens(*args, **kwargs)`

装饰器：注册 **token** 构造器映射；`pass_metta` 同上。

## `grounded(arg)`

两种用法：

1. `@grounded`：在扩展模块中延迟注册；由模块加载扫描 `metta_type` 属性时，用函数名作为 **token**，`unwrap=True` 创建 `OperationAtom`。
2. `@grounded(metta)`：立即向给定 `MeTTa` 实例 `register_atom`。

与 `register_atoms` 的区别：`grounded` 直接把 **Python 函数** 包装为操作；`register_atoms` 由函数**返回**多个 **regex → Atom** 条目。

## `mark_register_function`

内部用于实现上述装饰器；扩展一般不需要直接使用。

## 最小扩展示例

```python
from hyperon.ext import register_atoms
from hyperon.atoms import OperationAtom, ValueAtom

@register_atoms
def my_ops():
    return {
        r"hello": OperationAtom("hello", lambda: [ValueAtom("ok", "String")]),
    }
```

将模块置于可导入路径并在 **MeTTa** 模块系统中加载后，`hello` **token** 即可用。
