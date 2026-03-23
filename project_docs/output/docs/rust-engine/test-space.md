---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# `lib/tests/space.rs` 分析报告

## 文件角色

单测：在 `GroundingSpace` 中嵌入 `DynSpace`（作为 grounded 子空间），验证跨空间联合查询与变量绑定。

## 关键 API / 测试覆盖

- `GroundingSpace::new`、`DynSpace::new`、`add`、`query`
- 模式：`expr!("," ...)` 与 `VariableAtom::resolve`

## 小结

一条测试即可说明「空间作为原子」时，主空间查询能穿透子空间中的蕴含事实并得到唯一绑定。
