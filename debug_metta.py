"""
调试用脚本：从 Python 侧跟踪 MeTTa 代码的完整执行过程。

用法：
  1. 在此文件中设断点
  2. 在 runner.py / atoms.py / base.py 等文件中设断点
  3. 使用 "Python: 交互式 MeTTa 调试" 配置启动调试
"""

from hyperon import MeTTa
from hyperon.runner import RunnerState

metta = MeTTa()

# ---- 方式1: 一步到位执行 ----
result = metta.run("!(+ 1 2)")  # <-- 在此行设断点，F11 步入可追踪 Python 层
print("一步执行结果:", result)

# ---- 方式2: 单步执行（可观察每一步的中间状态）----
program = "!(+ 3 4)"
state = RunnerState(metta, program)  # <-- 在此行设断点，观察 RunnerState 初始化

step_count = 0
while not state.is_complete():
    state.run_step()  # <-- 在此行设断点，每次循环观察一步解释器状态
    step_count += 1
    intermediate = state.current_results(flat=True)
    print(f"  步骤 {step_count}: {intermediate}")

final = state.current_results()
print("单步执行结果:", final)
