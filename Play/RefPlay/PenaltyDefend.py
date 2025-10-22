import Global
from Geometry import *
from Global import debugEngine
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Utils import buffered_condition
from Vision import *
from WorldModel import Flags, Conditions, Params

STOP_FLAG = Flags.slowly | Flags.dodge_ball
STOP_DSS = STOP_FLAG | Flags.allow_dss
ACC = 2000

DEFX = Params.pitchLength / 2 - Params.penaltyDepth - 3 * Params.playerRadius - 300
DEFY = Params.penaltyWidth / 2 + 3 * Params.playerRadius - 50
GOALIEX = -Params.pitchLength / 2 + Params.playerRadius * 2
GOALIEY = 0

DEF_POS1 = Ball.refSyntYPos(CGeoPoint(DEFX, 500 * 5))
DEF_POS2 = Ball.refSyntYPos(CGeoPoint(DEFX, 500 * 4))
DEF_POS3 = Ball.refAntiYPos(CGeoPoint(DEFX, 500 * 3))
DEF_POS4 = Ball.refSyntYPos(CGeoPoint(DEFX, 500 * 2))
DEF_POS5 = Ball.refAntiYPos(CGeoPoint(DEFX, 500 * 1))
DEF_POS6 = Ball.refAntiYPos(CGeoPoint(DEFX, -500 * 1))
DEF_POS7 = Ball.refSyntYPos(CGeoPoint(DEFX, -500 * 2))
DEF_POS8 = Ball.refAntiYPos(CGeoPoint(DEFX, -500 * 3))
DEF_POS9 = Ball.refSyntYPos(CGeoPoint(DEFX, -500 * 4))
DEF_POS10 = Ball.refSyntYPos(CGeoPoint(DEFX, -500 * 5))

class Ready(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "D": Task(Skill.RushTo(DEF_POS1, 0, ACC, STOP_DSS)),
            "M": Task(Skill.RushTo(DEF_POS2, 0, ACC, STOP_DSS)),
            "S": Task(Skill.RushTo(DEF_POS3, 0, ACC, STOP_DSS)),
            "L": Task(Skill.RushTo(DEF_POS4, 0, ACC, STOP_DSS)),
            "A": Task(Skill.RushTo(DEF_POS5, 0, ACC, STOP_DSS)),
            "B": Task(Skill.RushTo(DEF_POS6, 0, ACC, STOP_DSS)),
            "R": Task(Skill.RushTo(DEF_POS7, 0, ACC, STOP_DSS)),
            "K": Task(Skill.RushTo(DEF_POS8, 0, ACC, STOP_DSS)),
            "F": Task(Skill.RushTo(DEF_POS9, 0, ACC, STOP_DSS)),
            "C": Task(Skill.RushTo(DEF_POS10, 0, ACC, STOP_DSS)),
            "G": Task(Skill.PenaltyGoalie()),
        }

    def getMatchString(self) -> str:
        return "[LASMDBRKFC]"

    def transFunction(self) -> str:
        debugEngine.gui_debug_arc(Ball.pos(), 500, 0, 360, 1)
        if Conditions.isNormalStart() and buffered_condition(Ball.velMod() > 500, 10):
            return "GetBall"
        return ""
        # if Conditions.isGameOn():
        #     return "exit"

class Go(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "D": Task(Skill.RushTo(DEF_POS1, 0, ACC, STOP_DSS)),
            "M": Task(Skill.RushTo(DEF_POS2, 0, ACC, STOP_DSS)),
            "S": Task(Skill.RushTo(DEF_POS3, 0, ACC, STOP_DSS)),
            "L": Task(Skill.RushTo(DEF_POS4, 0, ACC, STOP_DSS)),
            "A": Task(Skill.RushTo(DEF_POS5, 0, ACC, STOP_DSS)),
            "B": Task(Skill.RushTo(DEF_POS6, 0, ACC, STOP_DSS)),
            "R": Task(Skill.RushTo(DEF_POS7, 0, ACC, STOP_DSS)),
            "K": Task(Skill.RushTo(DEF_POS8, 0, ACC, STOP_DSS)),
            "F": Task(Skill.RushTo(DEF_POS9, 0, ACC, STOP_DSS)),
            "C": Task(Skill.RushTo(DEF_POS10, 0, ACC, STOP_DSS)),
            "G": Task(Skill.PenaltyGoalie()),
        }

    def getMatchString(self) -> str:
        return "[LASMDBRKFC]"

    def transFunction(self) -> str:
        debugEngine.gui_debug_arc(Ball.pos(), 500, 0, 360, 1)
        # if Conditions.isGameOn():
        #     return "exit"
        return ""

class GetBall(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "D": Task(Skill.RushTo(DEF_POS1, 0, ACC, STOP_DSS)),
            "M": Task(Skill.RushTo(DEF_POS2, 0, ACC, STOP_DSS)),
            "S": Task(Skill.RushTo(DEF_POS3, 0, ACC, STOP_DSS)),
            "L": Task(Skill.RushTo(DEF_POS4, 0, ACC, STOP_DSS)),
            "A": Task(Skill.RushTo(DEF_POS5, 0, ACC, STOP_DSS)),
            "B": Task(Skill.RushTo(DEF_POS6, 0, ACC, STOP_DSS)),
            "R": Task(Skill.RushTo(DEF_POS7, 0, ACC, STOP_DSS)),
            "K": Task(Skill.RushTo(DEF_POS8, 0, ACC, STOP_DSS)),
            "F": Task(Skill.RushTo(DEF_POS9, 0, ACC, STOP_DSS)),
            "C": Task(Skill.RushTo(DEF_POS10, 0, ACC, STOP_DSS)),
            "G": Task(Skill.RushTo(CGeoPoint(-4000, 0))),
        }

    def getMatchString(self) -> str:
        return ""

    def transFunction(self) -> str:
        # debugEngine.gui_debug_arc(Ball.pos(), 500, 0, 360, 1)
        if (Player.pos("Goalie") - CGeoPoint(-4000, 0)).mod() < 50:
            return "TouchBall"
        return ""


class TouchBall(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "D": Task(Skill.RushTo(DEF_POS1, 0, ACC, STOP_DSS)),
            "M": Task(Skill.RushTo(DEF_POS2, 0, ACC, STOP_DSS)),
            "S": Task(Skill.RushTo(DEF_POS3, 0, ACC, STOP_DSS)),
            "L": Task(Skill.RushTo(DEF_POS4, 0, ACC, STOP_DSS)),
            "A": Task(Skill.RushTo(DEF_POS5, 0, ACC, STOP_DSS)),
            "B": Task(Skill.RushTo(DEF_POS6, 0, ACC, STOP_DSS)),
            "R": Task(Skill.RushTo(DEF_POS7, 0, ACC, STOP_DSS)),
            "K": Task(Skill.RushTo(DEF_POS8, 0, ACC, STOP_DSS)),
            "F": Task(Skill.RushTo(DEF_POS9, 0, ACC, STOP_DSS)),
            "C": Task(Skill.RushTo(DEF_POS10, 0, ACC, STOP_DSS)),
            "G": Task(Skill.RushTo(Ball.pos(), Player.toBallDir(Global.goalieNumber))),
        }

    def getMatchString(self) -> str:
        return ""

    def transFunction(self) -> str:
        debugEngine.gui_debug_arc(Ball.pos(), 500, 0, 360, 1)
        # if Conditions.isGameOn():
        #     return "exit"
        return ""

@declare_state_machine(
    Ready,
    Go,
    GetBall,
    TouchBall
)
class PenaltyDefend(StateMachine):
    pass
"""
gPlayTable.CreatePlay({
    "firstState": "Ready",

    "Ready": {
        "switch": switch_Ready,
        "Defender": task.goCmuRush(DEF_POS1, 0, ACC, STOP_DSS),
        "Middle":   task.goCmuRush(DEF_POS2, 0, ACC, STOP_DSS),
        "Special":  task.goCmuRush(DEF_POS3, 0, ACC, STOP_DSS),
        "Leader":   task.goCmuRush(DEF_POS4, 0, ACC, STOP_DSS),
        "Assister": task.goCmuRush(DEF_POS5, 0, ACC, STOP_DSS),
        "Breaker":  task.goCmuRush(DEF_POS6, 0, ACC, STOP_DSS),
        "Receiver": task.goCmuRush(DEF_POS7, 0, ACC, STOP_DSS),
        "Kicker":   task.goCmuRush(DEF_POS8, 0, ACC, STOP_DSS),
        "Fronter":  task.goCmuRush(DEF_POS9, 0, ACC, STOP_DSS),
        "Center":   task.goCmuRush(DEF_POS10, 0, ACC, STOP_DSS),
        "Goalie":   Task(Skill.Penaltygoalie()),
        "match": "[LASMDBRKFC]"
    },

    "Go": {
        "switch": switch_Go,
        "Defender": task.goCmuRush(DEF_POS1, 0, ACC, STOP_DSS),
        "Middle":   task.goCmuRush(DEF_POS2, 0, ACC, STOP_DSS),
        "Special":  task.goCmuRush(DEF_POS3, 0, ACC, STOP_DSS),
        "Leader":   task.goCmuRush(DEF_POS4, 0, ACC, STOP_DSS),
        "Assister": task.goCmuRush(DEF_POS5, 0, ACC, STOP_DSS),
        "Breaker":  task.goCmuRush(DEF_POS6, 0, ACC, STOP_DSS),
        "Receiver": task.goCmuRush(DEF_POS7, 0, ACC, STOP_DSS),
        "Kicker":   task.goCmuRush(DEF_POS8, 0, ACC, STOP_DSS),
        "Fronter":  task.goCmuRush(DEF_POS9, 0, ACC, STOP_DSS),
        "Center":   task.goCmuRush(DEF_POS10, 0, ACC, STOP_DSS),
        "Goalie":   Task(Skill.Penaltygoalie()),
        "match": "[LASMDBRKFC]"
    },

    "getBall": {
        "switch": switch_getBall,
        "Defender": task.goCmuRush(DEF_POS1, 0, ACC, STOP_DSS),
        "Middle":   task.goCmuRush(DEF_POS2, 0, ACC, STOP_DSS),
        "Special":  task.goCmuRush(DEF_POS3, 0, ACC, STOP_DSS),
        "Leader":   task.goCmuRush(DEF_POS4, 0, ACC, STOP_DSS),
        "Assister": task.goCmuRush(DEF_POS5, 0, ACC, STOP_DSS),
        "Breaker":  task.goCmuRush(DEF_POS6, 0, ACC, STOP_DSS),
        "Receiver": task.goCmuRush(DEF_POS7, 0, ACC, STOP_DSS),
        "Kicker":   task.goCmuRush(DEF_POS8, 0, ACC, STOP_DSS),
        "Fronter":  task.goCmuRush(DEF_POS9, 0, ACC, STOP_DSS),
        "Center":   task.goCmuRush(DEF_POS10, 0, ACC, STOP_DSS),
        "Goalie":   task.goCmuRush(CGeoPoint(-4000, 0)), # task.goCmuRush((Ball.pos().x()+goaliePos().x())/2, (Ball.pos().y()+goaliePos().y())/2), Player.toBallDir),
        "match": ""
    },

    "touchBall": {
        "switch": switch_touchBall,
        "Defender": task.goCmuRush(DEF_POS1, 0, ACC, STOP_DSS),
        "Middle":   task.goCmuRush(DEF_POS2, 0, ACC, STOP_DSS),
        "Special":  task.goCmuRush(DEF_POS3, 0, ACC, STOP_DSS),
        "Leader":   task.goCmuRush(DEF_POS4, 0, ACC, STOP_DSS),
        "Assister": task.goCmuRush(DEF_POS5, 0, ACC, STOP_DSS),
        "Breaker":  task.goCmuRush(DEF_POS6, 0, ACC, STOP_DSS),
        "Receiver": task.goCmuRush(DEF_POS7, 0, ACC, STOP_DSS),
        "Kicker":   task.goCmuRush(DEF_POS8, 0, ACC, STOP_DSS),
        "Fronter":  task.goCmuRush(DEF_POS9, 0, ACC, STOP_DSS),
        "Center":   task.goCmuRush(DEF_POS10, 0, ACC, STOP_DSS),
        "Goalie":   task.goCmuRush(Ball.pos, Player.toBallDir),
        "match": ""
    },

    "name": "Ref_PenaltyDef_11vs11",
    "applicable": {
        "exp": "a",
        "a": True
    },
    "attribute": "attack",
    "timeout": 99999
})
"""
