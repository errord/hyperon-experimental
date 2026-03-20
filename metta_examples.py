"""
MeTTa 语言能力演示
==================
演示内容：
  1. 创建基本的DAG（有向无环图）
  2. 创建超图（Hypergraph）
  3. 超图的增删查改（CRUD）
  4. 超图上的复杂模式匹配
  5. 其他 MeTTa 能力（函数、类型、推理、状态等）
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from hyperon import MeTTa, Environment


def new_metta():
    return MeTTa(env_builder=Environment.custom_env(working_dir=".", config_dir=""))


def banner(title):
    print("\n" + "=" * 62)
    print(f"  {title}")
    print("=" * 62)


def step(text):
    print(f"\n--- {text} ---")


def show_space(metta, token, label):
    """显示空间中的所有原子，以列表形式打印"""
    atoms = metta.run(f"!(get-atoms {token})")[0]
    print(f"\n  [{label}] 空间内容 ({len(atoms)} 个原子):")
    for a in atoms:
        print(f"    * {a}")


def run_show(metta, code, label=""):
    """运行 MeTTa 代码并打印结果"""
    results = metta.run(code)
    if label:
        print(f"  {label}")
    for group in results:
        if group:
            for atom in group:
                print(f"    => {atom}")
    return results


# ═════════════════════════════════════════════════════════════
#  第一部分：创建基本的 DAG（有向无环图）
# ═════════════════════════════════════════════════════════════
banner("第一部分：创建基本的 DAG（有向无环图）")

print("""
  DAG (Directed Acyclic Graph) 是有方向、无环路的图。
  在 MeTTa 中，我们用原子表达式 (edge 源 目标) 来表示有向边。

  要构建的 DAG 结构：

      A --> B --> D
      |     |
      |     v
      +---> C --> E --> F
""")

m = new_metta()

step("步骤 1：创建一个新空间，用来存放 DAG")
m.run("!(bind! &dag (new-space))")
print("  已创建空间 &dag")

step("步骤 2：逐条添加有向边")
edges = [
    "(edge A B)", "(edge A C)", "(edge B D)",
    "(edge C E)", "(edge B E)", "(edge E F)",
]
for e in edges:
    m.run(f"!(add-atom &dag {e})")
    print(f"  添加: {e}")

show_space(m, "&dag", "DAG 拓扑")

step("步骤 3：查询 -- A 的直接后继节点")
run_show(m, "!(match &dag (edge A $x) $x)",     "A -> ?")

step("步骤 4：查询 -- 谁指向 E？(E 的前驱)")
run_show(m, "!(match &dag (edge $x E) $x)", "? -> E")

step("步骤 5：查询 -- 经一步中间节点从 A 到达 E 的路径")
run_show(m,
    "!(match &dag (, (edge A $mid) (edge $mid E)) (path A $mid E))",
    "两步路径 A -> ? -> E:")

step("步骤 6：查询 -- 所有的边")
run_show(m, "!(match &dag (edge $from $to) ($from -> $to))", "所有边:")


# ═════════════════════════════════════════════════════════════
#  第二部分：创建超图（Hypergraph）
# ═════════════════════════════════════════════════════════════
banner("第二部分：创建超图（Hypergraph）")

print("""
  超图与普通图的区别：一条"超边"可以连接 2 个以上的节点。
  在 MeTTa 中，一个表达式天然可以包含任意多个元素，
  因此非常适合表示超图。

  我们构建一个"学术合作"超图：

  超边类型          内容                     含义
  ------------------------------------------------
  collaboration     (张三 李四 王五)         三人合作项目
  collaboration     (李四 赵六)              两人合作项目
  research-area     (张三 AI NLP)            张三的研究方向
  research-area     (李四 AI DataMining)     李四的研究方向
  research-area     (王五 ML DeepLearning)   王五的研究方向
  paper             (张三 李四 AAAI-2024)    发表论文
""")

m2 = new_metta()
m2.run("!(bind! &hyper (new-space))")

step("步骤 1：添加超边")
hyperedges = [
    "(collaboration Zhang Li Wang)",
    "(collaboration Li Zhao)",
    "(research-area Zhang AI NLP)",
    "(research-area Li AI DataMining)",
    "(research-area Wang ML DeepLearning)",
    "(paper Zhang Li AAAI-2024)",
]
for he in hyperedges:
    m2.run(f"!(add-atom &hyper {he})")
    print(f"  添加超边: {he}")

show_space(m2, "&hyper", "超图拓扑")

step("步骤 2：查找所有研究 AI 的人")
run_show(m2,
    "!(match &hyper (research-area $person AI $sub) ($person sub-field $sub))",
    "研究 AI 的人及子方向:")

step("步骤 3：查找张三参与的合作（三人合作）")
run_show(m2,
    "!(match &hyper (collaboration Zhang $p1 $p2) (Zhang cooperates-with $p1 and $p2))",
    "张三的三人合作:")

step("步骤 4：联合查询 -- 同时研究 AI 且有论文合作的人")
run_show(m2, """
    !(match &hyper
        (, (research-area $p1 AI $f1)
           (research-area $p2 AI $f2)
           (paper $p1 $p2 $venue))
        ($p1 and $p2 both-study-AI published-at $venue))
""", "AI 领域且有共同论文:")


# ═════════════════════════════════════════════════════════════
#  第三部分：超图的增删查改（CRUD）
# ═════════════════════════════════════════════════════════════
banner("第三部分：超图的增删查改（CRUD 操作）")

print("""
  MeTTa 提供了操作空间的原语：
    add-atom    -- 添加原子
    remove-atom -- 删除原子
    get-atoms   -- 列出所有原子
    match       -- 模式匹配查询
""")

m3 = new_metta()
m3.run("!(bind! &db (new-space))")

# --- Create ---
step("C (Create) -- 创建初始知识")
facts = [
    "(person Alice age 30)",
    "(person Bob age 25)",
    "(person Carol age 35)",
    "(friend Alice Bob)",
    "(friend Bob Carol)",
]
for f in facts:
    m3.run(f"!(add-atom &db {f})")
    print(f"  + {f}")

show_space(m3, "&db", "创建后")

# --- Read ---
step("R (Read) -- 查询操作")
print("\n  查询 1: 所有人员信息")
run_show(m3, "!(match &db (person $name age $age) ($name age $age))")
print("\n  查询 2: Alice 的朋友")
run_show(m3, "!(match &db (friend Alice $f) $f)")
print("\n  查询 3: 谁是 Bob 的朋友? (谁把 Bob 当朋友)")
run_show(m3, "!(match &db (friend $who Bob) $who)")

# --- Update (先删后加) ---
step("U (Update) -- 修改 Bob 的年龄 25 -> 26")
m3.run("!(remove-atom &db (person Bob age 25))")
print("  - 删除旧值: (person Bob age 25)")
m3.run("!(add-atom &db (person Bob age 26))")
print("  + 添加新值: (person Bob age 26)")
show_space(m3, "&db", "修改后")

print("\n  验证修改 -- 查询 Bob 的年龄:")
run_show(m3, "!(match &db (person Bob age $age) $age)")

# --- Delete ---
step("D (Delete) -- 删除 Carol 及相关关系")
m3.run("!(remove-atom &db (person Carol age 35))")
print("  - 删除: (person Carol age 35)")
m3.run("!(remove-atom &db (friend Bob Carol))")
print("  - 删除: (friend Bob Carol)")

show_space(m3, "&db", "删除后")

print("\n  验证删除 -- 查询所有人员:")
run_show(m3, "!(match &db (person $name age $age) ($name age $age))")
print("\n  验证删除 -- 查询所有朋友关系:")
run_show(m3, "!(match &db (friend $a $b) ($a -> $b))")

# --- 追加新数据 ---
step("追加 -- 新增 Dave, 并与 Alice 建立关系")
m3.run("!(add-atom &db (person Dave age 28))")
m3.run("!(add-atom &db (friend Alice Dave))")
print("  + (person Dave age 28)")
print("  + (friend Alice Dave)")

show_space(m3, "&db", "最终状态")


# ═════════════════════════════════════════════════════════════
#  第四部分：超图上的复杂模式匹配（子图匹配）
# ═════════════════════════════════════════════════════════════
banner("第四部分：超图上的复杂模式匹配")

print("""
  构建一个"公司知识图谱"超图，包含：
    部门、员工、项目、技能 四类关系。
  然后用联合查询 (,) 进行跨关系的子图匹配。

  超图结构概览:

  部门:                        员工:
    Engineering <- 经理 Chen     Chen  (senior, Engineering)
    Marketing   <- 经理 Liu      Liu   (senior, Marketing)
    Research    <- 经理 Wang     Wang  (senior, Research)
                                  Zhang (junior, Engineering)
                                  Li    (junior, Engineering)
                                  Zhao  (mid,    Research)

  项目 (超边,连接多人):         技能 (超边):
    Alpha: Chen, Zhang, Li        Chen:  Python, Java
    Beta:  Wang, Zhao             Zhang: Python, Go
    Gamma: Chen, Wang             Li:    Java,   Rust
                                  Wang:  Python, ML
                                  Zhao:  ML,     Stats
""")

m4 = new_metta()
m4.run("!(bind! &co (new-space))")

company_facts = [
    # 部门
    "(dept Engineering manager Chen)",
    "(dept Marketing manager Liu)",
    "(dept Research manager Wang)",
    # 员工
    "(employee Chen senior Engineering)",
    "(employee Liu senior Marketing)",
    "(employee Wang senior Research)",
    "(employee Zhang junior Engineering)",
    "(employee Li junior Engineering)",
    "(employee Zhao mid Research)",
    # 项目（超边：连接 2~3 人）
    "(project Alpha Chen Zhang Li)",
    "(project Beta Wang Zhao)",
    "(project Gamma Chen Wang)",
    # 技能（超边：一人多技能）
    "(skill Chen Python Java)",
    "(skill Zhang Python Go)",
    "(skill Li Java Rust)",
    "(skill Wang Python ML)",
    "(skill Zhao ML Stats)",
]
for f in company_facts:
    m4.run(f"!(add-atom &co {f})")

show_space(m4, "&co", "公司知识图谱")

step("匹配 1 (单模式): 找所有高级员工及其部门")
run_show(m4,
    "!(match &co (employee $name senior $dept) ($name is-senior-in $dept))",
    "高级员工:")

step("匹配 2 (双模式联合): 找部门经理和该部门的初级员工")
print("  子图模式: dept(部门, manager, 经理) AND employee(员工, junior, 部门)")
run_show(m4, """
    !(match &co
        (, (dept $dept manager $mgr)
           (employee $emp junior $dept))
        ($mgr manages-junior $emp in $dept))
""", "经理 -> 初级员工:")

step("匹配 3 (双模式联合): 找在同一项目中的两人组合")
print("  子图模式: project(项目, A, B, C) AND employee(A, 级别, 部门)")
run_show(m4, """
    !(match &co
        (, (project $proj $p1 $p2 $p3)
           (employee $p1 $level $dept))
        (in-project $proj leader $p1 level $level from $dept))
""", "三人项目中第一人的部门:")

step("匹配 4 (三模式联合 -- 复杂子图): 找跨部门项目的成员组合")
print("  子图模式: project(项目, A, B) AND employee(A, _, 部门1) AND employee(B, _, 部门2)")
print("  要求两人来自不同部门 (跨部门合作)")
run_show(m4, """
    !(match &co
        (, (project $proj $p1 $p2)
           (employee $p1 $l1 $d1)
           (employee $p2 $l2 $d2))
        (cross-dept $proj : $p1 from $d1 and $p2 from $d2))
""", "双人项目跨部门:")

step("匹配 5 (三模式联合): 找会 Python 的人在哪些项目中做了第一负责人")
print("  子图模式: skill(人, Python, _) AND project(项目, 人, ...) AND employee(人, 级别, 部门)")
run_show(m4, """
    !(match &co
        (, (skill $person Python $other)
           (project $proj $person $m2 $m3)
           (employee $person $level $dept))
        (python-lead $person level $level dept $dept project $proj))
""", "会 Python 的项目负责人:")

step("匹配 6 (技能子图): 找同时会 ML 的人及其项目")
run_show(m4, """
    !(match &co
        (, (skill $person ML $other-skill)
           (project $proj $a $person))
        (ML-expert $person also-knows $other-skill in-project $proj))
""", "ML 专家及其项目:")


# ═════════════════════════════════════════════════════════════
#  第五部分：其他 MeTTa 能力演示
# ═════════════════════════════════════════════════════════════
banner("第五部分：MeTTa 其他能力演示")

# --- 5.1 函数定义与递归 ---
step("5.1 函数定义与递归")
m5 = new_metta()
m5.run("""
(= (factorial $n)
   (if (== $n 0) 1
       (* $n (factorial (- $n 1)))))
""")
print("  定义阶乘函数 (使用 if 防止无限递归):")
print("    (= (factorial $n)")
print("       (if (== $n 0) 1")
print("           (* $n (factorial (- $n 1)))))")
run_show(m5, "!(factorial 5)", "  factorial(5) =")
run_show(m5, "!(factorial 10)", "  factorial(10) =")

# --- 5.2 类型系统 ---
step("5.2 类型系统")
m5b = new_metta()
m5b.run("""
(: Animal Type)
(: Dog Animal)
(: Cat Animal)
(: Buddy Dog)
(: Kitty Cat)
(= (sound Buddy) "Woof!")
(= (sound Kitty) "Meow!")
""")
print("  类型层次: Animal > Dog, Cat")
print("  实例: Buddy:Dog, Kitty:Cat")
print("  函数: sound -- 通过模式匹配实现多态")
run_show(m5b, "!(sound Buddy)", "  sound(Buddy) =")
run_show(m5b, "!(sound Kitty)", "  sound(Kitty) =")
run_show(m5b, "!(get-type Buddy)", "  type(Buddy) =")
run_show(m5b, "!(get-type Kitty)", "  type(Kitty) =")

# --- 5.3 非确定性计算 ---
step("5.3 非确定性计算 (superpose / collapse)")
m5c = new_metta()
print("  superpose: 将元组展开为多个非确定性结果")
run_show(m5c, "!(superpose (apple banana cherry))", "  展开:")
print("\n  collapse: 将非确定性结果收集回元组")
run_show(m5c, "!(collapse (superpose (10 20 30 40 50)))", "  收集:")
print("\n  结合计算 -- 对每个元素翻倍:")
m5c.run("(= (double $x) (* 2 $x))")
run_show(m5c, "!(collapse (double (superpose (1 2 3 4 5))))", "  翻倍:")

# --- 5.4 条件表达式 ---
step("5.4 条件表达式")
m5d = new_metta()
m5d.run("""
(= (classify $age)
   (if (< $age 18) child
       (if (< $age 60) adult
           senior)))
""")
print("  年龄分类: <18->child, <60->adult, >=60->senior")
run_show(m5d, "!(classify 10)", "  classify(10) =")
run_show(m5d, "!(classify 35)", "  classify(35) =")
run_show(m5d, "!(classify 70)", "  classify(70) =")

# --- 5.5 逻辑推理（反向链） ---
step("5.5 逻辑推理 -- 反向链推理 (Backward Chaining)")
m5e = new_metta()
m5e.run("""
; 事实
(Fact (philosopher Socrates))
(Fact (likes-debate Socrates))

; 规则: 哲学家 + 爱辩论 -> 人类
(Rule
   (And (Fact (philosopher $x))
        (Fact (likes-debate $x)))
   (Fact (human $x)))

; 规则: 人类 -> 会死的
(Rule
   (Fact (human $x))
   (Fact (mortal $x)))

; 推理引擎: 如果事实已知则直接返回
(= (prove (Fact ($P $x)))
   (match &self (Fact ($P $x)) True))

; 推理引擎: 通过规则推导
(= (prove (Fact ($P $x)))
   (match &self (Rule $premise (Fact ($P $x)))
      (prove $premise)))

; 推理引擎: And 连接件
(= (prove (And $a $b))
   (let $ra (prove $a)
      (let $rb (prove $b)
         (if (== $ra True)
            (if (== $rb True) True False)
            False))))
""")
print("  知识库:")
print("    事实: Socrates 是哲学家, Socrates 爱辩论")
print("    规则: 哲学家 AND 爱辩论 -> 人类")
print("    规则: 人类 -> 会死的")
print("\n  推理:")
run_show(m5e, "!(prove (Fact (philosopher Socrates)))", "  Socrates是哲学家? =")
run_show(m5e, "!(prove (Fact (human Socrates)))", "  Socrates是人类? =")
run_show(m5e, "!(prove (Fact (mortal Socrates)))", "  Socrates会死? =")

# --- 5.6 可变状态 ---
step("5.6 可变状态 (State)")
m5f = new_metta()
m5f.run("!(bind! &counter (new-state 0))")
print("  创建状态: &counter = 0")
run_show(m5f, "!(get-state &counter)", "  当前值 =")

m5f.run("!(change-state! &counter 10)")
print("\n  修改状态: &counter <- 10")
run_show(m5f, "!(get-state &counter)", "  当前值 =")

m5f.run("!(change-state! &counter 42)")
print("\n  修改状态: &counter <- 42")
run_show(m5f, "!(get-state &counter)", "  当前值 =")

# --- 5.7 let 绑定 ---
step("5.7 let / let* 绑定表达式")
m5g = new_metta()
print("  let 单变量绑定:")
run_show(m5g, "!(let $x 5 (* $x $x))", "  let x=5 in x*x =")
print("\n  let* 多变量绑定:")
run_show(m5g, "!(let* (($x 3) ($y 4)) (+ (* $x $x) (* $y $y)))", "  let x=3,y=4 in x^2+y^2 =")

# --- 5.8 case 表达式 ---
step("5.8 case 模式匹配表达式")
m5h = new_metta()
m5h.run("""
(= (describe $x)
   (case $x
     ((1 "one")
      (2 "two")
      (3 "three")
      ($_ "other"))))
""")
run_show(m5h, '!(describe 1)', "  describe(1) =")
run_show(m5h, '!(describe 2)', "  describe(2) =")
run_show(m5h, '!(describe 3)', "  describe(3) =")
run_show(m5h, '!(describe 99)', "  describe(99) =")

# --- 5.9 列表操作 ---
step("5.9 列表/表达式操作")
m5i = new_metta()
print("  car-atom (取头部):")
run_show(m5i, "!(car-atom (a b c d))", "  car (a b c d) =")
print("\n  cdr-atom (取尾部):")
run_show(m5i, "!(cdr-atom (a b c d))", "  cdr (a b c d) =")
print("\n  cons-atom (构造):")
run_show(m5i, "!(cons-atom x (a b c))", "  cons x (a b c) =")
print("\n  size-atom (长度):")
run_show(m5i, "!(size-atom (a b c d e))", "  size (a b c d e) =")


# ═════════════════════════════════════════════════════════════
print("\n" + "=" * 62)
print("  所有演示完成！")
print("=" * 62)
