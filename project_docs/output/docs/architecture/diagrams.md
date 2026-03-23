---
title: Hyperon 架构图表集
description: 总体架构、执行、类型、空间、模块与 FFI 的 Mermaid 图汇总
---

# 架构图表集

本文集中列出文档站常用的 **Mermaid** 图，便于单独引用或嵌入其它页面。图中 **节点 ID** 不使用空格；含特殊字符的标签使用引号包裹。

## 1. 总体分层栈

```mermaid
flowchart TB
    subgraph L1["语言与用户代码"]
        Mtxt["MeTTa 源码"]
        PyPkg["Python hyperon"]
    end
    subgraph L2["绑定层"]
        Hpy["hyperonpy"]
        Cdy["hyperonc C API"]
    end
    subgraph L3["Rust 核心"]
        Run["hyperon 运行器与解释器"]
        Spc["hyperon-space"]
        Atm["hyperon-atom"]
        Com["hyperon-common"]
        Mac["hyperon-macros"]
    end
    Mtxt --> PyPkg
    PyPkg --> Hpy
    Hpy --> Cdy
    Cdy --> Run
    Run --> Spc
    Run --> Atm
    Spc --> Atm
    Atm --> Com
    Atm --> Mac
    Spc --> Mac
```

## 2. Cargo Workspace 七个成员依赖

箭头由 **依赖方** 指向 **被依赖的 crate**（与 `Cargo.toml` 一致；**`hyperon-macros`** 仅依赖 `litrs`，不依赖 `hyperon-common`）。

```mermaid
flowchart BT
    repl["metta-repl"]
    hnc["hyperonc"]
    hn["hyperon"]
    hs["hyperon-space"]
    ha["hyperon-atom"]
    hm["hyperon-macros"]
    hcom["hyperon-common"]
    repl --> hn
    repl --> ha
    repl --> hcom
    hnc --> hn
    hnc --> hs
    hnc --> ha
    hnc --> hcom
    hn --> hs
    hn --> ha
    hn --> hcom
    hn --> hm
    hs --> ha
    hs --> hcom
    hs --> hm
    ha --> hcom
    ha --> hm
```

## 3. 端到端数据流（Python → Rust）

```mermaid
sequenceDiagram
    participant Py as Python
    participant Hp as hyperonpy
    participant Cc as hyperonc
    participant Rs as hyperon_Rust
    Py->>Hp: run / step
    Hp->>Cc: FFI
    Cc->>Rs: Metta RunnerState
    Rs-->>Cc: 结果
    Cc-->>Hp: catom 数组
    Hp-->>Py: Atom 对象
```

## 4. MeTTa 执行总流水线

```mermaid
flowchart LR
    A["文本"] --> B["SExprParser"]
    B --> C["Tokenizer"]
    C --> D["Atom"]
    D --> E["Metta::run"]
    E --> F["RunnerState"]
    F --> G["InterpreterState"]
    G --> H["interpret_step"]
    H --> I["Vec_Vec_Atom"]
```

## 5. 解析：字符流到 Atom 树

```mermaid
flowchart TB
    Chr["字符迭代器"]
    P["SExprParser"]
    T["Tokenizer"]
    subgraph kinds["Atom 变体"]
        S["Symbol"]
        V["Variable"]
        E["Expression"]
        G["Grounded"]
    end
    Chr --> P
    P --> T
    T --> S
    T --> V
    T --> E
    T --> G
```

## 6. Runner 状态机（MettaRunnerMode）

```mermaid
stateDiagram-v2
    [*] --> ADD
    ADD --> INTERPRET: 下一条为可求值 Atom
    INTERPRET --> ADD: 单条解释结束
    ADD --> TERMINATE: 无更多输入
    INTERPRET --> TERMINATE: 错误停止
    TERMINATE --> [*]
```

## 7. RunContext::step 决策

```mermaid
flowchart TB
    entry["step 入口"]
    q1{"存在 InterpreterState?"}
    q2{"has_next?"}
    istep["interpret_step"]
    fin["into_result 写入 results"]
    next["next_op tokenizer"]
    entry --> q1
    q1 -->|是| q2
    q2 -->|是| istep
    q2 -->|否| fin
    q1 -->|否| next
```

## 8. interpret_step 主循环

```mermaid
flowchart LR
    S0["State_n"]
    T["interpret_step"]
    S1["State_n+1"]
    S0 --> T
    T --> S1
    S1 -->|"继续"| T
    S1 -->|"结束"| R["结果列表"]
```

## 9. eval / 求值路径（INTERPRET 模式）

```mermaid
flowchart TB
    atom["Executable::Atom"]
    tc{"type-check auto?"}
    wrap["wrap_atom_by_metta_interpreter"]
    init["interpret_init"]
    step["interpret_step 直到完成"]
    atom --> tc
    tc -->|是且类型错误| err["finished 错误 Atom"]
    tc -->|否或通过| wrap
    wrap --> init
    init --> step
```

## 10. 类型检查流程

```mermaid
flowchart TB
    en["进入 INTERPRET"]
    g["get_atom_types"]
    allerr{"全部为 AtomType::Error?"}
    ok["interpret_init"]
    short["直接 finished 状态"]
    en --> g
    g --> allerr
    allerr -->|是| short
    allerr -->|否| ok
```

## 11. Rust Atom 枚举结构

```mermaid
flowchart TB
    root["Atom"]
    root --> sym["Symbol(SymbolAtom)"]
    root --> expr["Expression(ExpressionAtom)"]
    root --> var["Variable(VariableAtom)"]
    root --> gnd["Grounded(Box dyn GroundedAtom)"]
```

## 12. Python 原子类层次

```mermaid
flowchart TB
    base["Atom"]
    base --> symc["SymbolAtom"]
    base --> varc["VariableAtom"]
    base --> exprc["ExpressionAtom"]
    base --> gndc["GroundedAtom"]
```

## 13. Grounded trait 体系

```mermaid
flowchart TB
    GA["GroundedAtom trait"]
    G["Grounded"]
    CX["CustomExecute"]
    CM["CustomMatch"]
    GA --> G
    G --> CX
    G --> CM
```

## 14. Grounded 算子执行时序

```mermaid
sequenceDiagram
    participant IS as InterpreterState
    participant GE as Grounded_CustomExecute
    participant SP as Space
    IS->>SP: 查规则 / 匹配
    IS->>GE: execute_bindings
    GE-->>IS: 多分支 Atom + Bindings
```

## 15. Space / SpaceMut / DynSpace

```mermaid
flowchart LR
    Sp["trait Space"]
    Sm["trait SpaceMut"]
    Dy["DynSpace"]
    Sp --> Sm
    Sm --> Dy
```

## 16. GroundingSpace 与 AtomIndex

```mermaid
flowchart TB
    GS["GroundingSpace"]
    AI["AtomIndex"]
    Q["query 模式"]
    GS --> AI
    Q --> GS
```

## 17. ModuleSpace 组合视图

```mermaid
flowchart TB
    MS["ModuleSpace"]
    Base["内层 Space"]
    Dep["依赖 Space Atom"]
    MS --> Base
    MS --> Dep
```

## 18. Python 空间桥接（AbstractSpace → CSpace）

```mermaid
flowchart LR
    Ab["AbstractSpace"]
    Gref["GroundingSpaceRef"]
    Sref["SpaceRef"]
    Cs["CSpace"]
    Ab --> Gref
    Ab --> Sref
    Gref --> Cs
    Sref --> Cs
```

## 19. Bindings 与模式匹配

```mermaid
flowchart TB
    Pat["模式 Atom"]
    Sub["主体 Atom"]
    M["match_atoms"]
    B["Bindings / BindingsSet"]
    Pat --> M
    Sub --> M
    M --> B
```

## 20. 非确定性分支（多结果）

```mermaid
flowchart TB
    one["单步归约"]
    split["多条规则或多 Bindings"]
    many["Vec 或迭代器 of 结果"]
    one --> split
    split --> many
```

## 21. import! 到 RunContext

```mermaid
flowchart LR
    IM["ImportOp"]
    LM["RunContext::load_module"]
    ML["ModuleLoader"]
    MM["MettaMod"]
    IM --> LM
    LM --> ML
    ML --> MM
```

## 22. 模块加载序列（含 init_self_module）

```mermaid
sequenceDiagram
    participant RC as RunContext
    participant LD as ModuleLoader
    participant RS as RunnerState
    RC->>LD: prepare
    RC->>RS: 子加载 RunnerState
    RS->>RC: init_self_module
    RS-->>RC: finalize_loading
```

## 23. Runner 初始化（stdlib / corelib）

```mermaid
sequenceDiagram
    participant M as Metta::new_with_stdlib_loader
    participant CL as CoreLibLoader
    participant ST as StdlibLoader
    M->>CL: load_module_direct corelib
    M->>ST: load_module_direct stdlib
    M-->>M: top MettaMod + GroundingSpace
```

## 24. 标准库功能分组（示意）

```mermaid
flowchart TB
    subgraph std["stdlib 模块族"]
        sp["space 空间算子"]
        md["module import 等"]
        at["atom 与类型辅助"]
        lg["逻辑与控制"]
    end
    core["corelib 内核规则"]
    core --> std
```

## 25. AtomIndex 与 Trie 令牌（概念）

```mermaid
flowchart TB
    atom["Atom 子结构"]
    key["TrieKey 令牌序列"]
    idx["AtomIndex 查询"]
    atom --> key
    key --> idx
```

## 26. C API FFI 桥接层次

```mermaid
flowchart TB
    Py["Python"]
    Pyo3["PyO3 hyperonpy"]
    Chdr["C 头文件 ABI"]
    RustC["hyperonc 实现"]
    RustL["hyperon lib"]
    Py --> Pyo3
    Pyo3 --> Chdr
    Chdr --> RustC
    RustC --> RustL
```

## 27. Trie / MultiTrie（stdlib atom 辅助）

```mermaid
flowchart LR
    A2K["atom_to_trie_key"]
    MT["MultiTrie"]
    IDX2["规则或 RHS 索引"]
    A2K --> MT
    MT --> IDX2
```

---

**说明**：部分图为 **概念示意**；模块导入与类型检查的边界行为以源码与测试为准。若与独立章节文档重复，可优先引用本页图号以保持站点图表一致。
