import math

import Global
from Geometry import *
from Global import getRoleNumber
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Strategy import *
from Strategy.AttackInfomation import generateShootPoint
from Utils import buffered_condition
from Vision import *
from WorldModel import Flags, Conditions, Params, Positions, KickPower, Directions, ChipPower

UpPoint = CGeoPoint(-224/1200*Params.pitchLength,-140/900*Params.pitchWidth)
MiddlePoint = CGeoPoint(-66/1200*Params.pitchLength,0)
BelowPoint = CGeoPoint(-224/1200*Params.pitchLength,140/900*Params.pitchWidth)

class Start(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.RushTo(MiddlePoint)),
            "A": Task(Skill.RushTo(BelowPoint)),
            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return "[L][A]"

    def transFunction(self) -> str:
        if Conditions.isGameOn():
            return "exit"
        else:
            return "Start"
        
@declare_state_machine(
    Start
)
class KickOffDefend_2023(StateMachine):
    pass