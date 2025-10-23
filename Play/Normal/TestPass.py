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


class Rush(State):
    @override
    def getMatchString(self) -> str:
        return "{AB}{C}"
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        global flag 
        flag = False
        # 寻找一个合理的可传球点位
        global WAIT_POS
        # WAIT_POS = CGeoPoint(Player.posX("B") + 1000, Player.posY("B") +randint(-200, 300))# 1000后面可修改
        # WAIT_POS = CGeoPoint(Player.posX("B") + randint(- 200, 1000), Player.posY("B") +randint(-200, 300))# 1000后面可修改
        # while (WAIT_POS.x() > 3300 and WAIT_POS.y() < 1200 and WAIT_POS.y() > -1200) or (WAIT_POS.x() < -3300 and WAIT_POS.y() < 1200 and WAIT_POS.y() > -1200): # TOD: 设置一个可到达的点位（非禁区）
        #     WAIT_POS = CGeoPoint(Player.posX("B") + randint(-200, 1000), Player.posY("B") + randint(-200, 300))# 1000后面可修改
        WAIT_POS = CGeoPoint(2500 + randint(-200, 1000), 0 + randint(-2500, 2500))
        flag = True
        return {
            "A": Task(Skill.GetBall()),
            # 前一个生成随机数的范围可以改
            # -3500 - 3500 就是非禁区的区域
            # "B": Task(Skill.RushToV4(pos = (WAIT_POS := CGeoPoint(randint(-3500, 3500), randint(-Params.pitchWidth // 2, Params.pitchWidth // 2))), mydir = (WAIT_POS - Player.Pos("A")).dir())),
            "B": Task(Skill.SmartGoTo(target = WAIT_POS, dir = (WAIT_POS - Player.Pos("B")).dir())),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }
    
    @override
    def transFunction(self) -> str:
        global flag
        if flag:
            flag = False
            # return "Pass"   # v1
            return "RushWait"   # v2

    
class RushWait(State):

    @override
    def getMatchString(self) -> str:
        return "[A][B]" # TOO：还没修改
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            # "A": Task(Skill.RushTo(Ball.pos(), angle = Player.toPlayerDir("B"), maxAcc = 1, needDribble = True)), # 或者StaticGetBall, GetBall
            "A": Task(Skill.GetBall()),
            "B": Task(Skill.SmartGoTo(WAIT_POS, dir = (WAIT_POS - Player.Pos("B")).dir())),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }
    
    @override
    def transFunction(self) -> str:
        # if buffered_condition((Ball.Pos() - Player.Pos("A")).mod()< 100 and (Player.Pos("B") - WAIT_POS).mod()< 50, 5):
        if (Player.Pos("B") - WAIT_POS).mod() < 200: # 到达位置了，能传球就传球
            return "Pass(CGeoPoint(randint(0, 3500), randint(-2800, 2800)))"   # v1
                # return "PassAndGet"   # v2


class Pass(State):
    def __init__(self, passPos = CGeoPoint(0, 0)):
        self.passPos = passPos
    @override
    def getMatchString(self) -> str:
        return "{AB}{C}" # TOD:还没修改
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        # global PlayerDist
        # PlayerDist = (Player.pos("A") - Player.pos("B")).mod()
        # if PlayerDist > 5000:
        #     return {
        #         "A": Task(Skill.PassToPos(Player.Pos("B"), kickpower = PlayerDist - 1500)), # GetBestPower 不可用的话，就得自己寻找合适值
        #         "B": Task(Skill.Stop()),
        #         "C": Task(Skill.Goalie(), fixedNumber=0)
        #     }   
        # elif PlayerDist > 3000:
        #     return {
        #         "A": Task(Skill.PassToPos(Player.Pos("B"), kickpower = PlayerDist)), # GetBestPower 不可用的话，就得自己寻找合适值
        #         "B": Task(Skill.Stop()),
        #         "C": Task(Skill.Goalie(), fixedNumber=0)
        #     }   
        # elif PlayerDist > 1000:
        #     return {
        #         "A": Task(Skill.PassToPos(Player.Pos("B"), kickpower = PlayerDist + 1000)), # GetBestPower 不可用的话，就得自己寻找合适值
        #         "B": Task(Skill.Stop()),
        #         "C": Task(Skill.Goalie(), fixedNumber=0)
        #     }   
        # else:
        #     return {
        #     "A": Task(Skill.PassToPos(Player.Pos("B"), kickpower = 1000)), # GetBestPower 不可用的话，就得自己寻找合适值
        #     "B": Task(Skill.Stop()),
        #     "C": Task(Skill.Goalie(), fixedNumber=0)
        # }  
            return {
            "A": Task(Skill.PassToPos(self.passPos, kickpower = 2000)), # GetBestPower 不可用的话，就得自己寻找合适值
            "B": Task(Skill.Stop()),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        } 
    @override
    def transFunction(self) -> str:
         #理论
        global PlayerDist
        if PlayerDist > 5000:
            if (Ball.pos() - self.passPos).mod() < 2000: # 为了流畅度这个200可以调整
                return "Get"
        elif PlayerDist > 3000:
            if (Ball.pos() - self.passPos).mod() < 1500:
                return "Get"
        elif PlayerDist >= 0:
            if (Ball.pos() - self.passPos).mod() < 1000:
                return "Get"
        # # 实际
        # if (Ball.pos() - Player.pos("B")).mod() < 3000:
        #     return "Get" 
        
class Get(State):
    @override
    def getMatchString(self) -> str:
        return "{AB}{C}" # TOD:还没修改
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.Stop()), # 少用Stop
            # "A": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("A"), maxAcc = 1)),
            "B": Task(Skill.GetBall()),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }
    
    @override
    def transFunction(self) -> str:
        if (Player.pos("B") - Ball.pos()).mod() > 100:
            return "Get"
        # if Player.toTheirGoalDist("B") <= 2000: # 每个都试一下 # TODO: 射门条件也需要修改调试
        #     return "Score"
        # elif Player.toTheirGoalDist("B") > 2000:
        #     return "Rush"
        return "Score" 

class Score(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]{C}" # TOD:还没修改
    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.NormalShoot(isChip=False, power=12700)), # isChip 可以修改
            # "B": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("B"), maxAcc = 1)),
            "B": Task(Skill.Stop()),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }

    @override
    def transFunction(self) -> str:
        if Player.toBallDist("A") > 1000 and Player.toBallDist("B") >1000:
            return "Rush"   



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
    Rush,
    RushWait,
    Pass,
    Get,
    Score,
    # AllStop
)
class TestPass(StateMachine):
    pass