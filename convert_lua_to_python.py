"""
用于先进行AI翻译把lua变成python（包括很多语法上、下标索引上面的改动）
然后再进行一些批量的替换以适应新脚本的命名和函数

细节：
Lua 的 table 和 Python 的 list/dict 在用法上有差异，已做适配。
Lua 的闭包和索引从1的习惯已做 Python 化处理（Python索引从0）。

Prompt: (mode: ask)
帮我把当前文件lua的代码转成用python语言书写的，保持函数名称的命名样式不变
"""


import os
import re

relative_path = 'Vision/Enemy.py'
# relative_path = 'Play/RefPlay/KickOff.py'
# relative_path = 'waited_to_convert.py'

abs_path = os.path.abspath(relative_path)
with open(abs_path, 'r', encoding='utf-8') as f:
    content = f.read()


# 全字匹配 "ball()."，且区分大小写
new_content = re.sub(r'\bball\.', 'Ball.', content) # \b 是正则表达式中的单词边界（word boundary）
new_content = re.sub(r'\bparam\.', 'Params.', new_content)
new_content = re.sub(r'\benemy\.', 'Enemy.', new_content)
new_content = re.sub(r'\bposmodule\.getPos', 'CppPackage.getPosModulePos', new_content)
new_content = re.sub(r'\bplayer\.', 'Player.', new_content)
new_content = re.sub(r'\bpos\.', 'Positions.', new_content)
new_content = re.sub(r'\bPosition\.', 'Positions.', new_content)
new_content = re.sub(r'\bdir\.', 'Directions.', new_content)
new_content = re.sub(r'\bDirection\.', 'Directions.', new_content)
new_content = re.sub(r'\bflag\.', 'Flags.', new_content)
new_content = re.sub(r'\bFlag\.', 'Flags.', new_content)
new_content = re.sub(r'\bcond\.', 'Conditions.', new_content)
new_content = re.sub(r'\bbufcnt\b', 'buffered_condition', new_content)
new_content = re.sub(r'\bkp\.', 'FlatPower.', new_content)
new_content = re.sub(r'\bcp\.', 'ChipPower.', new_content)
new_content = re.sub(r'\bIS_SIMULATION\b', 'Global.isSimulation', new_content)
new_content = re.sub(r'\bIS_RIGHT\b', 'Global.isRight', new_content)
new_content = re.sub(r'\bIS_YELLOW\b', 'Global.isYellow', new_content)
new_content = re.sub(r'\bbeckham\.', 'beckhamDecision.', new_content)
new_content = re.sub(r'\bmessi\.', 'messiDecision.', new_content)
new_content = re.sub(r'\bdefenceSquence\.', 'defenceSequence.', new_content)

# skill相关的调整
new_content = re.sub(r'\bgoCmuRush\(', 'RushTo(', new_content)
new_content = re.sub(r'\bwback\(', 'WBack(', new_content)
new_content = re.sub(r'\bgoalie\(', 'Goalie(', new_content)
new_content = re.sub(r'\bstaticGetBall\(', 'StaticGetBall(', new_content)
new_content = re.sub(r'\bstaticGetBallV2\(', 'StaticGetBall(', new_content)
new_content = re.sub(r'\bshoot\(', 'Shoot(', new_content)
new_content = re.sub(r'\bmarking\(', 'Marking(', new_content)
new_content = re.sub(r'\btask\.shootGen\(', 'generateShootPoint(', new_content)
new_content = re.sub(r'\bgoSpeciPos\(', 'SmartGoTo(', new_content)
new_content = re.sub(r'\bcrosserover\(', 'Crossover(', new_content)
new_content = re.sub(r'\bCrosserover\(', 'Crossover(', new_content)
new_content = re.sub(r'\bstop\(', 'Stop(', new_content)

# role的调整
role_names = [
    "Goalie", "Kicker", "Assister", "Special", "Defender", "Middle",
    "Leader", "Tier", "Breaker", "Fronter", "Receiver", "Center"
]
for name in role_names:
    new_content = re.sub(rf'"{name}"', f'"{name[0]}"', new_content)

# 最后才将 task.<func>(...) 替换为 Task(Skill.<func>(...)), 保持末尾逗号或换行符
new_content = re.sub(
    r'task\.(\w+)\((.*?)\)(?P<end>,?\n)',
    r'Task(Skill.\1(\2))\g<end>',
    new_content
)

with open(abs_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
        
