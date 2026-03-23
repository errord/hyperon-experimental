---
source_version: "0.2.10"
source_commit: "cf4c5375"
last_updated: "2026-03-23"
source_path: "python/sandbox/jetta/enum_lambda.metta"
---

# sandbox：jetta 枚举 λ

**角色**：非确定性 `bin` 与 Jetta 中 `calc_err` 搜索零误差函数。  
**要点**：`jetta`、`bin`、`num`/`S`/`Z`、`rnd-square`、`calc_err`。  
**概要**：用多子句 `(= (bin) 0/1)` 枚举；`rnd-square` 为随机二次参数化；若 `(calc_err $f)` 在 jetta 中为 0 则保留该 `$f`，否则 `Empty`。
