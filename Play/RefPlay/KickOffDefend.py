from Geometry import *
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Vision import *
from Vision import Enemy
from WorldModel import Flags, Conditions, Params, Positions


def Leftpos():
    for i in range(Params.maxPlayer):
        if Enemy.valid(i):
            if Enemy.posX(i) < 500:
                if Enemy.posY(i) < -1000:
                    return Enemy.pos(i)
    return CGeoPoint(150, -Params.pitchWidth / 4 - 500)

def Rightpos():
    for i in range(Params.maxPlayer):
        if Enemy.valid(i):
            if Enemy.posX(i) < 500:
                if Enemy.posY(i) > 1000:
                    return Enemy.pos(i)
    return CGeoPoint(150, Params.pitchWidth / 4 + 500)

SIDE_POS, MIDDLE_POS, INTER_POS, SIDE2_POS, INTER2_POS = Positions.refStopAroundBall()

def OTHER_POS():
    leftnum = 0
    rightnum = 0
    for i in range(Params.maxPlayer):
        if Enemy.valid(i):
            if Enemy.posY(i) > 0:
                rightnum += 1
            else:
                leftnum += 1
    if rightnum > leftnum:
        return CGeoPoint(-500, Params.pitchWidth / 4)
    else:
        return CGeoPoint(-500, -Params.pitchWidth / 4)

DSS_FLAG = Flags.allow_dss

def play_switch():
    if Conditions.isGameOn():
        return "exit"
    return ""


class Start(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "L": Task(Skill.SmartGoTo(MIDDLE_POS, Player.toBallDir("L"), DSS_FLAG)),
            "S": Task(Skill.Marking(Leftpos())),
            "A": Task(Skill.Marking(Rightpos())),
            "B": Task(Skill.SmartGoTo(INTER2_POS, Player.toBallDir("B"), DSS_FLAG)),
            "R": Task(Skill.SmartGoTo(SIDE2_POS, Player.toBallDir("R"), DSS_FLAG)),
            "K": Task(Skill.SmartGoTo(OTHER_POS(), Player.toBallDir("K"), DSS_FLAG)),
            "M": Task(Skill.WBack(4, 1)),
            "D": Task(Skill.WBack(4, 2)),
            "C": Task(Skill.WBack(4, 3)),
            "F": Task(Skill.WBack(4, 4)),
            "G": Task(Skill.Goalie()),
        }

    def getMatchString(self) -> str:
        return "(L)(AS)(DCFM)(BRK)"

    def transFunction(self) -> str:
        return play_switch()

@declare_state_machine(
    Start
)
class KickOffDefend(StateMachine):
    pass