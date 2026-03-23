---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `lib/tests/metta.rs` 分析报告

## 文件角色

MeTTa 运行时与 grounded 算子集成测试：高阶/柯里化、`GroundedFunctionAtom` 三种构造方式，以及通过内嵌 `.metta` 文件跑标准库。

## 关键 API / 测试覆盖

- `test_reduce_higher_order`：`assertEqualToResult`、`UNIT_ATOM`
- `GroundedFunctionAtom::new` + 闭包 / 函数 / `impl GroundedFunction`
- `run_metta_test!` + `include_bytes!("test_stdlib.metta")`；错误形态扫描 `ERROR_SYMBOL`

## 小结

兼顾语言层（高阶与断言）与宿主扩展（grounded 可执行原子），并用宏批量执行外部 MeTTa 脚本做回归。
