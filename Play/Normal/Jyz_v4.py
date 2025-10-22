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

ShootPositionUp = CGeoPoint(2500, 100)
ShootPositionDown = CGeoPoint(2500, -100)

class ControlBall(State):
    @override
    def getMatchString(self) -> str:
        return "{C}[A][B]"

    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.RushToV4(pos=Ball.pos(), mydir=Player.toBallDir("A"))),
            "B": Task(Skill.SimpleGoTo(CGeoPoint(500, 0))),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }

    @override
    def transFunction(self) -> str:
        # if abs(Player.pos("A").x() - Ball.posX()) < 50 and abs(Player.pos("A").y() - Ball.posY()) < 50:
        # if Player.toBallDist("A") < 100:
        if (Player.pos("A") - Ball.pos()).mod() < 100:
            return "PassBall"
            return "PassBall"
        else:
            return "ControlBall"

class PassBall(State):
    @override
    def getMatchString(self) -> str:
        return "{C}(AB)" # 设成()为了防止后续判断是否快接到球时转换身份导致一直停留在传球状态

    @override
    def getTasks(self) -> "dict[str, Task]":
        if Enemy.getTheirGoaliePos().y() > 0: # 如果门将位置站在偏上方，向相反方向传球
            return {
                "A": Task(Skill.PassToPos(ShootPositionDown, kickpower=3000)),
                # "A": Task(Skill.PassToPos(CGeoPoint(Player.pos("B").x(), Player.pos("B").y()), kickpower=4000)),
                # "B": Task(Skill.GetBallV5(direction=toBallDir("B")))
                "B": Task(Skill.SimpleGoTo(ShootPositionDown)),
                # "B": Task(Skill.Stop())
                # "B": Task(Skill.GetBall())
                # "B": Task(Skill.StaticGetBall(target=Player.pos("B"), kickPower=5000, chipPower=0))
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
        else:
            return {
                "A": Task(Skill.PassToPos(ShootPositionUp, kickpower=3000)),
                "B": Task(Skill.SimpleGoTo(ShootPositionUp)),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }

    @override
    def transFunction(self) -> str:
        # if Player.isBallPassed("A", "B") and toBallDist("B") < 1000:
        # if abs(Ball.posX() - Player.pos("B").x()) < 1200 or abs(Ball.posY() - Player.pos("B").y()) < 800:
        if (Ball.pos() - Player.pos("B")).mod() < 500:
            return "Transition"
        else:
            return "PassBall"


class Transition(State):
    @override
    def getMatchString(self):
        return "{C}(A)(B)" # 同理也是为了防止后续判断时候出现错误

    @override
    def getTasks(self):
        return {
            # "A": Task(Skill.GetBall()),
            "A": Task(Skill.NormalShoot(12000, isChip=False)),
            # "A": Task(Skill.RushToV4(pos=Ball.pos(), mydir=Player.toBallDir("A"))),
            # "B": Task(Skill.SimpleGoTo(CGeoPoint(2000, -200)))
            "B": Task(Skill.SimpleGoTo(CGeoPoint(1200, 0))),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }

    @override
    def transFunction(self):
        if Ball.toTheirGoalDist() < 1500:
            return "ControlBall"
        elif abs(Ball.posX() - Player.pos("A").x()) < 80 and abs(Ball.posY() - Player.pos("A").y()) < 80:
            return "LastShoot"
        else:
            return "Transition"


class LastShoot(State):
    @override
    def getMatchString(self) -> str:
        return "{C}[A][B]"

    @override
    def getTasks(self) -> "dict[str, Task]":
        if Enemy.getTheirGoaliePos().y() > 0:
            return {
                "A": Task(Skill.NormalShoot(12000, isChip=False)),
                # "A": Task(Skill.PassToPos(CGeoPoint(4470, -400), kickpower=7000)),
                # "A": Task(Skill.Shoot(target=Enemy.shootp(), direction=Player.toPointDir(p=Enemy.shootp(), role="A"), power=4000)),
                # "B": Task(Skill.RushToV4(pos=Ball.pos(), mydir=toBallDir("B")))
                "B": Task(Skill.SimpleGoTo(CGeoPoint(500, 0))),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
        else:
            return {
                "A": Task(Skill.NormalShoot(12000, isChip=False)),
                # "A": Task(Skill.PassToPos(CGeoPoint(4470, 400), kickpower=7000)),
                "B": Task(Skill.SimpleGoTo(CGeoPoint(500, 0))),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }

    @override
    def transFunction(self) -> str:
        if Ball.toTheirGoalDist() < 1500:
            return "ControlBall"
        # else:
        #     return "PassBall"


@declare_state_machine(
    ControlBall,
    PassBall,
    Transition,
    LastShoot
)
class Jyz_v4(StateMachine):
    pass