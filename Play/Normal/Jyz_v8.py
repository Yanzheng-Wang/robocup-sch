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

PassPositionUp = CGeoPoint(4500, 300)
PassPositionDown = CGeoPoint(4500, -300)
ReceivePositionUp = CGeoPoint(2500, 400)
ReceivePositionDown = CGeoPoint(2500, -400)
WaitPosition = CGeoPoint(2500, 0)
PostPassPosition = CGeoPoint(1000, 0)

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
        else:
            return "ControlBall"
        
class PassBall(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]{C}"
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        if Ball.posY() > 0 and Ball.posX() < 1500:
            if Player.calToPointDist("A", Player.pos("B")) > 2500:
                return {
                    # "A": Task(Skill.PassToPos(PassPositionDown, 9000)),
                    "A": Task(Skill.NormalShoot(3000, isChip=True)),
                    "B": Task(Skill.SimpleGoTo(ReceivePositionUp)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
            else:
                return {
                    # "A": Task(Skill.PassToPos(PassPositionDown, 9000)),
                    "A": Task(Skill.NormalShoot(1000, isChip=True)),
                    "B": Task(Skill.SimpleGoTo(ReceivePositionUp)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
        elif Ball.posY() <= 0 and Ball.posX() < 1500:
            if Player.calToPointDist("A", Player.pos("B")) > 2500:
                return {
                    # "A": Task(Skill.PassToPos(PassPositionUp, 9000)),
                    "A": Task(Skill.NormalShoot(3000, isChip=True)),
                    "B": Task(Skill.SimpleGoTo(ReceivePositionDown)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
            else:
                return {
                    # "A": Task(Skill.PassToPos(PassPositionUp, 9000)),
                    "A": Task(Skill.NormalShoot(1000, isChip=True)),
                    "B": Task(Skill.SimpleGoTo(ReceivePositionDown)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
        else:
            ### ????????????????????????????
            return {
                # 这里是SimpleGoTo更好吗？
                # "A": Task(Skill.GetBall()),
                "A": Task(Skill.SimpleGoTo(Ball.pos())),
                "B": Task(Skill.SimpleGoTo(PostPassPosition)),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
        
    @override
    def transFunction(self) -> str:
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
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        if Ball.posY() < -600 or 0 < Ball.posY() < 600:
            return {
                    "A": Task(Skill.PassToPos(PassPositionDown, 9000)),
                    "B": Task(Skill.SimpleGoTo(PostPassPosition)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
        else:
            return {
                    "A": Task(Skill.PassToPos(PassPositionUp, 9000)),
                    "B": Task(Skill.SimpleGoTo(PostPassPosition)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
    
    @override
    def transFunction(self) -> str:
        if Ball.isBallInBox() or Ball.isBallOutSide() or Player.calToBallDist("A") > 2000:
            return "Defense"
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
                "A": Task(Skill.NormalShoot(3000, isChip=True)),
                "B": Task(Skill.WMarking(priority=1, num=Enemy.nearestToOurGoalNum())),
                "C": Task(Skill.Goalie())
            }
        else:
            return {
                "A": Task(Skill.SimpleGoTo(Ball.pos())),
                "B": Task(Skill.SimpleGoTo(PostPassPosition)),
                "C": Task(Skill.Goalie())
            }
    
    @override
    def transFunction(self) -> str:
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
class Jyz_v8(StateMachine):
    pass
