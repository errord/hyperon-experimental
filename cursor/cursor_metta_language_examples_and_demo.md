# Metta language examples and demonstrations
_Exported on 3/20/2026 at 16:52:26 GMT+8 from Cursor (2.6.20)_

---

**User**

你帮我写一些metta语言的例子：
1. 创建基本的DAG图
2. 创建一个超图
3. 演示超图的增删查改
4. 演示超图之上的模式匹配，这里超图要稍微复杂点，能匹配一个子图。但总体上还是要人类可以看明白的，不要超过人类可以理解的程度
5. 其它的各种metta的能力演示

上述内容都必须打印出拓补结构，要人类容易看懂。并且最好是每个动作之后都打印，让我能看到整个过程，也要有中文的解释，让我容易理解。

你要自己调试、验证通过，不要有错误。

---

**Cursor**

让我查看一些现有的MeTTa示例文件，了解具体的语法和输出方式。

Now let me check how to run metta scripts and understand the `println!` and `format-args` usage better.

让我先检查一下Python环境和现有的调试脚本。

MeTTa环境可以正常运行。让我测试一些关键操作。

PowerShell会解析`$`符号，所以直接写Python文件来执行。让我创建完整的示例脚本。

需要修复编码问题。让我将Unicode特殊字符替换为ASCII字符，并设置UTF-8输出。

Now let me also fix the table separators in Part 2 and Part 4:

Now fix the arrows in Part 2 print:

Now fix the Part 2 conjunction match and arrows:

Now fix Part 3 arrows:

Now fix Part 4 special chars:

Now fix Part 4 conjunction descriptions:

Now fix Part 5 special chars:

Also fix remaining special characters:

Good, it's already fixed. Let me now also check for any remaining non-ASCII characters that might cause issues:

Now let me also check the remaining text for other special chars:

Now let me run it again:

The script seems to be hanging. Let me kill it and debug section by section.

Let me test each section independently to find the hanging issue. Let me create small test scripts.

Part 1 works. Let me test Part 2 (Hypergraph).

Part 2 works. Let me test Part 3 (CRUD).

Part 3 works. Now test Part 4 (complex pattern matching).

Part 4 works. Now let me test Part 5 (other capabilities) section by section since the hang was likely there.

The factorial issue is that MeTTa tries both rules for `(factorial 0)`, leading to infinite recursion. I need to add a guard. Let me fix and test.

Now let me test the other parts of section 5:

Found issues: 1) Type system example has a subtype error, 2) Factorial needed a guard (already fixed). Let me fix the type system example and update the main script.

Good. Approach 1 works - just remove the `(: sound (-> Animal String))` type annotation. Now let me update the main script with all fixes:

Now let me fix all the issues found during testing:

Now let me also fix the remaining em-dashes in the file:

Now let me also check for any remaining Unicode-special characters:

The `═` characters are only in comments (not printed), so they're fine. Let me run the full corrected script:

所有部分都运行成功了。现在让我修复一些输出格式问题 — 有些 label 缩进没对齐。

Now let me clean up the temporary test files and do a final run:

Now let me do the final run to confirm everything is clean:

全部通过验证，脚本已经写好并测试完成。文件是 `metta_examples.py`，运行方式：`python metta_examples.py`。

下面是脚本的五大部分总结：

**第一部分：DAG（有向无环图）**
- 用 `(edge A B)` 表示有向边，存入独立空间 `&dag`
- 演示了 `add-atom`、`get-atoms` 查看拓扑，以及用 `match` 做单步查询和两步路径查询（联合匹配 `,`）

**第二部分：超图（Hypergraph）**
- 超边连接多个节点：`(collaboration Zhang Li Wang)` 三人合作、`(research-area Zhang AI NLP)` 多元关系
- 演示了单模式匹配和三模式联合查询（同时研究AI且有论文合作）

**第三部分：CRUD 增删查改**
- `add-atom` 增、`match` 查、`remove-atom` + `add-atom` 改、`remove-atom` 删
- 每步操作后都用 `get-atoms` 打印完整空间状态

**第四部分：复杂模式匹配（子图匹配）**
- 构建了一个包含部门、员工、项目、技能的17原子超图
- 演示了从单模式到三模式联合的逐步递进匹配：找高级员工、经理-初级员工关系、跨部门项目、Python技能+项目+员工三重联合

**第五部分：其他MeTTa能力**
- 5.1 递归函数（阶乘）
- 5.2 类型系统（类型层次 + 多态）
- 5.3 非确定性计算（superpose / collapse）
- 5.4 条件表达式（if 嵌套）
- 5.5 逻辑推理（反向链推理证明 Socrates 会死）
- 5.6 可变状态（new-state / change-state! / get-state）
- 5.7 let / let* 绑定
- 5.8 case 模式匹配表达式
- 5.9 列表操作（car / cdr / cons / size）

