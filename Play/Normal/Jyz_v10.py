# v10版本已经修了无数的bug了

from typing import override
import Global
import Utils
from Geometry import *
from Global import debugEngine
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill, SimpleGoTo, Goalie, RushTo
from Strategy import *
from Utils import buffered_condition
from Vision import Enemy, Player, Ball
from WorldModel import Flags, Conditions, Params, Positions
from RoleMatch_LuaStyle.Skills.Skill import *


ReceivePositionUp = CGeoPoint(2500, 400)
ReceivePositionDown = CGeoPoint(2500, -400)
WaitPosition = CGeoPoint(2500, 0)
PostPassPosition = CGeoPoint(1000, 0)


# TODO: 可能要根据实际情况修改
GoalPointUp = CGeoPoint(4500, 300)
GoalPointDown = CGeoPoint(4500, -300)
# GoalPointUp = CGeoPoint(4500, 380)
# GoalPointDown = CGeoPoint(4500, -380)
# GoalPointUp = CGeoPoint(4500, 400)
# GoalPointDown = CGeoPoint(4500, -400)
# GoalPointUp = CGeoPoint(4500, 450)
# GoalPointDown = CGeoPoint(4500, -450)


class ControlBall(State):
    @override
    def getMatchString(self) -> str:
        # return "[A][B]{C}"
        return "(A)(B){C}"          # 解决Defense转到ControlBall的滑动问题

    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.GetBall()),
            # "B": Task(Skill.SimpleGoTo(WaitPosition)),
            "B": Task(Skill.RushTo(WaitPosition, angle=Player.toBallDir("B"))),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }

    @override
    def transFunction(self) -> str:
        if Ball.posX() > 2500 and (Player.posX("A") > 2300 or Player.posX("B") > 2300):
            return "LastShoot"
        if Player.calToBallDist("A") < 200:
            return "PassBall"
        else:
            return "ControlBall"
        
class PassBall(State):
    @override
    def getMatchString(self) -> str:
        # return "[A][B]{C}"
        return "(A)(B){C}"              # FIXEME： 用于解决PassBall的时候一直切换状态导致的抖动
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        


        # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        # TODO： 实际场地的力度可能要加1000？


        # 后场射门，前场挑传？
        
        if Ball.posY() > 0 and Ball.posX() < 1500:
            if Player.calToPointDist("A", Player.pos("B")) > 4000:
                return {
                    # "A": Task(Skill.PassToPos(GoalPointDown, 9000)),
                    "A": Task(Skill.NormalShoot(500, isChip=True)),
                    "B": Task(Skill.RushTo(ReceivePositionUp, Player.toBallDir("B"))),
                    # "B": Task(Skill.SimpleGoTo(ReceivePositionUp)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
            elif Player.calToPointDist("A", Player.pos("B")) > 2500:
                return {
                    # "A": Task(Skill.PassToPos(GoalPointDown, 9000)),
                    "A": Task(Skill.NormalShoot(500, isChip=True)),
                    "B": Task(Skill.RushTo(ReceivePositionUp, Player.toBallDir("B"))),
                    # "B": Task(Skill.SimpleGoTo(ReceivePositionUp)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
            else:
                return {
                    # "A": Task(Skill.PassToPos(GoalPointDown, 9000)),
                    "A": Task(Skill.NormalShoot(12000, isChip=False)),
                    "B": Task(Skill.RushTo(ReceivePositionUp, Player.toBallDir("B"))),
                    # "B": Task(Skill.SimpleGoTo(ReceivePositionUp)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
        elif Ball.posY() <= 0 and Ball.posX() < 1500:
            if Player.calToPointDist("A", Player.pos("B")) > 4000:
                return {
                    # "A": Task(Skill.PassToPos(GoalPointUp, 9000)),
                    "A": Task(Skill.NormalShoot(500, isChip=True)),
                    "B": Task(Skill.RushTo(ReceivePositionDown, Player.toBallDir("B"))),
                    # "B": Task(Skill.SimpleGoTo(ReceivePositionDown)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
            elif Player.calToPointDist("A", Player.pos("B")) > 2500:
                return {
                    # "A": Task(Skill.PassToPos(GoalPointDown, 9000)),
                    "A": Task(Skill.NormalShoot(500, isChip=True)),
                    "B": Task(Skill.RushTo(ReceivePositionDown, Player.toBallDir("B"))),
                    # "B": Task(Skill.SimpleGoTo(ReceivePositionUp)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
            else:
                return {
                    # "A": Task(Skill.PassToPos(GoalPointUp, 9000)),
                    "A": Task(Skill.NormalShoot(12000, isChip=False)),
                    "B": Task(Skill.RushTo(ReceivePositionDown, Player.toBallDir("B"))),
                    # "B": Task(Skill.SimpleGoTo(ReceivePositionDown)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
        else:
            ### ????????????????????????????
            return {
                # 这里是SimpleGoTo更好吗？
                "A": Task(Skill.GetBall()),
                # "A": Task(Skill.SimpleGoTo(Ball.pos())),
                # "B": Task(Skill.SimpleGoTo(PostPassPosition)),
                "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
        
    @override
    def transFunction(self) -> str:
        if Ball.posX() > 2500 and (Player.posX("A") > 2300 or Player.posX("B") > 2300):
            return "LastShoot"
        if Ball.isBallInBox() or Ball.isBallOutSide(): # 不该再加上球在我们半场内吗
            return "Defense"
        elif Ball.posX() >= 1500 and Player.calToBallDist("A") < 300:
            return "LastShoot"
        else:
            return "PassBall"
        
class LastShoot(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]{C}"
        # return "{A}{B}{C}"
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        # ！！！！！！！！！！！！！！！！！！！！！！！！！
        # TODO：实际场地哪个效果好就用哪个

        # 因为实地passTopos力道很小，故使用Shoot TODO:测试
        # if Ball.posY() < -600 or 0 < Ball.posY() < 600:
        #     return {
        #             # "A": Task(Skill.Shoot(power = 12700)),
        #             "A": Task(Skill.PassToPos(GoalPointDown, 12700)),
        #             # "B": Task(Skill.SimpleGoTo(PostPassPosition)),
        #             "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #             "C": Task(Skill.Goalie(), fixedNumber=0)
        #         }
        # else:
        #     return {
        #             # "A": Task(Skill.Shoot(power = 12700)),
        #             "A": Task(Skill.PassToPos(GoalPointUp, 12700)),
        #             # "B": Task(Skill.SimpleGoTo(PostPassPosition)),/
        #             "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #             "C": Task(Skill.Goalie(), fixedNumber=0)
        #         }
        
        # TODO: 射门两套逻辑
        ##### 出现在y = 0不移动门将
        if Ball.posY() < 0:
            return {
                    # "A": Task(Skill.Shoot(power = 12700)),
                    "A": Task(Skill.PassToPos(GoalPointDown, 12700)),
                    # "B": Task(Skill.SimpleGoTo(PostPassPosition)),
                    "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
        else:
            return {
                    # "A": Task(Skill.Shoot(power = 12700)),
                    "A": Task(Skill.PassToPos(GoalPointUp, 12700)),
                    # "B": Task(Skill.SimpleGoTo(PostPassPosition)),/
                    "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }

    
        # if Ball.posY()-100 <= Enemy.posY(0) <= Ball.posY()+100 and Ball.posY() >= 0:
        #     return {
        #     "A": Task(Skill.PassToPos(GoalPointDown, 12000)), # isChip 可以修改
        #     # "B": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("B"))),
        #     "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #     "C": Task(Skill.Goalie(), fixedNumber=0)
        # }
        # if Ball.posY()-100 <= Enemy.posY(0) <= Ball.posY()+100 and Ball.posY() <= 0:
        #     return {
        #     "A": Task(Skill.PassToPos(GoalPointUp, 12000)), # isChip 可以修改
        #     # "B": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("B"))),
        #     "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #     "C": Task(Skill.Goalie(), fixedNumber=0)
        # }
        # if Ball.posY() >= 0:
        #    return {
        #     "A": Task(Skill.PassToPos(GoalPointUp, 12000)), # isChip 可以修改
        #     # "B": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("B"))),
        #     "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #     "C": Task(Skill.Goalie(), fixedNumber=0)
        # }
        # else:
        #     return {
        #     "A": Task(Skill.PassToPos(GoalPointDown, 12000)), # isChip 可以修改
        #     # "B": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("B"))),
        #     "B": Task(Skill.WMarking(priority=1, num = Enemy.nearestToOurGoalNum())),
        #     "C": Task(Skill.Goalie(), fixedNumber=0)
        # }

    @override
    def transFunction(self) -> str:
        # if buffered_condition(Player.kickBallVision("A"), 2, 100):
        if Ball.isBallInBox() or Ball.isBallOutSide() or Player.calToBallDist("A") >1800:
            if Ball.isBallInBox() or Ball.isBallOutSide() or Player.calToBallDist("A") > 2000:
                return "Defense"
            else:
                return "LastShoot"
        
class Defense(State):
    @override
    def getMatchString(self) -> str:
        # return "[A][B]{C}"
        return "(A)(B){C}"

    @override
    def getTasks(self) -> "dict[str, Task]":
        if Ball.posX() < 0: # 球在本方半场
            return {
                "A": Task(Skill.NormalShoot(700, isChip=True)),
                "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                # "B": Task(Skill.GetBall()),
                "C": Task(Skill.Goalie())
            }
        else:
            return {
                # "A": Task(Skill.SimpleGoTo(Ball.pos())),
                "A": Task(Skill.GetBall()),
                "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                # "B": Task(Skill.GetBall()),
                "C": Task(Skill.Goalie())
            }
    
    @override
    def transFunction(self) -> str:
        if Ball.posX() > 2500 and (Player.posX("A") > 2300 or Player.posX("B") > 2300):
            return "LastShoot"
        if not Ball.isBallInBox() and not Ball.isBallOutSide() and Player.isOurPlayerControlBall():
            if abs(Player.pos("A").x() - 2500) < 500: # 位置很好，直接补射
                return "LastShoot"
            else:
                return "ControlBall"
        else:
            return "Defense"
        
@declare_state_machine(
    ControlBall,
    PassBall,
    LastShoot,
    Defense
)
class Jyz_v10(StateMachine):
    pass