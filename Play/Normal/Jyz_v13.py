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
        return "[A][B]{C}"
 
    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.GetBall()),
            "B": Task(Skill.SimpleGoTo(WaitPosition)),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }
 
    @override
    def transFunction(self) -> str:
        if Player.isOurPlayerControlBall():
            return "PassBall"
        elif Player.isOurPlayerLoseBall and Ball.posX() < 0:
            return "Defense"
        else:
            return "ControlBall"
 
class PassBall(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]{C}"
 
    @override
    def getTasks(self) -> "dict[str, Task]":
        # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        # TODO： 实际场地的力度可能要加1000？
 
        if Ball.posX() < 1500:
            return {
                "A": Task(Skill.NormalShoot(500, isChip=False)),
                "B": Task(Skill.RushTo(WaitPosition, Player.toBallDir("B"))),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
 
        elif 1500 < Ball.posX() < 2000:
            if Ball.posY() > 0:
                return {
                    "A": Task(Skill.NormalShoot(500, isChip=False)),
                    "B": Task(Skill.RushTo(ReceivePositionUp, Player.toBallDir("B"))),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
            else:
                return {
                    "A": Task(Skill.NormalShoot(500, isChip=False)),
                    "B": Task(Skill.RushTo(ReceivePositionDown, Player.toBallDir("B"))),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
        else:
            return {
                "A": Task(Skill.SimpleGoTo(Ball.pos())),
                # "B": Task(Skill.SimpleGoTo(PostPassPosition)),
                "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
 
    @override
    def transFunction(self) -> str:
        if Ball.isBallInBox() or Ball.isBallOutSide() or Player.isOurPlayerLoseBall(): 
            return "Defense"
        elif buffered_condition(not Player.isOurPlayerControlBall(), 30, 100):
            return "ControlBall"
        elif Ball.posX() > 2000 and Player.calToBallDist("A") < 150:
            return "LastShoot"
        else:
            return "PassBall"
 
class LastShoot(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]{C}"
 
    @override
    def getTasks(self) -> "dict[str, Task]":
        if Ball.posY() < -600 or 0 < Ball.posY() < 600:
            return {
                    "A": Task(Skill.PassToPos(GoalPointDown, 12700)),   
                    "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
        else:
            return {
                    "A": Task(Skill.PassToPos(GoalPointUp, 12700)),
                    "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
 
    @override
    def transFunction(self) -> str:
        if Ball.isBallInBox() or Player.isOurPlayerLoseBall():
            return "Defense"
        elif buffered_condition(not Player.isOurPlayerControlBall(), 30, 60):
            return "PassBall"
        else:
            return "LastShoot"
 
class Defense(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]{C}"
 
    @override
    def getTasks(self) -> "dict[str, Task]":
        if Ball.posX() < 0: # 球在本方半场
            return {
                "A": Task(Skill.NormalShoot(500, isChip=True)),
                "B": Task(Skill.WMarking(priority=1, num=Enemy.nearestToOurGoalNum())),
                "C": Task(Skill.Goalie())
            }
        else:
            return {
                "A": Task(Skill.RushTo(Ball.pos(), Player.toBallDir("A"))),
                "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                "C": Task(Skill.Goalie())
            }
 
    @override
    def transFunction(self) -> str:
        if not Ball.isBallInBox() and not Ball.isBallOutSide() and Player.isOurPlayerControlBall() and not Enemy.isEnemyControlBall():
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
class Jyz_v13(StateMachine):
    pass