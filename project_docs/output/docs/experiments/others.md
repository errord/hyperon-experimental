---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 其它实验目录

`python/sandbox/` 下各子目录涵盖多种集成原型，包括但不限于：

| 区域 | 示例路径 | 说明 |
|------|-----------|------|
| **REPL** / 解析 | `sandbox/repl/metta_repl.py`, `sandbox/pytorch/parsing_exceptions.py` | **REPL** 与解析试验 |
| **Resolve** | `sandbox/resolve/resolve.py`, `sandbox/resolve/r.py` | 模块解析实验 |
| **Jetta** | `sandbox/jetta/compile.py` 与 `*.metta` | 编译/λ/非确定性 |
| **MORK** | `sandbox/mork/mork.py` | 外部表示与序列化 |
| **行为 / 绑定** | `sandbox/bhv_binding/bhv_binding.py` | 行为组合示例 |
| **SingularityNET** | `hyperon/exts/snet_io/`（扩展包内） | 服务调用 **IO** |

## 使用建议

1. 阅读文件头注释与 `pytest` 标记（`skip`、`xfail`）。
2. 不要把 **sandbox** 当作稳定 **API** 教程；生产集成以正式扩展文档为准。
3. 新实验请放在 `python/sandbox/<主题>/` 子目录下，避免与 `python/tests/` 核心回归混淆。

## 清理与晋升

成熟原型可提炼为 `hyperon/exts` 包或独立 **PyPI** 项目，并补充 `../extension-dev/module-packaging.md` 所述打包说明。
