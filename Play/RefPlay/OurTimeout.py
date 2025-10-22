from Geometry import *
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Utils import buffered_condition
from Vision import *
from WorldModel import Flags, Conditions, Params, Positions

TargetPosG = CGeoPoint(-Params.pitchLength / 4, -600)
TargetPos1 = CGeoPoint(-Params.pitchLength / 4, -200)
TargetPos2 = CGeoPoint(-Params.pitchLength / 4, 200)
TargetPos3 = CGeoPoint(-Params.pitchLength / 4, 600)
TargetPos4 = CGeoPoint(-Params.pitchLength / 4 + 300, 300)
TargetPos5 = CGeoPoint(-Params.pitchLength / 4 + 600, 0)
TargetPos6 = CGeoPoint(-Params.pitchLength / 4 + 900, -300)
TargetPos7 = CGeoPoint(-Params.pitchLength / 4 + 1200, -600)
TargetPos8 = CGeoPoint(-Params.pitchLength / 4 + 1200, -200)
TargetPos9 = CGeoPoint(-Params.pitchLength / 4 + 1200, 200)
TargetPos10 = CGeoPoint(-Params.pitchLength / 4 + 1200, 600)

ACC = 2000



class Move(State):
    def transFunction(self) -> str:
        if buffered_condition(
                Player.toTargetDist("A") < 20 and
                Player.toTargetDist("L") < 20 and
                Player.toTargetDist("S") < 20 and
                Player.toTargetDist("D") < 20 and
                Player.toTargetDist("M") < 20 and
                Player.toTargetDist("G") < 20 and
                Player.toTargetDist("B") < 20 and
                Player.toTargetDist("C") < 20 and
                Player.toTargetDist("R") < 20 and
                Player.toTargetDist("F") < 20 and
                Player.toTargetDist("K") < 20,
                20, 999
        ):
            return "Move"
        if Conditions.isGameOn():
            return "exit"
        return ""

    def getMatchString(self) -> str:
        return "[LSMACBDRFK]"

    def getTasks(self) -> "dict[str, Task]":
        return {
            "K": Task(Skill.RushTo(Positions.getTimeOutPos(0), 0, ACC, Flags.allow_dss)),
            "L": Task(Skill.RushTo(Positions.getTimeOutPos(1), 0, ACC, Flags.allow_dss)),
            "S": Task(Skill.RushTo(Positions.getTimeOutPos(2), 0, ACC, Flags.allow_dss)),
            "M": Task(Skill.RushTo(Positions.getTimeOutPos(3), 0, ACC, Flags.allow_dss)),
            "D": Task(Skill.RushTo(Positions.getTimeOutPos(4), 0, ACC, Flags.allow_dss)),
            "A": Task(Skill.RushTo(Positions.getTimeOutPos(5), 0, ACC, Flags.allow_dss)),
            "B": Task(Skill.RushTo(Positions.getTimeOutPos(6), 0, ACC, Flags.allow_dss)),
            "C": Task(Skill.RushTo(Positions.getTimeOutPos(7), 0, ACC, Flags.allow_dss)),
            "R": Task(Skill.RushTo(Positions.getTimeOutPos(8), 0, ACC, Flags.allow_dss)),
            "F": Task(Skill.RushTo(Positions.getTimeOutPos(9), 0, ACC, Flags.allow_dss)),
            "G": Task(Skill.RushTo(Positions.getTimeOutPos(10), 0, ACC, Flags.allow_dss)),
        }

@declare_state_machine(
    Move
)
class OurTimeout(StateMachine):
    pass
"""

gPlayTable.CreatePlay({
    "firstState": "move",
    "move": {
        "switch": move_switch,
        "K": Task(Skill.RushTo(Positions.getTimeOutPos(0), 0, ACC, Flags.allow_dss)),
        "L": Task(Skill.RushTo(Positions.getTimeOutPos(1), 0, ACC, Flags.allow_dss)),
        "S": Task(Skill.RushTo(Positions.getTimeOutPos(2), 0, ACC, Flags.allow_dss)),
        "M": Task(Skill.RushTo(Positions.getTimeOutPos(3), 0, ACC, Flags.allow_dss)),
        "D": Task(Skill.RushTo(Positions.getTimeOutPos(4), 0, ACC, Flags.allow_dss)),
        "A": Task(Skill.RushTo(Positions.getTimeOutPos(5), 0, ACC, Flags.allow_dss)),
        "B": Task(Skill.RushTo(Positions.getTimeOutPos(6), 0, ACC, Flags.allow_dss)),
        "C": Task(Skill.RushTo(Positions.getTimeOutPos(7), 0, ACC, Flags.allow_dss)),
        "R": Task(Skill.RushTo(Positions.getTimeOutPos(8), 0, ACC, Flags.allow_dss)),
        "F": Task(Skill.RushTo(Positions.getTimeOutPos(9), 0, ACC, Flags.allow_dss)),
        "G": Task(Skill.RushTo(Positions.getTimeOutPos(10), 0, ACC, Flags.allow_dss)),
        "match": "[LSMACBDRFK]"
    },
    "name": "Ref_OurTimeout_11vs11",
    "applicable": {
        "exp": "a",
        "a": True
    },
    "attribute": "attack",
    "timeout": 99999
})
"""