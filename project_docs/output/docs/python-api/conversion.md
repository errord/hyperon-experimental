---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 模块 `hyperon.conversion` — 公共 API

在 **Python** 与其它运行时之间桥接基础值。

## `ConvertingSerializer(Serializer)`

用于接收 **Rust** 侧通过 **serialize** 回调传来的标量。

### 构造

- `__init__()`：初始化 `self.value = None`。

### 方法（返回 `SerialResult.OK`）

| 方法 | 设置 `self.value` 类型 |
|------|-------------------------|
| `serialize_bool(v)` | `bool` |
| `serialize_int(v)` | `int` |
| `serialize_float(v)` | `float` |
| `serialize_str(v)` | `str` |

### 使用场景

`GroundedAtom.get_object()` 在 **Grounded** 类型为 **Bool** / **Number** / **String** 时，内部创建 `ConvertingSerializer` 并调用 `hp.atom_gnd_serialize`，将值填入 `converter.value` 再包进 `ValueObject`。

扩展自定义 **Grounded** 时，若需从 **Rust** 读回 Python 标量，可实现对称的 **Serializer** 协议（见 **hyperonpy** `Serializer` / `SerialResult`）。
