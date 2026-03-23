---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "mkdocs.metta"
---

# other：mkdocs.metta

## 文件角色

从模块空间的 `@doc-formal` **生成 Markdown 帮助**并写入 `docs/generated/*.md` 的脚本化管线（配合 MkDocs）。

## 关键原子/函数

- `concat-help`、`help-md!`、`help-param-md!`、`help-md-space!`
- `document-module`、`import! &self fileio`
- `file-open!`、`file-write!`、`module-space-no-deps`、`mod-space!`
- `collapse`、`sort-strings`、`foldl-atom`

## 概要

解析函数/原子文档结构，格式化为带 Type/Parameters/Returns 的 Markdown；`document-module` 对 `corelib`、`random`、`fileio`、`json`、`catalog`、`das` 等执行导入、收集帮助、排序拼接并写文件。
