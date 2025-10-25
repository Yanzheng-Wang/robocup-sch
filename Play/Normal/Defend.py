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
from random import randint

GoalPointUp = CGeoPoint(4500, 300)
GoalPointDown = CGeoPoint(4500, -300)

# class Defense(State):
#     @override
#     def getMatchString(self) -> str:
#         return "[AB]"
    
#     @override
#     def getTasks(self):
#         return{
#             "A": Task(Skill.WMarking(priority = 1, num = 1)),
#             "B": Task(Skill.WMarking(priority = 1, num = 2)),
#             # 门将flag=1没什么区别
#             # flag = 2也没什么区别
#             "C": Task(Skill.Goalie(pos = (GoalPointUp if Ball.posY() < 0 else GoalPointDown), flag = 4), fixedNumber=0),
#             # "B": Task(Skill.Stop())
#         }
    
#     @override
#     def transFunction(self):
#         return "Defense"
    

class Destroy(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]{C}"
    
    @override
    def getTasks(self) -> dict[str, Task]:
        return{
            "A": Task(Skill.NormalShoot(12700, True if randint(0, 1) else False)),
            "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
            "C": Task(Skill.Goalie(pos = (GoalPointUp if Ball.posY() < 0 else GoalPointDown), flag = 4), fixedNumber=0),

        }
    
    @override
    def transFunction(self) -> str:
        return "Destroy"
# todo: start state
@declare_state_machine(
    Destroy
)
class Defend(StateMachine):
    pass