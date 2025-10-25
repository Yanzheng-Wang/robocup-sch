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



# TODO: 可能要根据实际情况修改
GoalPointUp = CGeoPoint(4500, 300)
GoalPointDown = CGeoPoint(4500, -300)
# GoalPointUp = CGeoPoint(4500, 380)
# GoalPointDown = CGeoPoint(4500, -380)
# GoalPointUp = CGeoPoint(4500, 400)
# GoalPointDown = CGeoPoint(4500, -400)
# GoalPointUp = CGeoPoint(4500, 450)
# GoalPointDown = CGeoPoint(4500, -3450)


class Dribble(State):
    @override 
    def getMatchString(self) -> str:
        return "[A][B]{C}"
    
    @override
    def getTasks(self) -> dict[str, Task]:
        if Ball.posY() > 0:
            return{
                "A": Task(Skill.PassToPos(CGeoPoint(3500, 400), kickpower=2000)),
                "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
        else:
            return{
                "A": Task(Skill.PassToPos(CGeoPoint(3500, -400), kickpower=2000)),
                "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }


        # return {

        #     # !！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        #     # TODO： 实际场地测最佳的pickpower


        #     # # "A": Task(Skill.PassToPos(CGeoPoint(Player.posX("A") + 300, Player.posY("A")), kickpower = 3000)),
        #     # "A": Task(Skill.PassToPos(CGeoPoint(4500, 0), kickpower=2000)),
        #     # "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #     # "C": Task(Skill.Goalie(), fixedNumber=0)
        
        # }
    
    @override
    def transFunction(self) -> str:
        if Ball.isBallOutSide() or Ball.isBallInBox() or Enemy.isEnemyControlBall():
            return "Defense"
        if Player.isOurPlayerNearGoal("A", "B") or (Ball.posX() > 2000 and(Player.posX("A") > 1800 or Player.posX("B") > 1800)):
            return "LastShoot"

class LastShoot(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]{C}"
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        # ！！！！！！！！！！！！！！！！！！！！！！！！！
        # TODO：实际场地哪个效果好就用哪个

        if Ball.posY() < -600 or 0 < Ball.posY() < 600:
            return {
                    "A": Task(Skill.PassToPos(GoalPointDown, 12000)),
                    # "B": Task(Skill.SimpleGoTo(PostPassPosition)),
                    "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
        else:
            return {
                    "A": Task(Skill.PassToPos(GoalPointUp, 12000)),
                    # "B": Task(Skill.SimpleGoTo(PostPassPosition)),
                    "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
    
        # if Ball.posY()-100 <= Enemy.posY(0) <= Ball.posY()+100 and Ball.posY() >= 0:
        #     return {
        #     "A": Task(Skill.PassToPos(GoalPointDown, 12000)), # isChip 可以修改
        #     # "B": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("B"))),
        #     "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #     "C": Task(Skill.Goalie(), fixedNumber=0)
        # }
        # if Ball.posY()-100 <= Enemy.posY(0) <= Ball.posY()+100 and Ball.posY() <= 0:
        #     return {
        #     "A": Task(Skill.PassToPos(GoalPointUp, 12000)), # isChip 可以修改
        #     # "B": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("B"))),
        #     "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #     "C": Task(Skill.Goalie(), fixedNumber=0)
        # }
        # if Ball.posY() >= 0:
        #    return {
        #     "A": Task(Skill.PassToPos(GoalPointUp, 12000)), # isChip 可以修改
        #     # "B": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("B"))),
        #     "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #     "C": Task(Skill.Goalie(), fixedNumber=0)
        # }
        # else:
        #     return {
        #     "A": Task(Skill.PassToPos(GoalPointDown, 12000)), # isChip 可以修改
        #     # "B": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("B"))),
        #     "B": Task(Skill.WMarking(priority=1, num = Enemy.nearestToOurGoalNum())),
        #     "C": Task(Skill.Goalie(), fixedNumber=0)
        # }

    @override
    def transFunction(self) -> str:
        # if buffered_condition(Player.kickBallVision("A"), 1, 100):
        if Ball.isBallInBox() or Ball.isBallOutSide() or Player.calToBallDist("A") >1800:
            return "Dribble"


class Defense(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]{C}"
    
    @override
    def getTasks(self) -> "dict[str, Task]":
            return {

                # !！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                # TODO: NormalShoot解围的力道要根据实际情况调整


                "A": Task(Skill.NormalShoot(1000, isChip=True)),
                "B": Task(Skill.WMarking(priority=1, num=Enemy.nearestToOurGoalNum())),
                "C": Task(Skill.Goalie())
            }
    
    @override
    def transFunction(self) -> str:
        if Ball.posX() > 0 and (not Enemy.isEnemyControlBall() or Player.isOurPlayerControlBall()):
            return "Dribble"
        

# todo: start state
@declare_state_machine(
    Dribble,
    LastShoot,
    Defense
)
class NoPass(StateMachine):
    pass