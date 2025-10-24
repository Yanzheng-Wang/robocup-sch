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
from WorldModel import Params
from random import randint

class RushToStop(State):
    @override 
    def getMatchString(self) -> str:
        return "[A][B][C]"
    
    @override 
    def getTasks(self):
        return {
            "A": Task(Skill.RushTo(Ball.pos(), Player.toBallDir("A"), maxAcc=1)),
            "B": Task(Skill.RushTo(Ball.pos(), Player.toBallDir("B"), maxAcc=1)),
            "C": Task(Skill.RushTo(Ball.pos(), Player.toBallDir("C"), maxAcc=1))
        }
    
    @override 
    def transFunction(self):
        return "RushToStop"



# todo: start state
@declare_state_machine(
    RushToStop
)
class TestRushTo(StateMachine):
    pass