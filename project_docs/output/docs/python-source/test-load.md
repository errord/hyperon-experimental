---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# test_load.py 分析报告

## 文件角色

**load-ascii**：将 MeTTa 源文件按行读入新空间并与磁盘内容解析结果一致。

## 测试覆盖摘要

- `setUp` 将 cwd 设为测试文件父目录。
- `new-space` + `load-ascii &space test_load.metta`，再 `match &space $x $x` 得到空间中所有原子。
- 与 `open(test_file).read()` 经 `parse_all` 的结果做**无序**相等。

## 关键断言/特性

- `assertEqualNoOrder` 保证加载顺序与解析列表顺序无关。

## 小结

单用例、聚焦文件 IO 与空间填充的一致性。
