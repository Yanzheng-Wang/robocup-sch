import math

import Global
from Geometry import *
from Global import getRoleNumber
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Strategy import *
from Strategy.AttackInfomation import generateShootPoint
from Utils import buffered_condition
from Utils import Polar2Vector
from Vision import *
from WorldModel import Flags, Conditions, Params, Positions, KickPower, Directions, ChipPower

START_POS = CGeoPoint(27/1200 * Params.pitchLength, 0)
START_POS_1 = CGeoPoint(27/1200*Params.pitchLength, 18/900*Params.pitchWidth)
START_POS_2 = CGeoPoint(27/1200*Params.pitchLength, -18/900*Params.pitchWidth)
RECEIVE_POS_1 = CGeoPoint(-110/1200*Params.pitchLength, -70/900*Params.pitchWidth)
RECEIVE_POS_2 = CGeoPoint(-110/1200*Params.pitchLength, 70/900*Params.pitchWidth)

def passForTouch(pos):
    return pos + Polar2Vector(99.6, Directions.posToTheirGoal(pos))

class Start(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.RushTo(START_POS,math.pi,flag=Flags.allow_dss)),
            "A": Task(Skill.RushTo(RECEIVE_POS_1, Player.toBallDir('A'), flag=Flags.allow_dss)),
            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return "{L}[A]"

    def transFunction(self) -> str:
        if Conditions.isNormalStart():
            return "Adjust"
        else:
            return "Start"
        
class Adjust(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.RushTo(START_POS_1,Player.toBallDir('L'),flag=Flags.allow_dss)),
            "A": Task(Skill.RushTo(RECEIVE_POS_1, Player.toBallDir('A'), flag=Flags.allow_dss)),
            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return "{L}[A]"

    def transFunction(self) -> str:
        if buffered_condition(Player.toTargetDist('L') < 100, 5, 100):
            return "GetBall"
        else:
            return "Adjust"
        
class GetBall(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.StaticGetBallV4(passForTouch(RECEIVE_POS_1))),
            "A": Task(Skill.RushTo(RECEIVE_POS_1, Player.toBallDir('A'), flag=Flags.allow_dss)),
            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return "{L}[A]"

    def transFunction(self) -> str:
        if buffered_condition(Player.toTargetDist('L') < 50, 70, 100):
            return "KickOff"
        else:
            return "GetBall"
        
class KickOff(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.PassToPos(RECEIVE_POS_1, kickpower=6000)),
            "A": Task(Skill.RushTo(RECEIVE_POS_1, Player.toBallDir('A'), flag=Flags.allow_dss)),
            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return "{L}[A]"

    def transFunction(self) -> str:
        if buffered_condition(Player.kickBall("L"), 10, 200):
            return "Receive"
        else:
            return "KickOff"
        
class Receive(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.WMarking(priority=0,num=defenceSequence.getAttackNum(0))),
            "A": Task(Skill.GetBallV5(Player.toBallDir('A'))),
            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return "{L}[A]"

    def transFunction(self) -> str:
        if buffered_condition(Ball.toPlayerHeadDist("A") < 200, 10, 150):
            return "exit"
        else:
            return "Receive"
        
@declare_state_machine(
    Start,
    Adjust,
    GetBall,
    KickOff,
    Receive
)
class KickOff_2023(StateMachine):
    pass
