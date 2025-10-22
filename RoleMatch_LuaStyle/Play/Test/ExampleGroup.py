from typing import override

import CppPackage as C
import Global
from Geometry import *
from RoleMatch_LuaStyle.Skills import Goalie
from RoleMatch_LuaStyle.Skills.Skill import SimpleGoTo, RushTo
from RoleMatch_LuaStyle.State import State
from RoleMatch_LuaStyle.StateMachine import declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Task import Task
from Utils import buffered_condition
from Vision import Player
from RoleMatch_LuaStyle.Skills import Skill

class GO_FORWARD(State):

    @override
    def getMatchString(self) -> str:
        return "(A)[CDEGH]"

    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.GetBall()),
            # "B": Task(SimpleGoTo(C.CGeoPoint(1000, 500), 0, 0)),
            "C": Task(SimpleGoTo(C.CGeoPoint(1000, 1000), 0, 0), fixedNumber=2),
            "D": Task(lambda: SimpleGoTo(self.playerPos("E") + CVector(200,200), 0, 0), fixedNumber=1),
            "E": Task(SimpleGoTo(C.CGeoPoint(1000, 1500), 0, 0)),
            "G": Task(SimpleGoTo(CGeoPoint(-3518,-3012), 0, 0)), # 应该会因为Config.py中的固定车号配置而被覆盖
            "H": Task(SimpleGoTo(Player.Pos("E") + CVector(-200,-200), 0, 0), fixedNumber=3), # 测试传统方法的效果
        }

    # 子类不覆写__init__方法也没问题，不会报错；如果覆写，一定要调用super().__init__()！！！
    def __init__(self):
        super().__init__()

    @override
    def transFunction(self):
        """状态转换函数：根据球的位置决定状态"""
        if Global.ball().Pos().x() > 0:
            return "GO_FORWARD"
        return "GO_BACKWARD"


class GO_BACKWARD(State):
    @override
    def getMatchString(self) -> str:
        return "(A)[CDEGH]"

    @override
    def getTasks(self) -> "dict[str, Task]":
        return{
            "A": Task(Skill.GetBall()),
            # "B": Task(SimpleGoTo(C.CGeoPoint(-1000, 500), 0, 0)),
            "C": Task(SimpleGoTo(C.CGeoPoint(-1000, 1000), 0, 0), fixedNumber=2),
            "D": Task(lambda: SimpleGoTo(self.playerPos("E"), 0, 0), fixedNumber=1),
            "E": Task(SimpleGoTo(C.CGeoPoint(-1000, 1500), 0, 0)),
            "H": Task(RushTo(CGeoPoint(100,200), 3, 0)),
            # "I": Task(lambda: RushTo(self.playerPos("H"), 3, 0)),
            "G": Task(SimpleGoTo(CGeoPoint(-3518, 3012), 0, 0)),  # 应该会因为Config.py中的固定车号配置而被覆盖
        }


    @override
    def transFunction(self):
        """状态转换函数：根据球的位置决定状态"""
        if Global.ball().Pos().x() > 0:
            return "GO_FORWARD"
        return "GO_BACKWARD"


class Go_Other(State):
    def transFunction(self) -> str:
        pass

    def getMatchString(self) -> str:
        pass

    def getTasks(self) -> "dict[str, Task]":
        # 下面示例通过这样的方法复用tasks
        p = GO_BACKWARD()
        tasks = p.getTasks()
        tasks["C"] = Task(SimpleGoTo(C.CGeoPoint(1000, 1000), 0, 0), fixedNumber=0)
        return tasks

class Attack(State):

    def getMatchString(self) -> str:
        return "[ABCD]"

    def getTasks(self) -> "dict[str, Task]":
        return {
            "A":Task(SimpleGoTo(CGeoPoint(300,200)),fixedNumber=3),
            "B":Task(SimpleGoTo(CGeoPoint(200,100))),
            "G":Task(Goalie(CGeoPoint(200,100))),
            "C":Task(SimpleGoTo(Player.Pos("A"))),
            "D":Task(SimpleGoTo(CGeoPoint(200,1000))),
        }

    def transFunction(self) -> str:
        if buffered_condition(Global.ball().Pos().x() > 0,10,100):
            return "GO_FORWARD"
        return "GO_BACKWARD"


# 第一个状态是最初状态（GO_FORWARD）
# todo: start state
@declare_state_machine(
                       GO_FORWARD,
                       GO_BACKWARD,
                       )
class ExampleGroup(StateMachine):
    """示例任务组：继承自 StateMachine，定义具体的状态和任务"""
    pass





