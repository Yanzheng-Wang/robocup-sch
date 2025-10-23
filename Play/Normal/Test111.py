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

WAIT_POS: CGeoPoint
flag: bool
receive_ball_range = 100
PlayerDist = (Player.pos("A") - Player.pos("B")).mod()

# 一个人跑位一个拿球

# 能传球传球， 不能传球，再跑位
# 传球的时候，一个人传球，一个人等待，
# 然后一个人等待， 一个人拿球，拿球后即判断是否能射门

# 能射门射门，不能射门再跑位




class Defense(State):
    @override
    def getMatchString(self) -> str:
        return "[B][A]{C}" # TOD:还没修改
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())), # 盯没拿球的人
            "B": Task(Skill.NormalShoot(power = 12700, isChip = False)),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }
    
    @override
    def transFunction(self) -> str:
        if not Enemy.isEnemyControlBall():
            return "Defense"
        return "AllStop"


class AllStop(State):
    @override 
    def getMatchString(self) -> str:
        return "[ABC]"

    @override 
    def getTasks(self):
        return {
            "A": Task(Skill.Stop()),
            "B": Task(Skill.Stop()),
            "C": Task(Skill.Stop())
        }
    
    @override 
    def transFunction(self):
        # if Enemy.isEnemyControlBall():
        #     return "Defense"
        return "AllStop"

# todo: start state
@declare_state_machine(
    Defense,
    AllStop
)
class Test111(StateMachine):
    pass