---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 自定义 Space 实现

## 接口

继承 `hyperon.base.AbstractSpace` 并实现：

| 方法 | 说明 |
|------|------|
| `query(query_atom)` | 对模式求查询，返回 `BindingsSet`。 |
| `add(atom)` | 添加 **Atom**。 |
| `remove(atom)` | 删除；返回值若存在应符合 **C** 层约定。 |
| `replace(atom, replacement)` | 原地替换。 |

可选：`atom_count()`、`atoms_iter()`（供枚举与统计）；未实现时 **hyperonpy** 可能返回哨兵值。

## 接入 Runner

```python
from hyperon.base import SpaceRef, AbstractSpace
from hyperon.runner import MeTTa
from hyperon.atoms import BindingsSet

class MySpace(AbstractSpace):
    def __init__(self):
        super().__init__()
        self._atoms = []

    def add(self, atom):
        self._atoms.append(atom)

    def remove(self, atom):
        self._atoms.remove(atom)

    def replace(self, atom, replacement):
        i = self._atoms.index(atom)
        self._atoms[i] = replacement

    def query(self, query_atom):
        # 最小实现：可委托给 GroundingSpace 或自写匹配
        return BindingsSet.empty()

metta = MeTTa(space=SpaceRef(MySpace()))
```

将自定义 **Space** 交给 `SpaceRef(my_space)`，再传入 `MeTTa(..., space=...)`。**C** 侧通过 `space_new_custom` 把回调派发到 **Python** 的 `AbstractSpace` 实现。

## 语义注意

- **query** 应返回**所有**匹配绑定的并集（`BindingsSet` 多帧）。
- **Grounded** **Space** **Atom** 使用 `atom_space` / `G(space_ref)` 包装。

## 调试

先用小 **GroundingSpace** 对照行为，再替换为自定义实现；使用 `metta.run` 与 `space.query` 单测。

## 参见

- `../python-api/base.md`
- **Rust** `hyperon-space` crate（原生 **Space** **trait**）
