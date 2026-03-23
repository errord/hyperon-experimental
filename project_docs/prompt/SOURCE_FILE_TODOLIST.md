# 源码文件分析进度跟踪清单

> **项目**：OpenCog Hyperon (hyperon-experimental)
> **基线 Git Commit**：`74edbddf0c35ed7b50edc5a29e13ebeca651943e`（`74edbddf`）
> **基线日期**：2026-03-20
> **生成日期**：2026-03-23
> **文件总数**：219（`.rs` 85 + `.py` 67 + `.metta` 67）
> **关联提示词**：
> - 主提示词：[00_main_generation_prompt.md](./00_main_generation_prompt.md)
> - Rust 分析：[01_single_file_rust.md](./01_single_file_rust.md)
> - Python 分析：[02_single_file_python.md](./02_single_file_python.md)
> - MeTTa 分析：[03_single_file_metta.md](./03_single_file_metta.md)

---

## 使用说明

### 进度标记规则
- `[ ]` — 未开始
- `[~]` — 进行中（已开始分析但未完成报告）
- `[x]` — 已完成（分析报告已输出到 `project_docs/output/docs/` 对应位置）
- `[-]` — 跳过（文件不需要独立分析，如纯 re-export、空 `__init__.py` 等，需注明原因）

### 断点续做机制
1. 每次启动分析任务时，先读取本文件，找到第一个 `[ ]` 标记的文件开始工作
2. 完成一个文件的分析后，立即将其标记从 `[ ]` 改为 `[x]`，并记录完成时间
3. 如果任务中断，下次恢复时只需搜索第一个 `[ ]` 即可继续
4. 所有 `[~]` 标记的文件需要重新审查，确保报告完整

### 完成率统计
在每个分类末尾有计数行，格式为：`完成/总数`，每次更新标记时同步更新。

### Git 一致性检查
开始分析前，运行 `git log -1 --format="%H"` 确认当前 commit 与基线一致。
若代码已更新，需在本文件顶部记录新的 commit hash，并对已分析文件评估是否需要重新分析。

---

## 一、Rust 源文件（85 个）

### 1.1 hyperon-common（基础数据结构库，12 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R01 | [ ] | `hyperon-common/src/lib.rs` | CachingMapper，crate 入口 | |
| R02 | [ ] | `hyperon-common/src/collections.rs` | Equality trait，ListMap，VecDisplay | |
| R03 | [ ] | `hyperon-common/src/unique_string.rs` | UniqueString 字符串驻留 | |
| R04 | [ ] | `hyperon-common/src/immutable_string.rs` | ImmutableString 不可变字符串 | |
| R05 | [ ] | `hyperon-common/src/flex_ref.rs` | FlexRef 统一借用 | |
| R06 | [ ] | `hyperon-common/src/reformove.rs` | RefOrMove 参数类型 | |
| R07 | [ ] | `hyperon-common/src/holeyvec.rs` | HoleyVec 稀疏向量 | |
| R08 | [ ] | `hyperon-common/src/shared.rs` | LockBorrow 统一借用接口 | |
| R09 | [ ] | `hyperon-common/src/multitrie.rs` | MultiTrie 多值Trie树 | |
| R10 | [ ] | `hyperon-common/src/owned_or_borrowed.rs` | OwnedOrBorrowed 枚举 | |
| R11 | [ ] | `hyperon-common/src/vecondemand.rs` | VecOnDemand 延迟向量 | |
| R12 | [ ] | `hyperon-common/src/assert.rs` | 测试辅助：无序向量比较 | |

> **hyperon-common 进度：0/12**

### 1.2 hyperon-atom（原子类型与模式匹配，10 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R13 | [ ] | `hyperon-atom/src/lib.rs` | **Atom ADT 核心定义**，Grounded trait 体系 | |
| R14 | [ ] | `hyperon-atom/src/matcher.rs` | **模式匹配/合一引擎**，Bindings/BindingsSet | |
| R15 | [ ] | `hyperon-atom/src/iter.rs` | Atom 深度优先迭代器 | |
| R16 | [ ] | `hyperon-atom/src/subexpr.rs` | 子表达式遍历，WalkStrategy | |
| R17 | [ ] | `hyperon-atom/src/serial.rs` | Serializer trait，ConvertingSerializer | |
| R18 | [ ] | `hyperon-atom/src/gnd/mod.rs` | GroundedFunction 包装 | |
| R19 | [ ] | `hyperon-atom/src/gnd/number.rs` | Number 类型（Integer/Float） | |
| R20 | [ ] | `hyperon-atom/src/gnd/str.rs` | Str 字符串类型 | |
| R21 | [ ] | `hyperon-atom/src/gnd/bool.rs` | Bool 类型 | |
| R22 | [ ] | `hyperon-atom/tests/macros.rs` | 宏测试 | |

> **hyperon-atom 进度：0/10**

### 1.3 hyperon-space（空间抽象与索引，5 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R23 | [ ] | `hyperon-space/src/lib.rs` | **Space/SpaceMut/DynSpace trait**，观察者 | |
| R24 | [ ] | `hyperon-space/src/index/mod.rs` | AtomIndex Trie 索引 | |
| R25 | [ ] | `hyperon-space/src/index/trie.rs` | AtomTrie 内部 Trie 节点 | |
| R26 | [ ] | `hyperon-space/src/index/storage.rs` | AtomStorage bimap 存储 | |
| R27 | [ ] | `hyperon-space/benches/atom_index.rs` | AtomIndex 基准测试 | |

> **hyperon-space 进度：0/5**

### 1.4 hyperon-macros（过程宏，1 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R28 | [ ] | `hyperon-macros/src/lib.rs` | metta!/metta_const! 过程宏 | |

> **hyperon-macros 进度：0/1**

### 1.5 hyperon lib — MeTTa 核心（34 个文件）

#### 1.5.1 顶层与空间实现

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R29 | [ ] | `lib/src/lib.rs` | crate 入口，re-export | |
| R30 | [ ] | `lib/src/space/mod.rs` | space 模块入口 | |
| R31 | [ ] | `lib/src/space/grounding/mod.rs` | **GroundingSpace** 内存空间实现 | |
| R32 | [ ] | `lib/src/space/module.rs` | **ModuleSpace** 复合空间 | |

#### 1.5.2 MeTTa 解释器核心

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R33 | [ ] | `lib/src/metta/mod.rs` | MeTTa 常量定义（符号/类型/错误） | |
| R34 | [ ] | `lib/src/metta/interpreter.rs` | **解释器归约引擎**（~2170行，最核心） | |
| R35 | [ ] | `lib/src/metta/types.rs` | **类型系统**（运行时类型检查） | |
| R36 | [ ] | `lib/src/metta/text.rs` | **S-表达式解析器**（Tokenizer+SExprParser） | |

#### 1.5.3 Runner 系统

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R37 | [ ] | `lib/src/metta/runner/mod.rs` | **Metta Runner** 核心（~1470行） | |
| R38 | [ ] | `lib/src/metta/runner/environment.rs` | Environment 环境配置 | |

#### 1.5.4 模块系统

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R39 | [ ] | `lib/src/metta/runner/modules/mod.rs` | MettaMod，ModuleLoader trait | |
| R40 | [ ] | `lib/src/metta/runner/modules/mod_names.rs` | 模块名树 ModNameNode | |

#### 1.5.5 标准库 Rust 实现

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R41 | [ ] | `lib/src/metta/runner/stdlib/mod.rs` | stdlib 入口，interpret 辅助，token 注册 | |
| R42 | [ ] | `lib/src/metta/runner/stdlib/core.rs` | 核心操作（pragma/match/sealed/equal/...） | |
| R43 | [ ] | `lib/src/metta/runner/stdlib/atom.rs` | 原子操作（get-type/unique/union/...） | |
| R44 | [ ] | `lib/src/metta/runner/stdlib/arithmetics.rs` | 算术运算（+/-/*/比较/布尔） | |
| R45 | [ ] | `lib/src/metta/runner/stdlib/math.rs` | 数学函数（三角/对数/幂/取整） | |
| R46 | [ ] | `lib/src/metta/runner/stdlib/space.rs` | 空间/状态操作（new-space/StateAtom/...） | |
| R47 | [ ] | `lib/src/metta/runner/stdlib/string.rs` | 字符串操作（println!/format-args/...） | |
| R48 | [ ] | `lib/src/metta/runner/stdlib/debug.rs` | 调试/测试（trace!/assertEqual/...） | |
| R49 | [ ] | `lib/src/metta/runner/stdlib/module.rs` | 模块操作（import!） | |
| R50 | [ ] | `lib/src/metta/runner/stdlib/package.rs` | 包管理操作（register-module!/git-module!） | |

#### 1.5.6 内置模块

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R51 | [ ] | `lib/src/metta/runner/builtin_mods/mod.rs` | 内置模块入口 | |
| R52 | [ ] | `lib/src/metta/runner/builtin_mods/random.rs` | random 模块 | |
| R53 | [ ] | `lib/src/metta/runner/builtin_mods/fileio.rs` | fileio 模块 | |
| R54 | [ ] | `lib/src/metta/runner/builtin_mods/json.rs` | json 模块 | |
| R55 | [ ] | `lib/src/metta/runner/builtin_mods/catalog.rs` | catalog 模块 | |
| R56 | [ ] | `lib/src/metta/runner/builtin_mods/das.rs` | das 分布式原子空间模块 | |
| R57 | [ ] | `lib/src/metta/runner/builtin_mods/skel.rs` | skel 骨架模板 | |

#### 1.5.7 包管理

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R58 | [ ] | `lib/src/metta/runner/pkg_mgmt/mod.rs` | 包管理入口 | |
| R59 | [ ] | `lib/src/metta/runner/pkg_mgmt/catalog.rs` | DirCatalog/LocalCatalog | |
| R60 | [ ] | `lib/src/metta/runner/pkg_mgmt/managed_catalog.rs` | ManagedCatalog | |
| R61 | [ ] | `lib/src/metta/runner/pkg_mgmt/git_cache.rs` | CachedRepo Git 缓存 | |
| R62 | [ ] | `lib/src/metta/runner/pkg_mgmt/git_catalog.rs` | GitCatalog | |

#### 1.5.8 测试与基准

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R63 | [ ] | `lib/tests/case.rs` | case 集成测试 | |
| R64 | [ ] | `lib/tests/metta.rs` | metta 集成测试 | |
| R65 | [ ] | `lib/tests/space.rs` | space 集成测试 | |
| R66 | [ ] | `lib/tests/types.rs` | types 集成测试 | |
| R67 | [ ] | `lib/tests/macros.rs` | macros 集成测试 | |
| R68 | [ ] | `lib/benches/grounding_space.rs` | GroundingSpace 基准测试 | |
| R69 | [ ] | `lib/benches/interpreter_minimal.rs` | 解释器基准测试 | |
| R70 | [ ] | `lib/benches/states.rs` | 状态基准测试 | |
| R71 | [ ] | `lib/benches/type.rs` | 类型基准测试 | |

#### 1.5.9 示例

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R72 | [ ] | `lib/examples/custom_match.rs` | 自定义匹配示例 | |
| R73 | [ ] | `lib/examples/sorted_list.rs` | 排序列表示例 | |
| R74 | [ ] | `lib/examples/load_space.rs` | 空间加载示例 | |

> **hyperon lib 进度：0/46**

### 1.6 hyperonc（C API 绑定层，7 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R75 | [ ] | `c/src/lib.rs` | C API crate 入口 | |
| R76 | [ ] | `c/src/atom.rs` | 原子 C API（atom_*/bindings_*） | |
| R77 | [ ] | `c/src/space.rs` | 空间 C API（space_*） | |
| R78 | [ ] | `c/src/metta.rs` | Runner C API（metta_*/tokenizer_*） | |
| R79 | [ ] | `c/src/serial.rs` | 序列化 C API | |
| R80 | [ ] | `c/src/module.rs` | 模块 C API（module_loader_*） | |
| R81 | [ ] | `c/src/util.rs` | FFI 工具函数 | |

> **hyperonc 进度：0/7**

### 1.7 metta-repl（REPL，4 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| R82 | [ ] | `repl/src/main.rs` | CLI 入口，clap 参数解析 | |
| R83 | [ ] | `repl/src/metta_shim.rs` | MettaShim 双模式（Rust/Python） | |
| R84 | [ ] | `repl/src/config_params.rs` | REPL 配置参数 | |
| R85 | [ ] | `repl/src/interactive_helper.rs` | rustyline 补全/高亮 | |

> **metta-repl 进度：0/4**

### ✅ Rust 总进度：0/85

---

## 二、Python 源文件（67 个）

### 2.1 hyperon 核心包（10 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| P01 | [ ] | `python/hyperon/__init__.py` | 包入口，公共导出 | |
| P02 | [ ] | `python/hyperon/atoms.py` | **Atom 类型体系**核心 | |
| P03 | [ ] | `python/hyperon/base.py` | **Space/Parser/Tokenizer** 抽象 | |
| P04 | [ ] | `python/hyperon/runner.py` | **MeTTa/RunnerState/Environment** | |
| P05 | [ ] | `python/hyperon/ext.py` | **扩展装饰器**（register_atoms/tokens/grounded） | |
| P06 | [ ] | `python/hyperon/stdlib.py` | **Python 端标准库** | |
| P07 | [ ] | `python/hyperon/conversion.py` | ConvertingSerializer 类型转换 | |
| P08 | [ ] | `python/hyperon/module.py` | MettaModRef 模块引用 | |
| P09 | [ ] | `python/hyperon/metta.py` | CLI 入口 metta-py | |
| P10 | [ ] | `python/setup.py` | setuptools 构建配置 | |

> **hyperon 核心包进度：0/10**

### 2.2 扩展模块 — py_ops（2 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| P11 | [ ] | `python/hyperon/exts/py_ops/__init__.py` | py_ops 包入口 | |
| P12 | [ ] | `python/hyperon/exts/py_ops/pyop.py` | 算术/类型运算 | |

> **py_ops 进度：0/2**

### 2.3 扩展模块 — agents（6 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| P13 | [ ] | `python/hyperon/exts/agents/__init__.py` | agents 包入口 | |
| P14 | [ ] | `python/hyperon/exts/agents/agent_base.py` | Agent 基类 | |
| P15 | [ ] | `python/hyperon/exts/agents/events/__init__.py` | events 子包入口 | |
| P16 | [ ] | `python/hyperon/exts/agents/events/basic_bus.py` | 事件总线 | |
| P17 | [ ] | `python/hyperon/exts/agents/tests/test_1_python_agents.py` | agents 测试 | |
| P18 | [ ] | `python/hyperon/exts/agents/tests/test_2_daemon.py` | daemon 测试 | |
| P19 | [ ] | `python/hyperon/exts/agents/tests/test_3_events_python.py` | events 测试 | |

> **agents 进度：0/7**

### 2.4 扩展模块 — snet_io（3 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| P20 | [ ] | `python/hyperon/exts/snet_io/__init__.py` | snet_io 包入口 | |
| P21 | [ ] | `python/hyperon/exts/snet_io/snet_gate.py` | SingularityNET 服务网关 | |

> **snet_io 进度：0/2**

### 2.5 测试文件（20 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| P22 | [ ] | `python/tests/test_atom.py` | Atom 类型测试 | |
| P23 | [ ] | `python/tests/test_atom_type.py` | Atom 类型系统测试 | |
| P24 | [ ] | `python/tests/test_bindings.py` | Bindings 测试 | |
| P25 | [ ] | `python/tests/test_common.py` | 通用功能测试 | |
| P26 | [ ] | `python/tests/test_custom_space.py` | 自定义 Space 测试 | |
| P27 | [ ] | `python/tests/test_environment.py` | Environment 测试 | |
| P28 | [ ] | `python/tests/test_examples.py` | 示例脚本测试 | |
| P29 | [ ] | `python/tests/test_extend.py` | 扩展机制测试 | |
| P30 | [ ] | `python/tests/test_grounded_type.py` | Grounded 类型测试 | |
| P31 | [ ] | `python/tests/test_grounding_space.py` | GroundingSpace 测试 | |
| P32 | [ ] | `python/tests/test_load.py` | 加载测试 | |
| P33 | [ ] | `python/tests/test_metta.py` | MeTTa 综合测试 | |
| P34 | [ ] | `python/tests/test_modules.py` | 模块系统测试 | |
| P35 | [ ] | `python/tests/test_pln_tv.py` | PLN 真值测试 | |
| P36 | [ ] | `python/tests/test_run_metta.py` | run_metta 测试 | |
| P37 | [ ] | `python/tests/test_sexparser.py` | S-表达式解析器测试 | |
| P38 | [ ] | `python/tests/test_stdlib.py` | 标准库测试 | |
| P39 | [ ] | `python/tests/extension.py` | 扩展辅助 | |
| P40 | [ ] | `python/tests/pyfile_test_mod.py` | Python 模块加载测试辅助 | |
| P41 | [ ] | `python/tests/error_pyext.py` | 错误扩展测试辅助 | |

> **测试文件进度：0/20**

### 2.6 测试扩展目录（4 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| P42 | [ ] | `python/tests/ext_dir/__init__.py` | ext_dir 测试入口 | |
| P43 | [ ] | `python/tests/ext_dir/ext.py` | ext_dir 扩展注册 | |
| P44 | [ ] | `python/tests/ext_sub/ext_nested/__init__.py` | ext_sub 嵌套入口 | |
| P45 | [ ] | `python/tests/ext_sub/ext_nested/ext.py` | ext_sub 嵌套扩展 | |
| P46 | [ ] | `python/tests/ext_recursive/level-2/ext_nested/__init__.py` | 递归嵌套入口 | |
| P47 | [ ] | `python/tests/ext_recursive/level-2/ext_nested/ext.py` | 递归嵌套扩展 | |

> **测试扩展目录进度：0/6**

### 2.7 沙箱实验（14 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| P48 | [ ] | `python/sandbox/pytorch/torchme.py` | PyTorch 集成 | |
| P49 | [ ] | `python/sandbox/pytorch/kwargsme.py` | Kwargs 处理实验 | |
| P50 | [ ] | `python/sandbox/pytorch/tm_test.py` | PyTorch 测试 | |
| P51 | [ ] | `python/sandbox/pytorch/parsing_exceptions.py` | 解析异常实验 | |
| P52 | [ ] | `python/sandbox/pytorch/parse_torch_func_signatures.py` | Torch 签名解析 | |
| P53 | [ ] | `python/sandbox/numpy/numme.py` | NumPy 集成 | |
| P54 | [ ] | `python/sandbox/sql_space/sql_space.py` | SQL 空间实现 | |
| P55 | [ ] | `python/sandbox/neurospace/neurospace.py` | 神经空间实现 | |
| P56 | [ ] | `python/sandbox/bhv_binding/bhv_binding.py` | BHV 向量绑定 | |
| P57 | [ ] | `python/sandbox/jetta/compile.py` | Jetta 编译实验 | |
| P58 | [ ] | `python/sandbox/mork/mork.py` | MORK HTTP 客户端 | |
| P59 | [ ] | `python/sandbox/resolve/resolve.py` | 解析实验 | |
| P60 | [ ] | `python/sandbox/resolve/r.py` | 解析辅助 | |
| P61 | [ ] | `python/sandbox/repl/metta_repl.py` | Python REPL 实验 | |

> **沙箱实验进度：0/14**

### 2.8 其他 Python 文件（6 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| P62 | [ ] | `metta_examples.py` | **综合功能演示**脚本（项目根） | |
| P63 | [ ] | `debug_metta.py` | 调试脚本（项目根） | |
| P64 | [ ] | `python/conanfile.py` | Conan 构建配置 | |
| P65 | [ ] | `c/conanfile.py` | C API Conan 构建配置 | |
| P66 | [ ] | `python/integration/test_torch.py` | PyTorch 集成测试 | |
| P67 | [ ] | `repl/src/py_shim.py` | REPL Python shim | |

> **其他 Python 文件进度：0/6**

### ✅ Python 总进度：0/67

---

## 三、MeTTa 源文件（67 个）

### 3.1 标准库与核心定义（2 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| M01 | [ ] | `lib/src/metta/runner/stdlib/stdlib.metta` | **MeTTa 标准库定义**（~1400行，最核心） | |
| M02 | [ ] | `lib/tests/test_stdlib.metta` | 标准库测试 | |

> **标准库进度：0/2**

### 3.2 内置模块 MeTTa 定义（8 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| M03 | [ ] | `lib/src/metta/runner/builtin_mods/random.metta` | random 模块 MeTTa 接口 | |
| M04 | [ ] | `lib/src/metta/runner/builtin_mods/fileio.metta` | fileio 模块 MeTTa 接口 | |
| M05 | [ ] | `lib/src/metta/runner/builtin_mods/json.metta` | json 模块 MeTTa 接口 | |
| M06 | [ ] | `lib/src/metta/runner/builtin_mods/catalog.metta` | catalog 模块 MeTTa 接口 | |
| M07 | [ ] | `lib/src/metta/runner/builtin_mods/das.metta` | das 模块 MeTTa 接口 | |
| M08 | [ ] | `lib/src/metta/runner/builtin_mods/skel.metta` | skel 模块骨架 | |
| M09 | [ ] | `lib/src/metta/runner/init.default.metta` | Runner 初始化默认代码 | |
| M10 | [ ] | `lib/src/metta/runner/environment.default.metta` | Environment 默认配置 | |

> **内置模块进度：0/8**

### 3.3 教学示例脚本（23 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| M11 | [ ] | `python/tests/scripts/a1_symbols.metta` | 入门：符号与表达式 | |
| M12 | [ ] | `python/tests/scripts/a2_opencoggy.metta` | 入门：OpenCog 风格 | |
| M13 | [ ] | `python/tests/scripts/a3_twoside.metta` | 入门：双向规则 | |
| M14 | [ ] | `python/tests/scripts/b0_chaining_prelim.metta` | 进阶：链式求值预备 | |
| M15 | [ ] | `python/tests/scripts/b1_equal_chain.metta` | 进阶：等式链 | |
| M16 | [ ] | `python/tests/scripts/b2_backchain.metta` | 进阶：向后链推理 | |
| M17 | [ ] | `python/tests/scripts/b3_direct.metta` | 进阶：直接求值 | |
| M18 | [ ] | `python/tests/scripts/b4_nondeterm.metta` | 进阶：非确定性 | |
| M19 | [ ] | `python/tests/scripts/b5_types_prelim.metta` | 进阶：类型初步 | |
| M20 | [ ] | `python/tests/scripts/c1_grounded_basic.metta` | Grounding 基础 | |
| M21 | [ ] | `python/tests/scripts/c2_spaces.metta` | 空间操作 | |
| M22 | [ ] | `python/tests/scripts/c2_spaces_kb.metta` | 空间知识库 | |
| M23 | [ ] | `python/tests/scripts/c3_pln_stv.metta` | PLN 概率推理 | |
| M24 | [ ] | `python/tests/scripts/d1_gadt.metta` | 类型：GADT | |
| M25 | [ ] | `python/tests/scripts/d2_higherfunc.metta` | 类型：高阶函数 | |
| M26 | [ ] | `python/tests/scripts/d3_deptypes.metta` | 类型：依赖类型 | |
| M27 | [ ] | `python/tests/scripts/d4_type_prop.metta` | 类型：类型即命题 | |
| M28 | [ ] | `python/tests/scripts/d5_auto_types.metta` | 类型：自动类型 | |
| M29 | [ ] | `python/tests/scripts/e1_kb_write.metta` | 知识库写操作 | |
| M30 | [ ] | `python/tests/scripts/e2_states.metta` | 状态管理 | |
| M31 | [ ] | `python/tests/scripts/e3_match_states.metta` | 模式匹配与状态 | |
| M32 | [ ] | `python/tests/scripts/f1_imports.metta` | 模块导入 | |
| M33 | [ ] | `python/tests/scripts/g1_docs.metta` | 文档系统 | |

> **教学示例进度：0/23**

### 3.4 模块系统辅助（3 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| M34 | [ ] | `python/tests/scripts/f1_moduleA.metta` | 模块 A（imports 测试辅助） | |
| M35 | [ ] | `python/tests/scripts/f1_moduleB.metta` | 模块 B（imports 测试辅助） | |
| M36 | [ ] | `python/tests/scripts/f1_moduleC.metta` | 模块 C（imports 测试辅助） | |

> **模块系统辅助进度：0/3**

### 3.5 测试辅助（4 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| M37 | [ ] | `python/tests/test_include.metta` | include 测试 | |
| M38 | [ ] | `python/tests/test_load.metta` | load 测试 | |
| M39 | [ ] | `python/tests/ext_sub/module.metta` | 子模块测试 | |
| M40 | [ ] | `repl/src/repl.default.metta` | REPL 默认配置 | |

> **测试辅助进度：0/4**

### 3.6 agents 扩展 MeTTa 文件（4 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| M41 | [ ] | `python/hyperon/exts/agents/tests/agent.metta` | agent 定义 | |
| M42 | [ ] | `python/hyperon/exts/agents/tests/test_0_passive_agents.metta` | 被动 agent 测试 | |
| M43 | [ ] | `python/hyperon/exts/agents/tests/test_4_events.metta` | 事件测试 | |
| M44 | [ ] | `python/hyperon/exts/agents/tests/test_4_agent1.metta` | agent1 测试 | |
| M45 | [ ] | `python/hyperon/exts/agents/tests/test_4_agent2.metta` | agent2 测试 | |

> **agents MeTTa 进度：0/5**

### 3.7 snet_io 扩展 MeTTa 文件（3 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| M46 | [ ] | `python/hyperon/exts/snet_io/snet/naint/text-generation.metta` | 文本生成服务 | |
| M47 | [ ] | `python/hyperon/exts/snet_io/test_snet_call.metta` | snet 调用测试 | |
| M48 | [ ] | `python/hyperon/exts/snet_io/test_snet_meta.metta` | snet 元数据测试 | |

> **snet_io MeTTa 进度：0/3**

### 3.8 沙箱实验 MeTTa 文件（15 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| M49 | [ ] | `python/sandbox/bhv_binding/01_example_majority.metta` | BHV 多数表决 | |
| M50 | [ ] | `python/sandbox/bhv_binding/02_example_perm.metta` | BHV 排列 | |
| M51 | [ ] | `python/sandbox/bhv_binding/03_example_dict.metta` | BHV 字典 | |
| M52 | [ ] | `python/sandbox/bhv_binding/04_example_dollar_of_mexico.metta` | BHV 示例 | |
| M53 | [ ] | `python/sandbox/jetta/test_basic_jetta.metta` | Jetta 基础测试 | |
| M54 | [ ] | `python/sandbox/jetta/test_lambda.metta` | Jetta lambda 测试 | |
| M55 | [ ] | `python/sandbox/jetta/enum_lambda.metta` | Jetta 枚举 lambda | |
| M56 | [ ] | `python/sandbox/jetta/test_expr_compile.metta` | Jetta 表达式编译 | |
| M57 | [ ] | `python/sandbox/jetta/test_nondet.metta` | Jetta 非确定性 | |
| M58 | [ ] | `python/sandbox/neurospace/test_nspace.metta` | 神经空间测试 | |
| M59 | [ ] | `python/sandbox/pytorch/tm_test.metta` | PyTorch 测试 | |
| M60 | [ ] | `python/sandbox/numpy/nm_test.metta` | NumPy 测试 | |
| M61 | [ ] | `python/sandbox/sql_space/sql_space_test.metta` | SQL 空间测试 | |
| M62 | [ ] | `python/sandbox/mork/test_mork.metta` | MORK 测试 | |
| M63 | [ ] | `python/sandbox/resolve/r.metta` | resolve 测试 | |

> **沙箱实验 MeTTa 进度：0/15**

### 3.9 其他 MeTTa 文件（4 个文件）

| # | 状态 | 文件路径 | 文件角色 | 完成时间 |
|---|------|---------|---------|---------|
| M64 | [ ] | `python/sandbox/test_gnd_conv.metta` | Grounded 转换测试 | |
| M65 | [ ] | `mkdocs.metta` | MkDocs 配置（项目根） | |
| M66 | [ ] | `integration_tests/das/animals.metta` | DAS 集成测试 | |
| M67 | [ ] | `integration_tests/das/test.metta` | DAS 集成测试 | |

> **其他 MeTTa 进度：0/4**

### ✅ MeTTa 总进度：0/67

---

## 全局进度汇总

| 语言 | 文件数 | 已完成 | 进行中 | 跳过 | 完成率 |
|------|-------|-------|-------|------|-------|
| Rust (.rs) | 85 | 0 | 0 | 0 | 0% |
| Python (.py) | 67 | 0 | 0 | 0 | 0% |
| MeTTa (.metta) | 67 | 0 | 0 | 0 | 0% |
| **合计** | **219** | **0** | **0** | **0** | **0%** |

---

## 变更记录

| 日期 | Git Commit | 操作 | 说明 |
|------|-----------|------|------|
| 2026-03-23 | `74edbddf` | 初始创建 | 基线版本，219 个文件 |
