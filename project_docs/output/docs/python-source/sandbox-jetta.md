---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
---

# compile.py（Jetta 沙箱）

## 文件角色

**Jetta**（Kotlin MeTTa 编译器）HTTP 客户端：`requests` 调用本地 server，提供 `jetta`、`new-jetta-space`、`compile` 等 MeTTa 操作，把空间中函数的类型/规则发到 Jetta 并注册 **grounded 包装** 以远程求值。

## 关键特性与集成

- **jetta / jetta_unwrap_atom**：POST 代码、JSON 结果、错误转为 `Error ... JettaCompileError` 表达式。
- **compile(metta, ...)**：从空间查询 `@` 注解、`: type`、`= 规则`，拼 MeTTa 源码调用 Jetta，再 `register_atom(func+'-gnd', ...)`。
- **register_atoms(pass_metta=True)**：`jettaspace_atoms`。

## 摘要

跨语言编译/执行链路的早期封装；注释标明需克隆 Jetta 并跑 server；多处 TODO/断言限制（单规则、类型非确定性等）。实验性质强。
