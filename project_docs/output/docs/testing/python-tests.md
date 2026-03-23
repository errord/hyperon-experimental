---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# Python 测试说明

## 运行

在激活虚拟环境并 `pip install -e ./python` 后：

```bash
cd python
pytest
```

筛选单个文件：

```bash
pytest tests/test_metta.py -v
```

## 布局

- `tests/test_*.py`：按功能域划分（**atom**、**bindings**、**stdlib**、**module** 等）。
- `tests/scripts/`：**MeTTa** 源片段，由测试用 `MeTTa.run` 或文件路径加载。
- `tests/ext_*`：扩展加载与路径解析场景。

## 编写建议

1. 优先用 `MeTTa(Environment.test_env())` 避免污染用户配置。
2. 断言 `metta.run(..., flat=True)` 时注意结果列表形状。
3. 涉及 **Grounded** **Python** 回调的测试，避免在 **match** 中抛出未捕获异常。

## 与 **Rust** 测试的边界

纯 **Rust** 逻辑应在 `cargo test` 中覆盖；**Python** 测试验证 **FFI**、对象生命周期与 **API** 契约。

## 调试

`pytest -s` 保留打印；`RunnerState` 单步测试可复现解释器中间状态。
