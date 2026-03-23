---
source_version: "0.2.10"
last_updated: "2026-03-23"
---

# 贡献指南

## 流程

1. **Fork** 仓库并从最新 `main` 创建功能分支。
2. 小而递增的提交；尽量保持每个提交可通过测试。
3. **Pull Request** 需包含：与上游同步、通过 **CI**、经维护者 **Review**。
4. 提交信息：首行 ≤50 字符摘要，空行后可选正文（行宽建议 ≤73）。避免泛泛的 `Update foo.md`。
5. 不在首行写 `Fixes #123`；在 **PR** 描述中关联 **issue**。

## 代码风格

- 贴近现有代码；新增库依赖请**固定版本**（勿用宽松范围）。
- **Rust**：缩小 `unsafe` 块；**C** API 通常不对外标记为 `unsafe`。
- 注释：`FIXME`（合并前应处理）与 `TODO`（可后续 **PR**）区分使用。

## 测试

- **Rust**：`cargo test`
- **Python**：`pytest`（见 `../testing/python-tests.md`）
- **MeTTa** 脚本：`python/tests/scripts`（见 `../testing/metta-tests.md`）

## **Git** 与 **Docker**

根目录 `.gitignore` 亦用于 **Docker** 构建上下文；新增忽略项请放在仓库根 `.gitignore`。

## 获取帮助

可开 **draft PR** 讨论实现方向；复杂设计问题优先开 **issue**。

## 权威原文

本页为中文摘要；完整英文流程见仓库 `docs/CONTRIBUTING.md`。
