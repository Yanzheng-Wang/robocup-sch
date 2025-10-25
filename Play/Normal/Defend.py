import math
from typing import override

import Global
import Utils
from Geometry import *
from Global import debugEngine
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill, SimpleGoTo, Goalie, RushTo
from Strategy import *
from Utils import buffered_condition
from Vision import *
from Vision import Enemy
from WorldModel import Flags, Conditions, Params, Positions
from RoleMatch_LuaStyle.Skills.Skill import *

class Defense(State):
    @override
    def getMatchString(self) -> str:
        return "[ABC]"
    
    @override
    def getTasks(self):
        return{
            "A": Task(Skill.Goalie()),
            "B": Task(Skill.WMarking(priority = 1, num = 1)),
            "C": Task(Skill.WMarking(priority=1, num =2))
        }
    
    @override
    def transFunction(self):
        return "Defense"
# todo: start state
@declare_state_machine(
    Defense,
)
class Defend(StateMachine):
    pass