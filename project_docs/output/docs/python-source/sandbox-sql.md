---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# sql_space.py（沙箱）

## 文件角色

**PostgreSQL 接地空间**：`SqlSpace` 继承 `GroundingSpace`，把 MeTTa 查询原子解析为 `SELECT`/`INSERT`，通过 **psycopg2** 执行，结果转为 `BindingsSet`。

## 关键特性与集成

- **SqlHelper**：从嵌套表达式解析表、字段、条件、`LIMIT`；`save_query-result` 把查询结果实例化回普通 `GroundingSpace`；`sql.insert` 拼 `INSERT ... RETURNING`。
- **register_atoms**：`new-sql-space`、`sql.save-query-result`、`sql.insert`。
- **依赖**：`hyperon`、`psycopg2`。

## 摘要

用表达式结构约定表达 SQL 意图的实验后端；错误处理以打印或空 bindings 为主，生产需谨慎。典型沙箱原型。
