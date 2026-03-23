# Hyperon 项目文档生成提示词集

> **项目**：OpenCog Hyperon (hyperon-experimental)
> **版本**：0.2.10
> **项目根目录**：`d:\dev\hyperon-experimental`
> **提示词目录**：`project_docs/prompt/`
> **文档输出目录**：`project_docs/output/`

---

## 提示词文件清单

| 编号 | 文件名 | 用途 | 适用对象 |
|------|--------|------|---------|
| 00 | `00_main_generation_prompt.md` | **主文档生成提示词** —— 全局文档结构、理论背景、架构设计、语言语义/语法完整清单 | 整个项目 |
| 01 | `01_single_file_rust.md` | **Rust 单文件分析提示词** —— 所有权/trait/解释器/FFI 深度分析模板 | `*.rs` 文件（约 85 个） |
| 02 | `02_single_file_python.md` | **Python 单文件分析提示词** —— hyperonpy 调用映射/回调/装饰器分析模板 | `*.py` 文件（约 67 个） |
| 03 | `03_single_file_metta.md` | **MeTTa 单文件分析提示词** —— 原子分类/求值链/推理模式/知识图谱分析模板 | `*.metta` 文件（约 67 个） |
| -- | `SOURCE_FILE_TODOLIST.md` | **源码文件分析进度跟踪** —— 219 个文件的 checkbox 清单，支持断点续做 | 全部源文件 |

## 使用方法

### 全局文档生成
使用 `00_main_generation_prompt.md` 驱动整个项目的文档生成，产出物存放在 `project_docs/output/` 下。

### 单文件分析
根据目标文件的扩展名选择对应的提示词模板，替换 `{{占位符}}` 后执行：

```bash
# 分析 Rust 文件
模板：01_single_file_rust.md
替换：{{TARGET_FILE_REL}} = lib/src/metta/interpreter.rs

# 分析 Python 文件
模板：02_single_file_python.md
替换：{{TARGET_FILE_REL}} = python/hyperon/atoms.py

# 分析 MeTTa 文件
模板：03_single_file_metta.md
替换：{{TARGET_FILE_REL}} = python/tests/scripts/b2_backchain.metta
```

## 路径约定

| 变量 | 说明 | 值 |
|------|------|-----|
| `{{SOURCE_ROOT}}` | 项目仓库根目录 | `d:\dev\hyperon-experimental` |
| `{{TARGET_FILE_REL}}` | 目标文件相对于仓库根的路径 | 如 `lib/src/metta/interpreter.rs` |
| `{{TARGET_FILE_ABS}}` | 目标文件绝对路径 | 如 `d:\dev\hyperon-experimental\lib\src\metta\interpreter.rs` |
| 提示词目录 | 本目录 | `project_docs/prompt/` |
| 文档输出目录 | 生成的文档存放处 | `project_docs/output/` |
