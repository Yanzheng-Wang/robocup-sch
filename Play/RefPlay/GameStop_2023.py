import Global
from CppPackage import getPosModulePos
from Geometry import *
from Global import debugEngine
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Strategy import *
from Vision import *
from Vision import Enemy
from WorldModel import Flags, Conditions, Params, Positions
import math
START_POS = CGeoPoint(27/1200*Params.pitchLength,0)
RECEIVE_POS_1 = CGeoPoint(-110/1200*Params.pitchLength,-70/900*Params.pitchWidth)
RECEIVE_POS_2 = CGeoPoint(-110/1200*Params.pitchLength,70/900*Params.pitchWidth)

def SwitchBallArea():
    if Conditions.isGameOn():
        return "exit"
    elif abs(Ball.posX())<150 and abs(Ball.posY())<1500:
        return "kickoff"
    elif Ball.posX() > 4800 and abs(Ball.posY()) > 3000:
        return "CornerKickStop"
    elif Ball.posX() > 1000:  ##我方FrontKick或FrontDef
        return "FrontStop"
    elif Ball.posX() > -1000:  ##半攻半防
        return "MiddleStop"
    elif Ball.posX() < -3000 and (Ball.posY()) > 1200:  
        return "CornerDefendStop"
    elif Ball.posX() < -3000 and abs(Ball.posY()) < 1200:
        return "BackStop"
    else:
        return "BackStop"
    
FRONT_POS1 = Ball.antiYPos(CGeoPoint(350/1200 * Params.pitchLength, -150/900 * Params.pitchWidth))
FRONT_POS3 = Ball.antiYPos(CGeoPoint(350/1200 * Params.pitchLength, 150/900 * Params.pitchWidth))
DefendMiddlePos = CGeoPoint(-450/1200*Params.pitchLength,0)

def GetDefendPos():
    BallToOurGoalDist =  ((Ball.posX() - (-4500))**2 + (Ball.posY() - 0)**2)**0.5
    return CGeoPoint(Ball.posX() -600 / BallToOurGoalDist * (Ball.posX() - (-4500)), Ball.posY() + Ball.antiY() * 600 / BallToOurGoalDist * abs(Ball.posY()))

class kickoff(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "L": Task(Skill.RushTo(START_POS,3.14)),
            "A": Task(Skill.RushTo(RECEIVE_POS_1,Player.toBallDir('A'))),
            "G": Task(Skill.Goalie()),
        }

    def getMatchString(self) -> str:
        return "[L][A]"

    def transFunction(self) -> str:
        return SwitchBallArea()


class CornerKickStop(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.RushTo(messiDecision.receiverPos(),Player.toBallDir('L'))),
            #"A": Task(Skill.RushTo(FRONT_POS1,Player.toBallDir('A'))),
            "A": Task(Skill.RushTo(GetDefendPos(),Player.toBallDir('A'))),
            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return "[A][L]"

    def transFunction(self) -> str:
        return SwitchBallArea()
    
class FrontStop(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.RushTo(messiDecision.receiverPos(),Player.toBallDir('L'))),
            #"A": Task(Skill.RushTo(FRONT_POS3,Player.toBallDir('A'))),
            "A": Task(Skill.RushTo(GetDefendPos(),Player.toBallDir('A'))),
            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return "[A][L]"

    def transFunction(self) -> str:
        return SwitchBallArea()
    
class MiddleStop(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.RushTo(GetDefendPos(), Player.toBallDir('L'))),
            "A": Task(Skill.WBack(1,1)),
            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return "[L][A]"

    def transFunction(self) -> str:
        return SwitchBallArea()
    
class CornerDefendStop(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.RushTo(GetDefendPos(), Player.toBallDir('L'))),
            "A": Task(Skill.WMarking(priority=0,flag=0,num=defenceSequence.getAttackNum(0))),
            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return "[L][A]"

    def transFunction(self) -> str:
        return SwitchBallArea()

class BackStop(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.RushTo(GetDefendPos(), Player.toBallDir('L'))),
            "A": Task(Skill.WMarking(priority=0,num=defenceSequence.getAttackNum(0))),
            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return "[L][A]"

    def transFunction(self) -> str:
        return SwitchBallArea()

@declare_state_machine(
    BackStop,
    kickoff,
    CornerKickStop,
    FrontStop,
    MiddleStop,
    CornerDefendStop
)
class GameStop_2023(StateMachine):
    pass

