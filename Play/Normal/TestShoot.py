# 没有敌人状态下的无敌传球射门版本

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




# TODO: 可能要根据实际情况修改
GoalPointUp = CGeoPoint(4500, 300)
GoalPointDown = CGeoPoint(4500, -300)
# GoalPointUp = CGeoPoint(4500, 380)
# GoalPointDown = CGeoPoint(4500, -380)
# GoalPointUp = CGeoPoint(4500, 400)
# GoalPointDown = CGeoPoint(4500, -400)
# GoalPointUp = CGeoPoint(4500, 450)
# GoalPointDown = CGeoPoint(4500, -450)

class Score(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]" # TOD:还没修改
    @override
    def getTasks(self) -> "dict[str, Task]":
        if Ball.posY() < -600 or 0 < Ball.posY() < 600:
            return {
                    # "A": Task(Skill.Shoot(power = 12700)),
                    "A": Task(Skill.PassToPos(GoalPointDown, 12700)),
                    "B": Task(Skill.Stop()),
                }
        else:
            return {
                    # "A": Task(Skill.Shoot(power = 12700)),
                    "A": Task(Skill.PassToPos(GoalPointUp, 12700)),
                    "B": Task(Skill.Stop()),
                }

    @override
    def transFunction(self) -> str:
        if Player.toBallDist("A") > 1000 or Ball.isBallInBox() or Ball.isBallOutSide():
            return "AllStop"   



class AllStop(State):
    @override 
    def getMatchString(self) -> str:
        return "[AB]"

    @override 
    def getTasks(self):
        return {
            "A": Task(Skill.Stop()),
            "B": Task(Skill.Stop())
        }
    
    @override 
    def transFunction(self):
        return "AllStop"

# todo: start state
@declare_state_machine(

    Score,
    AllStop
)
class TestShoot(StateMachine):
    pass