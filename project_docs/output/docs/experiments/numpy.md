---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# NumPy 实验（sandbox）

## 位置

`python/sandbox/numpy/numme.py` 与 `python/sandbox/numpy/nm_test.metta` 等。

## 内容概要

将 **ndarray** 或标量 **numpy** 类型暴露为 **GroundedAtom**，试验向量运算、与 **MeTTa** 规则结合的数值脚本。

## 依赖

```bash
pip install numpy
```

## 注意

**numpy** 标量与 **Python** `float`/`int` 在 **Grounded** 桥接中行为可能不同；编写操作时需明确 `unwrap` 与 `ValueAtom` 类型标注。

## 参见

`pytorch.md`、`../python-api/atoms.md`
