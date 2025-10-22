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
from Vision import Player, Ball, ball
from RoleMatch_LuaStyle.Skills import Skill
from WorldModel import Positions, Directions


class GetBallState(State):

    @override
    def getMatchString(self) -> str:
        return "[A][B]"

    @override
    def getTasks(self) -> "dict[str, Task]":
        
        return {
            #"A": Task(Skill.RushTo(CGeoPoint(1000,0), 0))
            #"A": Task(Skill.GetBall()),
            # "A": Task(Skill.GetBallV4(Ball.pos())),
             "A": Task(Skill.GetBallV5(Directions.ballToTheirGoal()), fixedNumber=0),
         #"A": Task(Skill.NormalShoot(12700, False)),
            #"A": Task(Skill.PassToPos(Player.Pos("B"))),
            "B": Task(Skill.RushTo(CGeoPoint(2000,-1000), Player.toBallDir("B")), fixedNumber=4),
            # "B": Task(SimpleGoTo(C.CGeoPoint(1000, 500), 0, 0)),
            # "C": Task(SimpleGoTo(C.CGeoPoint(1000, 1000), 0, 0), fixedNumber=2),
            # "D": Task(lambda: SimpleGoTo(self.playerPos("E") + CVector(200,200), 0, 0), fixedNumber=1),
            # "E": Task(SimpleGoTo(C.CGeoPoint(1000, 1500), 0, 0)),
            # "G": Task(SimpleGoTo(CGeoPoint(-3518,-3012), 0, 0)), # 应该会因为Config.py中的固定车号配置而被覆盖
            # "H": Task(SimpleGoTo(Player.Pos("E") + CVector(-200,-200), 0, 0), fixedNumber=3), # 测试传统方法的效果
            #"G": Task(Skill.Goalie()),
        }

    # 子类不覆写__init__方法也没问题，不会报错；如果覆写，一定要调用super().__init__()！！！
    def __init__(self):
        super().__init__()

    @override
    def transFunction(self):
        #a = Player.infraredOn("A")
        """状态转换函数：根据球的位置决定状态"""
        # if Global.ball().Pos().x() > 0:
        #     return "GetBallState"
        
        # return "GetBallState"
        if buffered_condition(ball().Pos().x()>0, 10, 500):
            return "PASS_BALL"
        else:
            return "GetBallState"
        
class PASS_BALL(State):

    @override
    def getMatchString(self) -> str:
        return "[A][B]"

    @override
    def getTasks(self) -> "dict[str, Task]":
        
        return {
            #"A": Task(Skill.RushTo(CGeoPoint(1000,0), 0))
            #"A": Task(Skill.GetBall()),
            # "A": Task(Skill.GetBallV4(Ball.pos())),
            # "A": Task(Skill.GetBallV5(Directions.ballToTheirGoal())),
         #"A": Task(Skill.NormalShoot(12700, False)),
            # "A": Task(Skill.PassToPos(Player.Pos("B")), fixedNumber=0),
            "A": Task(Skill.GetBallV5(Directions.ballToTheirGoal()), fixedNumber=0),
            "B": Task(Skill.RushTo(CGeoPoint(2000,-1000), Player.toBallDir("B")), fixedNumber=4),
            # "B": Task(SimpleGoTo(C.CGeoPoint(1000, 500), 0, 0)),
            # "C": Task(SimpleGoTo(C.CGeoPoint(1000, 1000), 0, 0), fixedNumber=2),
            # "D": Task(lambda: SimpleGoTo(self.playerPos("E") + CVector(200,200), 0, 0), fixedNumber=1),
            # "E": Task(SimpleGoTo(C.CGeoPoint(1000, 1500), 0, 0)),
            # "G": Task(SimpleGoTo(CGeoPoint(-3518,-3012), 0, 0)), # 应该会因为Config.py中的固定车号配置而被覆盖
            # "H": Task(SimpleGoTo(Player.Pos("E") + CVector(-200,-200), 0, 0), fixedNumber=3), # 测试传统方法的效果
            #"G": Task(Skill.Goalie()),
        }

    # 子类不覆写__init__方法也没问题，不会报错；如果覆写，一定要调用super().__init__()！！！
    def __init__(self):
        super().__init__()

    @override
    def transFunction(self):
        #a = Player.infraredOn("A")
        """状态转换函数：根据球的位置决定状态"""
        # if Global.ball().Pos().x() > 0:
        #     return "GetBallState"
        # return "GetBallState"
        return ""
        
class RECEIVE_BALL(State):

    @override
    def getMatchString(self) -> str:
        return "[A][B]"

    @override
    def getTasks(self) -> "dict[str, Task]":
        
        return {
            #"A": Task(Skill.RushTo(CGeoPoint(1000,0), 0))
            #"A": Task(Skill.GetBall()),
            # "A": Task(Skill.GetBallV4(Ball.pos())),
            # "A": Task(Skill.GetBallV5(Directions.ballToTheirGoal())),
         #"A": Task(Skill.NormalShoot(12700, False)),
            "A": Task(Skill.RushTo(CGeoPoint(-2000,1000), 0), fixedNumber=0),
            "B": Task(Skill.NormalShoot(12700, False), fixedNumber=4),
            # "B": Task(SimpleGoTo(C.CGeoPoint(1000, 500), 0, 0)),
            # "C": Task(SimpleGoTo(C.CGeoPoint(1000, 1000), 0, 0), fixedNumber=2),
            # "D": Task(lambda: SimpleGoTo(self.playerPos("E") + CVector(200,200), 0, 0), fixedNumber=1),
            # "E": Task(SimpleGoTo(C.CGeoPoint(1000, 1500), 0, 0)),
            # "G": Task(SimpleGoTo(CGeoPoint(-3518,-3012), 0, 0)), # 应该会因为Config.py中的固定车号配置而被覆盖
            # "H": Task(SimpleGoTo(Player.Pos("E") + CVector(-200,-200), 0, 0), fixedNumber=3), # 测试传统方法的效果
            #"G": Task(Skill.Goalie()),
        }

    # 子类不覆写__init__方法也没问题，不会报错；如果覆写，一定要调用super().__init__()！！！
    def __init__(self):
        super().__init__()

    @override
    def transFunction(self):
        a = Player.infraredOn("A")
        """状态转换函数：根据球的位置决定状态"""
        # if Global.ball().Pos().x() > 0:
        #     return "GetBallState"
        # return "GetBallState"
        # if buffered_condition(Player.kickBall("A"), 10, 500):
        #     return "RECEIVE_BALL"
        # else:
        #     return "GetBallState"
        if False:
            return "GetBallState"
        else:
            return "RECEIVE_BALL"


# 第一个状态是最初状态（GO_FORWARD）
# todo: start state
@declare_state_machine(
                       GetBallState,
                       PASS_BALL,
                       RECEIVE_BALL
                       )
class Test_GetBall(StateMachine):
    """示例任务组：继承自 StateMachine，定义具体的状态和任务"""
    pass





