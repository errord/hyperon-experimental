---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "integration_tests/das/animals.metta"
---

# other：animals.metta（DAS）

## 文件角色

**DAS 集成测试**用的静态本体：概念、谓词与 `EVALUATION` 事实（动物/植物等分类）。

## 关键原子/函数

- 类型：`Concept`、`Predicate`、`EVALUATION`、`PREDICATE`、`CONCEPT`
- 概念：`human`、`monkey`、`triceratops`、`vine` 等
- 谓词：`is_animal`、`is_mammal`、`is_dinosaur`、`no_legs` 等

## 概要

声明类型与大量 `(EVALUATION (PREDICATE …) (CONCEPT …))` 三元组，供远程 DAS 上的 `match` 查询（见 `test.metta`）。无 `import`，纯数据。
