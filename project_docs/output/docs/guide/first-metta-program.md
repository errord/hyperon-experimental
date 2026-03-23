---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 第一个 MeTTa 程序

## 在 REPL 中

启动 `metta-py`，输入 **S-expression**：

```metta
(+ 1 2)
```

应得到 `3` 或包含 **Number** 的结果列表（取决于打印格式）。

再试规则定义：

```metta
(= (double $x) (* 2 $x))
(double 21)
```

## 在 Python 中

```python
from hyperon.runner import MeTTa

metta = MeTTa()
results = metta.run("""
    (= (hello) "Hi")
    (hello)
""")
print(results)
```

`run` 返回嵌套列表：外层为并行结果集，内层为 **Atom** 序列。

## 使用模块与空间

```metta
!(import! &self my-module)
```

具体 `import!` 路径依赖 **include** 目录；内置示例见仓库 `python/tests/scripts`。

## 下一步

- 教程：`../metta-lang/tutorial/`（若已生成）
- 非确定性：`../metta-lang/nondeterminism.md`
- **Python** 细节：`python-quickstart.md`
