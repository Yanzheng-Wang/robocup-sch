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

ShootPositionUp = CGeoPoint(2500, 500) # 用于设定Pass状态B的跑位
ShootPositionDown = CGeoPoint(2500, -500)
FinishPosUp = CGeoPoint(4500, 400) # 用于配合LastShoot中的PassToPos使用
FinishPosDown = CGeoPoint(4500, -400)

class ControlBall(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]{C}"

    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.RushToV4(pos=Ball.pos(), mydir=Player.toBallDir("A"))),
            "B": Task(Skill.SimpleGoTo(CGeoPoint(2500, 0))),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }

    @override
    def transFunction(self) -> str:
        if Player.successGetBall("A"):
            return "PassBall"
        else:
            return "ControlBall"

class PassBall(State):
    @override
    def getMatchString(self) -> str:
        return "(A)(B){C}" # 设成()为了防止后续判断是否快接到球时转换身份导致一直停留在传球状态

    @override
    def getTasks(self) -> "dict[str, Task]":
        if Ball.posY() > 0: # 如果门将位置站在偏上方，向相反方向传球
            return {
                "A": Task(Skill.PassToPos(ShootPositionDown, kickpower=5500)),
                "B": Task(Skill.SimpleGoTo(ShootPositionDown)),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
        else:
            return {
                "A": Task(Skill.PassToPos(ShootPositionUp, kickpower=5500)),
                "B": Task(Skill.SimpleGoTo(ShootPositionUp)),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }

    @override
    def transFunction(self) -> str:
        if Ball.isBallInBox() or Ball.isBallOutSide():
            return "Defense"
        elif Player.calToBallDist("B") < 1200:
            return "Transition"
        else:
            return "PassBall"


class Transition(State):
    @override
    def getMatchString(self):
        return "(A)(B){C}" # 同理也是为了防止后续判断时候出现错误

    @override
    def getTasks(self):
        if Ball.posY() > 0:
            return {
                "A": Task(Skill.PassToPos(FinishPosDown, 500)),
                "B": Task(Skill.SimpleGoTo(ShootPositionDown)),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
        else:
            return {
                "A": Task(Skill.PassToPos(FinishPosUp, 500)),
                "B": Task(Skill.SimpleGoTo(ShootPositionUp)),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }

    @override
    def transFunction(self):
        if Ball.isBallInBox() or Ball.isBallOutSide(): # 球员无法进入禁区，此时为对方拿球状态
            return "Defense"
        elif Player.isOurPlayerControlBall():
            return "LastShoot"
        else:
            return "Transition"

class LastShoot(State):
    @override
    def getMatchString(self) -> str:
        return "(A)(B){C}"

    @override
    def getTasks(self) -> "dict[str, Task]":
        if Ball.posY() > 0: # 门将站在上方，那么射向下方
            return {
                "A": Task(Skill.PassToPos(FinishPosDown, 9000)),
                "B": Task(Skill.SimpleGoTo(ShootPositionDown)),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
        else: # 门将站在下方，那么射向上方
            return {
                "A": Task(Skill.PassToPos(FinishPosUp, 9000)),
                "B": Task(Skill.SimpleGoTo(ShootPositionUp)),
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
        return "(A)(B){C}"
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        if Ball.posX() < 0:
            return {
                "A": Task(Skill.NormalShoot(3000, isChip=True)),
                # "B": Task(Skill.GetBall()),
                "B": Task(Skill.SimpleGoTo(ShootPositionUp)),
                "C": Task(Skill.Goalie())
            }
        else:
            return {
                "A": Task(Skill.GetBall()),
                # "B": Task(Skill.GetBall()),
                "B": Task(Skill.SimpleGoTo(ShootPositionUp)),
                "C": Task(Skill.Goalie())
            }
    
    @override
    def transFunction(self) -> str:
        if not Ball.isBallInBox() and not Ball.isBallOutSide() and Player.isOurPlayerControlBall():
            if abs(Player.pos("A").x() - 2000) < 500 and abs(Player.pos("B").x() - 2000) < 500: # 位置很好，直接补射
                return "LastShoot"
            else:
                return "ControlBall"
        else:
            return "Defense"


@declare_state_machine(
    ControlBall,
    PassBall,
    Transition,
    LastShoot,
    Defense
)
class Jyz_v7(StateMachine):
    pass