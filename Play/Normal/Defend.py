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

GoalPointUp = CGeoPoint(4500, 300)
GoalPointDown = CGeoPoint(4500, -300)

class Defense(State):
    @override
    def getMatchString(self) -> str:
        return "[AB]"
    
    @override
    def getTasks(self):
        return{
            # 门将flag=1没什么区别
            # flag = 2也没什么区别
            "A": Task(Skill.Goalie(pos = (GoalPointUp if Ball.posY() < 0 else GoalPointDown), flag = 4), fixedNumber=0),
            # "B": Task(Skill.WMarking(priority = 1, num = 1)),
            # "C": Task(Skill.WMarking(priority=1, num =2))
            "B": Task(Skill.Stop())
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