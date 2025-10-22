import Global
import Utils
from Geometry import *
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Vision import *
from WorldModel import Flags, Conditions, Params, Positions, Directions

our_player_stand_pos = [
    CGeoPoint(-Params.pitchLength/2 + Params.penaltyDepth + 500, 1350),
    CGeoPoint(-Params.pitchLength/2 + Params.penaltyDepth + 500, -1350),
    CGeoPoint(-Params.pitchLength/2 + Params.penaltyDepth + 500, 0),
    CGeoPoint(-Params.pitchLength/2 + Params.penaltyDepth + 500, -1000),
    CGeoPoint(-Params.pitchLength/2 + Params.penaltyDepth + 500, 1000),
    CGeoPoint(-Params.pitchLength/2 + Params.penaltyDepth + 500, -1700),
    CGeoPoint(-Params.pitchLength/2 + Params.penaltyDepth + 500, 1700),
    CGeoPoint(-Params.pitchLength/2 + Params.penaltyDepth + 500, 2100),
    CGeoPoint(-Params.pitchLength/2 + Params.penaltyDepth + 500, -2100),
    CGeoPoint(-Params.pitchLength/2 + Params.penaltyDepth + 500, 2500),
    CGeoPoint(-Params.pitchLength/2 + Params.penaltyDepth + 500, -2500),
]

DSS_FLAG = Flags.allow_dss + Flags.dodge_ball
f = Flags.dribbling
catchf = Flags.dribbling + Flags.our_ball_placement

kickpos = [
    CGeoPoint(Params.pitchLength/2, -Params.goalWidth/2 + 150),
    CGeoPoint(Params.pitchLength/2, Params.goalWidth/2 - 150)
]

def willshootPos():
    ballPos = Ball.pos()
    idir = (ballPos - Positions.theirGoal).dir()
    pos_ = ballPos + Utils.Polar2Vector(350 + Params.playerFrontToCenter, idir)
    return pos_

class WaitStart(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.RushTo(our_player_stand_pos[0], 0, None, DSS_FLAG)),
            "S": Task(Skill.RushTo(our_player_stand_pos[1], 0, None, DSS_FLAG)),
            "D": Task(Skill.RushTo(our_player_stand_pos[3], 0, None, DSS_FLAG)),
            "M": Task(Skill.RushTo(our_player_stand_pos[4], 0, None, DSS_FLAG)),
            "B": Task(Skill.RushTo(our_player_stand_pos[5], 0, None, DSS_FLAG)),
            "R": Task(Skill.RushTo(our_player_stand_pos[6], 0, None, DSS_FLAG)),
            "K": Task(Skill.RushTo(our_player_stand_pos[7], 0, None, DSS_FLAG)),
            "F": Task(Skill.RushTo(our_player_stand_pos[8], 0, None, DSS_FLAG)),
            "C": Task(Skill.RushTo(our_player_stand_pos[9], 0, None, DSS_FLAG)),
            "L": Task(Skill.RushTo(our_player_stand_pos[10], 0, None, DSS_FLAG)),
            "G": Task(Skill.RushTo(willshootPos(), Directions.playerToBall(Global.goalieNumber), None, DSS_FLAG)),
        }

    def getMatchString(self) -> str:
        return "{ASMDBRKFCL}"

    def transFunction(self) -> str:
        if Conditions.isNormalStart():
            return "penaltyKick"
        return ""

class penaltyKick(State):

    def transFunction(self) -> str:
        return ""

    def getTasks(self) -> "dict[str, Task]":
        return {
            "A": Task(Skill.RushTo(our_player_stand_pos[0], 0, None, DSS_FLAG)),
            "S":  Task(Skill.RushTo(our_player_stand_pos[1], 0, None, DSS_FLAG)),
            "D": Task(Skill.RushTo(our_player_stand_pos[3], 0, None, DSS_FLAG)),
            "M":   Task(Skill.RushTo(our_player_stand_pos[4], 0, None, DSS_FLAG)),
            "B":  Task(Skill.RushTo(our_player_stand_pos[5], 0, None, DSS_FLAG)),
            "R": Task(Skill.RushTo(our_player_stand_pos[6], 0, None, DSS_FLAG)),
            "K":   Task(Skill.RushTo(our_player_stand_pos[7], 0, None, DSS_FLAG)),
            "F":  Task(Skill.RushTo(our_player_stand_pos[8], 0, None, DSS_FLAG)),
            "C":   Task(Skill.RushTo(our_player_stand_pos[9], 0, None, DSS_FLAG)),
            "L":   Task(Skill.RushTo(our_player_stand_pos[10], 0, None, DSS_FLAG)),
            "G":   Task(Skill.BigPenaltyKick()),
        }

    def getMatchString(self) -> str:
        return "{ASMDBRKFCL}"

@declare_state_machine(
    WaitStart,
    penaltyKick
)
class PenaltyKick(StateMachine):
    pass