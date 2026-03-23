---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# SQL Space 实验

## 位置

`python/sandbox/sql_space/sql_space.py` 与 `python/sandbox/sql_space/sql_space_test.metta`。

## 思路

用 **SQL** 后端实现或代理 **Space** 的 `query` / `add`，使 **MeTTa** `match` 落在关系数据上。

## 状态

原型级；性能、事务语义与 **Bindings** 映射仍需定义。

## 运行

需配置 **DB** 驱动与连接串（见具体测试文件中的跳过条件 `pytest.mark.skip`）。

## 参见

`../extension-dev/custom-space.md`
