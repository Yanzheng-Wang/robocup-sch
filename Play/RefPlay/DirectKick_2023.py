from CppPackage import getPosModulePos
from Geometry import *
from Global import debugEngine
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Strategy import *
from Vision import *
from Vision import Enemy
from WorldModel import Flags, Conditions, Params, Positions, Directions
import Global
from Utils import buffered_condition
import math


SHOOT_POS = Ball.antiYPos(CGeoPoint(350/1200*Params.pitchLength,150/900 * Params.pitchWidth))

kick_flag = Flags.force_kick

def ReceivePos():
    if (Ball.posX() > -100/1200*Params.pitchLength):
        return CGeoPoint(SHOOT_POS.x() + 200 * math.cos(Ball.toPointDir(SHOOT_POS)), SHOOT_POS.y() + 200 * math.sin(Ball.toPointDir(SHOOT_POS)))
    else:
        return CGeoPoint(SHOOT_POS.x() + 200 * math.cos(Ball.toPointDir(SHOOT_POS) + Ball.antiY()*math.pi/4), SHOOT_POS.y() + 200 * math.sin(Ball.toPointDir(SHOOT_POS) + Ball.antiY()*math.pi/4))

def WaitBallPos1():
    return CGeoPoint(Ball.posX() + 500 * math.cos(-Ball.antiY()*math.pi*3/4), Ball.posY() + 500 * math.sin(-Ball.antiY()*math.pi*3/4))

def WaitBallPos2():
    return CGeoPoint(Ball.posX() + 500 * math.cos(math.pi + Ball.toPointDir(SHOOT_POS)), Ball.posY() + 500 * math.sin(math.pi + Ball.toPointDir(SHOOT_POS)))
    
def KickPower(pos):
    kick_power = Ball.toPointDist(pos)/1.5
    return kick_power

class ToBall1(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.RushTo(WaitBallPos1(),Player.toPointDir(SHOOT_POS), flag = Flags.dodge_ball)),
            "L": Task(Skill.RushTo(ReceivePos(), Player.toPlayerHeadDir('A'), flag = Flags.dodge_ball)),
            "G": Task(Skill.Goalie()),
        }

    def getMatchString(self) -> str:
        return "{A}[L]"

    def transFunction(self) -> str:
        if buffered_condition(Player.toTargetDist('L')<50, 10, 180):
            return "ToBall2"
        return "ToBall1"
    
class ToBall2(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.RushTo(WaitBallPos2(),Player.toPointDir(SHOOT_POS), flag = Flags.dodge_ball)),
            "L": Task(Skill.RushTo(ReceivePos(), Player.toPlayerHeadDir('A'), flag = Flags.dodge_ball)),
            "G": Task(Skill.Goalie()),
        }

    def getMatchString(self) -> str:
        return "{A}[L]"

    def transFunction(self) -> str:
        if buffered_condition(Player.toTargetDist('L')<50, 10, 180):
            return "GetBall"
        return "ToBall2"
    
class GetBall(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.StaticGetBallV4(SHOOT_POS, False)),
            "L": Task(Skill.RushTo(ReceivePos(), Player.toBallDir('L'), flag = Flags.dodge_ball)),
            "G": Task(Skill.Goalie()),
        }

    def getMatchString(self) -> str:
        return "{A}[L]"

    def transFunction(self) -> str:
        print(Player.toBallDist("A"))
        if buffered_condition(Player.toBallDist("A") < 200, 10, 100):
            return "PassBall"
        return "GetBall"
    
class PassBall(State):

    def getTasks(self) -> "dict[str, Task]":
        print("let's Pass the Ball")
        return {
            "A": Task(Skill.PassToPos(Player.Pos("L"))),
            "L": Task(Skill.RushTo(ReceivePos(), Player.toBallDir('L'), flag = Flags.dodge_ball)),
            "G": Task(Skill.Goalie()),
        }

    def getMatchString(self) -> str:
        return "{A}[L]"

    def transFunction(self) -> str:
        if buffered_condition(Player.kickBallVision("A"), 1, 100):
            return "Receive"
        return "PassBall"
    
class Receive(State):

    def getTasks(self) -> "dict[str, Task]":
        print("In Receive State")
        return {
            "A": Task(Skill.RushTo(ReceivePos(), Player.toBallDir('A'))),
            "L": Task(Skill.GetBallV5(Player.toBallDir('L'))),
            "G": Task(Skill.Goalie()),
        }

    def getMatchString(self) -> str:
        return "{A}[L]"

    def transFunction(self) -> str:
        if buffered_condition(Ball.toPlayerHeadDist("L") < 200, 50, 150):
            return "exit"
        return "Receive"
    
@declare_state_machine(
    ToBall1,
    ToBall2,
    GetBall,
    PassBall,
    Receive,
)
class DirectKick_2023(StateMachine):
    pass
    
