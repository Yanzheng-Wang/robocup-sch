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

# 一个人跑位一个拿球

# 能传球传球， 不能传球，再跑位
# 传球的时候，一个人传球，一个人等待，
# 然后一个人等待， 一个人拿球，拿球后即判断是否能射门

# 能射门射门，不能射门再跑位


class Rush(State):
    @override
    def getMatchString(self) -> str:
        return "{C}{A}{B}"
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        # 寻找一个合理的可传球点位
        global WAIT_POS
        # WAIT_POS = CGeoPoint(Player.posX("B") + 1000, Player.posY("B") +randint(-200, 300))# 1000后面可修改
        # WAIT_POS = CGeoPoint(Player.posX("B") + randint(- 200, 1000), Player.posY("B") +randint(-200, 300))# 1000后面可修改
        # while (WAIT_POS.x() > 3300 and WAIT_POS.y() < 1200 and WAIT_POS.y() > -1200) or (WAIT_POS.x() < -3300 and WAIT_POS.y() < 1200 and WAIT_POS.y() > -1200): # TOD: 设置一个可到达的点位（非禁区）
        #     WAIT_POS = CGeoPoint(Player.posX("B") + randint(-200, 1000), Player.posY("B") + randint(-200, 300))# 1000后面可修改
        WAIT_POS = CGeoPoint(2500 + randint(-200, 1000), 0 + randint(-2500, 2500))
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
        if Player.canFlatPassTo("A", "B") and (Player.Pos("B") - WAIT_POS).mod()== 0:
            # return "Pass"   # v1
            return "Pass"   # v2
        else:
            return "RushWait"
    
class RushWait(State):

    @override
    def getMatchString(self) -> str:
        return "{C}{A}{B}" # TOO：还没修改
    
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
        if (Player.Pos("B") - WAIT_POS).mod() < 200 and Player.canFlatPassTo("A", "B"): # 到达位置了，能传球就传球
            return "Pass"   # v1
                # return "PassAndGet"   # v2
        
# 一个人静止等球一个人传球
# TODO: 可以添加提前量来提高上限
# v1
class Pass(State):
    @override
    def getMatchString(self) -> str:
        return "{C}[AB]" # TOD:还没修改
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.PassToPos(Player.Pos("B"), kickpower = 2000)), # GetBestPower 不可用的话，就得自己寻找合适值
            # "B": Task(Skill.Stop()),
            "B": Task(Skill.RushTo(Player.Pos("A"), angle = Player.toPlayerDir("A"), maxAcc = 1)),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        } 

    @override
    def transFunction(self) -> str:
        # 这里maybe有问题，就是当球传出去的时候，他会先 卡一段时间，就是卡在"Pass"这个状态
        # 不知道这个PassToPos有没有自己去拿球的功能，就更NormalShoot一样的
        if (Player.Pos("A") - Ball.Pos()).mod() > 300: # 为了流畅度这个200可以调整
            return "Get"
        else:
            return "RushWait"
    

# 一个人传球一个人去拿球
# v2
# TODO: 还没改
class PassAndGet(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]" # TODO:还没修改
    
    @override 
    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.PassToPos(Player.Pos("B"))),
            "B": Task(Skill.GetBallV5(direction = Player.toBallDir("B"))), # toBallDir("B")不行的话改成toBallDir("A")
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }
    
    @override
    def transFunction(self) -> str:
        if (Player.Pos("B") - Ball.Pos()).mod() > 100: # 为了流畅度这个200可以调整
            return "Get"
        elif Player.canshoot("B") and Player.toTheirGoalDist("B") < 2000: # 
        # if (Player.Pos("B") - Ball.Pos()).mod() < 100 and Player.canDirectShoot("B"):
        # if (Player.Pos("B") - Ball.Pos()).mod() < 100 and Player.toTheirGoalDist("B") <2000:
        # if (Player.Pos("B") - Ball.Pos()).mod() < 100 and Player.toTheirGoalLineDistMin("B"):
            return "Score"
        else:
            return "Rush"

class Get(State):
    @override
    def getMatchString(self) -> str:
        return "{C}[B][A]" # TOD:还没修改
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            # "A": Task(Skill.Stop()), # 少用Stop
            "A": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("A"), maxAcc = 1)),
            "B": Task(Skill.GetBall()),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }
    
    @override
    def transFunction(self) -> str:
        if (Player.Pos("B") - Ball.Pos()).mod() > 1000: # 每个都试一下
            return "Get"
        if Player.canshoot("B") and Player.toTheirGoalDist("B") <= 2000: # 每个都试一下 # TODO: 射门条件也需要修改调试
            return "Score"
        else:
            return "Rush"

class Score(State):
    @override
    def getMatchString(self) -> str:
        return "{C}[A][B]" # TOD:还没修改
    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.NormalShoot(isChip=False, power=12700)), # isChip 可以修改
            "B": Task(Skill.RushTo(Ball.pos(), angle = Player.toBallDir("B"), maxAcc = 1)),
            # "B": Task(Skill.Stop()),
            "C": Task(Skill.Goalie(), fixedNumber=0)
        }

    @override
    def transFunction(self) -> str:
        return "Rush"


# todo: start state
@declare_state_machine(
    Rush,
    RushWait,
    Pass, # v1
    # PassAndGet, # v2
    Get,
    Score,
)
class NormalPlay_3vs3_wyz(StateMachine):
    pass