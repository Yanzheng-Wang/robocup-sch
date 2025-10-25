# v10版本已经修了无数的bug了
# v11是为了修改PassBall而生

from typing import override
import Global
import Utils
from Geometry import *
from Global import debugEngine
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill, SimpleGoTo, Goalie, RushTo
from Strategy import *
from Utils import buffered_condition
from Vision import Enemy, Player, Ball
from WorldModel import Flags, Conditions, Params, Positions
from RoleMatch_LuaStyle.Skills.Skill import *


ReceivePositionUp = CGeoPoint(2500, 400)
ReceivePositionDown = CGeoPoint(2500, -400)
WaitPosition = CGeoPoint(2500, 0)
PostPassPosition = CGeoPoint(1000, 0)


# TODO： 射门Ball.posX()阈值
canShootLine = 2000          # 仿真证明2000就可以射门
# canShootLine = 2500          # 最开始的，如果使用PassToPos在现实中射门力道太小，就使用这个
# canShootLine = 1500          # 现实中突破不了敌人的防线


# TODO: 可能要根据实际情况修改
GoalPointUp = CGeoPoint(4500, 300)
GoalPointDown = CGeoPoint(4500, -300)
# GoalPointUp = CGeoPoint(4500, 380)
# GoalPointDown = CGeoPoint(4500, -380)
# GoalPointUp = CGeoPoint(4500, 400)
# GoalPointDown = CGeoPoint(4500, -400)
# GoalPointUp = CGeoPoint(4500, 450)
# GoalPointDown = CGeoPoint(4500, -450)


class ControlBall(State):
    @override
    def getMatchString(self) -> str:
        # return "[A][B]{C}"
        return "(A)(B){C}"          # 解决Defense转到ControlBall的滑动问题

    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            # "A": Task(Skill.GetBall()), 
            "A": Task(Skill.RushTo(Ball.pos(), Player.toBallDir("A"), needDribble=True)),
            # "B": Task(Skill.RushTo(WaitPosition, angle=Player.toBallDir("B"))),
            "B": Task(Skill.WMarking(priority=1, num=Enemy.nearestToOurGoalNum())),

            # =========================================================
            # TODO:


            # "C": Task(Skill.Goalie(pos = (GoalPointUp if Ball.posY() < 0 else GoalPointDown)), fixedNumber=0), # 用于打反角
            "C": Task(Skill.Goalie(), fixedNumber=0)

            # +============————————————————————————————————++++++++++++++++++++++++++++++++
        }

    @override
    def transFunction(self) -> str:
        # TODO： 感觉仿真大于2000就可以直接射门了
        if Ball.posX() > canShootLine and (Player.posX("A") > canShootLine - 200 or Player.posX("B") > canShootLine - 200):
            return "LastShoot"
        if Player.calToBallDist("A") < 200:
            return "PassBall"
        else:
            return "ControlBall"
        
class PassBall(State):
    @override
    def getMatchString(self) -> str:
        # return "[A][B]{C}"
        return "(A)(B){C}"              # FIXEME： 用于解决PassBall的时候一直切换状态导致的抖动
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        


        # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        # TODO： 实际场地的力度可能要加1000？


        # 后场射门，前场挑传？
        
        if Ball.posY() > 0 and Ball.posX() < 500:
                return {
                    # "A": Task(Skill.PassToPos(GoalPointDown, 9000)),
                    "A": Task(Skill.NormalShoot(500, isChip=True)),
                    "B": Task(Skill.RushTo(ReceivePositionUp, Player.toBallDir("B"))),
                    # "B": Task(Skill.SimpleGoTo(ReceivePositionUp)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
        elif Ball.posY() <= 0 and Ball.posX() < 500:
                return {
                    # "A": Task(Skill.PassToPos(GoalPointUp, 9000)),
                    "A": Task(Skill.NormalShoot(500, isChip=True)),
                    "B": Task(Skill.RushTo(ReceivePositionDown, Player.toBallDir("B"))),
                    # "B": Task(Skill.SimpleGoTo(ReceivePositionDown)),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }
        else:
            return {
                "A": Task(Skill.NormalShoot(12700, isChip = False)),
                "B": Task(Skill.RushTo((ReceivePositionDown if Ball.posY() < 0 else ReceivePositionUp), angle = Player.toBallDir("B"))),
                "C": Task(Skill.Goalie(), fixedNumber=0),

            }
        
    @override
    def transFunction(self) -> str:
        if Ball.posX() > canShootLine and (Player.posX("A") > canShootLine - 200 or Player.posX("B") > canShootLine - 200):
            return "LastShoot"
        
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        # TODO: 明天如果             Dribble Too Far               解注释
        # if buffered_condition(Player.calToBallDist("A") < 200, 5, 100):
        #     return "LastShoot"

        # ====================-----------------------------------+++++++++++++++++++++++++====

        if Ball.isBallInBox() or Ball.isBallOutSide() or Player.isOurPlayerLoseBall(): # 不该再加上球在我们半场内吗
            return "Defense"
        else:
            return "PassBall"
        
class LastShoot(State):
    @override
    def getMatchString(self) -> str:
        return "[A][B]{C}"
        # return "{A}{B}{C}"
    
    @override
    def getTasks(self) -> "dict[str, Task]":
        # ！！！！！！！！！！！！！！！！！！！！！！！！！
        # TODO：实际场地哪个效果好就用哪个

        # 如果真的力道，又没有其他替代办法
        return {
                    # "A": Task(Skill.Shoot(power = 12700)),
                    "A": Task(Skill.NormalShoot(12700, False)),
                    "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                    "C": Task(Skill.Goalie(), fixedNumber=0)
                }

        # 因为实地passTopos力道很小，故使用Shoot TODO:测试
        # if Ball.posY() < -600 or 0 < Ball.posY() < 600:
        #     return {
        #             # "A": Task(Skill.Shoot(power = 12700)),
        #             "A": Task(Skill.PassToPos(GoalPointDown, 12700)),
        #             "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #             "C": Task(Skill.Goalie(), fixedNumber=0)
        #         }
        # else:
        #     return {
        #             # "A": Task(Skill.Shoot(power = 12700)),
        #             "A": Task(Skill.PassToPos(GoalPointUp, 12700)),
        #             "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #             "C": Task(Skill.Goalie(), fixedNumber=0)
        #         }
        
        # TODO: 射门两套逻辑
        ##### 出现在y = 0不移动门将
        # if Ball.posY() < 0:
        #     return {
        #             # "A": Task(Skill.Shoot(power = 12700)),
        #             "A": Task(Skill.PassToPos(GoalPointDown, 12700)),
        #             "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #             "C": Task(Skill.Goalie(), fixedNumber=0)
        #         }
        # else:
        #     return {
        #             # "A": Task(Skill.Shoot(power = 12700)),
        #             "A": Task(Skill.PassToPos(GoalPointUp, 12700)),
        #             "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
        #             "C": Task(Skill.Goalie(), fixedNumber=0)
        #         }

    
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
        # if buffered_condition(Player.kickBallVision("A"), 2, 100):
        if Ball.isBallInBox() or Ball.isBallOutSide() or Player.calToBallDist("A") >1800:
            return "Defense"
        else:
            return "LastShoot"
        
class Defense(State):
    @override
    def getMatchString(self) -> str:
        # return "[A][B]{C}"
        return "(A)(B){C}"

    @override
    def getTasks(self) -> "dict[str, Task]":
        if Ball.posX() < 0: # 球在本方半场
            return {
                "A": Task(Skill.NormalShoot(700, isChip=True)),
                "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                # "B": Task(Skill.GetBall()),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
        else:
            return {
                # "A": Task(Skill.SimpleGoTo(Ball.pos())),
                "A": Task(Skill.GetBall()),
                "B": Task(Skill.WMarking(priority = 1, num = Enemy.nearestToOurGoalNum())),
                # "B": Task(Skill.GetBall()),
                "C": Task(Skill.Goalie(), fixedNumber=0)
            }
    
    @override
    def transFunction(self) -> str:
        if Ball.posX() > canShootLine and (Player.posX("A") > canShootLine - 200 or Player.posX("B") > canShootLine - 200):
            return "LastShoot"
        if not Ball.isBallInBox() and not Ball.isBallOutSide() and Player.isOurPlayerControlBall():
            if abs(Player.pos("A").x() - 2500) < 500: # 位置很好，直接补射
                return "LastShoot"
            else:
                return "ControlBall"
        else:
            return "Defense"
        
@declare_state_machine(
    ControlBall,
    PassBall,
    LastShoot,
    Defense
)
class Jyz_v12(StateMachine):
    pass
