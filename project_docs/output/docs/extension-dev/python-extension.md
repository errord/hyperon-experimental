---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 编写 Python 扩展

## 目标

在 **MeTTa** 程序中使用自定义 **token**、**Grounded** 操作或桥接 **Python** 对象，而无需修改 **Rust** 核心。

## 两种注册路径

### 1. `register_atoms` / `register_tokens`

在模块顶层定义被装饰函数；函数名任意，但必须带有 `metta_type`（由装饰器注入）。

- **`register_atoms`**：返回 `{正则: Atom}`，**Atom** 常为 `OperationAtom(name, fn, type_names=[...], unwrap=True|False)`。
- **`register_tokens`**：返回 `{正则: lambda s: Atom}`，用于字面量。

`pass_metta=True` 时，函数接收 `MeTTa` 实例（需要 `parse` 等依赖 **Tokenizer** 的场景）。

### 2. `@grounded` / `@grounded(metta)`

把单个 **Python** 函数直接注册为同名操作；`unwrap=True` 时参数从 **GroundedAtom** 自动解包。

## 模块如何被加载

- **显式**：`MeTTa.load_module_direct_from_pymod("logical-name", "python.module.path")`。
- **文件系统**：`.py` 或含 `__init__.py` 的包出现在 **include path** 上，由 `_PyFileMeTTaModFmt` 加载；加载后会扫描模块 `dir()` 中带 `metta_type` 的函数并注册。

内置扩展目录：`hyperon/exts`（随包安装）。

## 操作实现要点

- **`unwrap=True`**：参数必须是可解包的 **Grounded**；否则抛 `NoReduceError`，行为类似“规则不匹配”。
- **`unwrap=False`**：接收 **Atom**，返回值**必须**为 **list**（多结果列表）。
- 用 `MettaError` 报告可恢复错误，可映射为 **MeTTa** `Error` 表达式。
- **`get_object()`**：在 **Space** **query** 回调中避免未捕获异常。

## 测试

将扩展与 `pytest` 用例放在 `python/tests` 模式旁；用 `MeTTa(Environment.test_env())` 隔离环境（若需要）。

## 参见

- `grounded-ops.md`、`module-packaging.md`
- `../python-api/ext.md`、`../python-api/atoms.md`
