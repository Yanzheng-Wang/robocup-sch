import math

import Global
import Utils
from Geometry import *
from Global import debugEngine
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Strategy import *
from Vision import *
from Vision import Enemy
from WorldModel import Flags, Conditions, Params, Positions

SIDE_POS, MIDDLE_POS, INTER_POS, SIDE2_POS, INTER2_POS = Positions.refStopAroundBall()
standpos = [
    CGeoPoint(-Params.pitchLength / 2 + Params.penaltyDepth + 200, -700),
    CGeoPoint(-Params.pitchLength / 2 + Params.penaltyDepth + 200, 700),
    CGeoPoint(0, 1000),
    CGeoPoint(0, -1000),
    CGeoPoint(-Params.pitchLength / 2 + 500, 0),
    CGeoPoint(Params.pitchLength / 4 - 500, 0),
    CGeoPoint(-Params.pitchLength / 4 + 200, -1000),
    CGeoPoint(-Params.pitchLength / 4 + 200, 1000),
]

run_mode = 1
GETBALL = 1
PUSHBALL = 2
PASSBALL = 3
RECEIVE = 4
BALLPLACE_MODE = 5
ballplcae_cnt = 0

run_once = True
last_cycle = 0

matchStr = ""
lasteMatchStr = ""
ballPlaceTasks = []

nextRoleNumber = Global.NextRoleNumber()


def getBallPlacementPos(index):
    return CppPackage.getPosModulePos(index, BALLPLACE_MODE)


def getAttackerNum(num):
    return defenceSequence.getAttackNum(num)


getballcnt = 0
lastCycle = 0
ACC = 5000


def otherflag():
    if Conditions.ourBallPlace():
        return Flags.our_ball_placement + Flags.allow_dss + Flags.avoid_stop_ball_circle
    else:
        return Flags.our_ball_placement + Flags.allow_dss


def LEADER_TASK():
    global run_mode, getballcnt, lastCycle
    if vision.getCycle() - lastCycle > 15:
        run_mode = GETBALL
        getballcnt = 0
    ipos = Ball.pos() + Utils.Polar2Vector(250, Player.toBallDir(Global.getLastRoleNumber("L")) + math.pi)
    if Conditions.ballPlaceFinish() and not Conditions.ballPlaceUnfinish():
        if Player.toBallDist(Global.getLastRoleNumber("L")) > 180:
            return Task(lambda runner: Skill.RushTo(MIDDLE_POS, Player.toBallDir(runner), None,
                                                    Flags.dodge_ball + Flags.allow_dss + Flags.our_ball_placement))
        else:
            return Task(lambda runner: Skill.RushTo(ipos, Player.toBallDir(runner), None,
                                                    Flags.dodge_ball + Flags.allow_dss + Flags.our_ball_placement))
    getballPoint = Ball.pos() + Utils.Polar2Vector(200, (Ball.pos() - Ball.placementPos()).dir())
    if Player.toPointDist(Global.getLastRoleNumber("L"), getballPoint) < 15:
        getballcnt += 1
    if getballcnt > 15:
        run_mode = PUSHBALL
    if not Utils.IsInField(Ball.pos(), 0):
        getballcnt = 0
        run_mode = GETBALL
    debugEngine.gui_debug_msg(CGeoPoint(-200, 0), "NOW MODE:" + str(run_mode))
    lastCycle = vision.getCycle()
    return Task(Skill.FetchBall(Ball.placementPos(), 2500, run_mode))


def ASSISTER_TASK():
    return Task(Skill.RushTo(getBallPlacementPos(2), 0, ACC, otherflag()))


def generateBallPlaceTasks():
    global ballPlaceTasks, matchStr
    nextRoleNumber.resetNextRoleNumber()
    ballPlaceTasks = []
    backNum = 2
    subStr = ["A", "S", "M", "D", "B", "R", "F", "K", "C"]
    curindex = 1
    posNum = 11
    enemyNum = defenceSequence.attackerAmount()
    defendNum = 0
    RealDefendNum = 0
    ballPlaceTasks.append(Task(Skill.RushTo(getBallPlacementPos(1), 0, ACC, otherflag())))
    ballPlaceTasks.append(Task(Skill.RushTo(Positions.rollpolingPos(), 0, ACC, otherflag())))
    nextRoleNumber["A"] = messiDecision.worstNum()
    matchStr = "{A}{L}"
    curindex += 1
    if Conditions.ourBallPlace():
        matchStr += "("
        nextRoleNumber["L"] = beckhamDecision.kickNum()
        ballPlaceTasks.append(LEADER_TASK())
        for i in range(2, posNum + 1):
            ballPlaceTasks.append(Task(Skill.RushTo(getBallPlacementPos(i), 0, ACC, otherflag())))
            if curindex >= 9:
                break
            matchStr += subStr[curindex]
            curindex += 1
    elif Conditions.theirBallPlace():
        matchStr += "("
        if Ball.posX() > 1000:
            defendNum = enemyNum
        else:
            defendNum = enemyNum
        debugEngine.gui_debug_msg(CGeoPoint(0, (Params.pitchWidth / 2 + 200) * (-1 if Global.isRight else 1)),
                                  "ourValidNum: " + str(Conditions.validNum()))
        debugEngine.gui_debug_msg(CGeoPoint(0, (Params.pitchWidth / 2 + 400) * (-1 if Global.isRight else 1)),
                                  "defendNum: " + str(defendNum))
        for i in range(defendNum):
            if not Enemy.IsTooClose2Ball(getAttackerNum(i)):
                if Ball.placementPos().x() < 0:
                    ballPlaceTasks.append(Task(Skill.WMarking(0, flag=Flags.avoid_stop_ball_circle, num=getAttackerNum(i))))
                    if curindex >= 9:
                        break
                    matchStr += subStr[curindex]
                    curindex += 1
        matchStr += ")("
        ballPlaceTasks.append(Task(Skill.RushTo(getBallPlacementPos(2), 0, ACC, otherflag())))
        for i in range(3, posNum + 1):
            ballPlaceTasks.append(Task(Skill.RushTo(getBallPlacementPos(i), 0, ACC, otherflag())))
            if curindex >= 9:
                break
            matchStr += subStr[curindex]
            curindex += 1
    else:
        ballPlaceTasks.append(Task(Skill.RushTo(getBallPlacementPos(2), 0, ACC, otherflag())))
        for i in range(3, posNum + 1):
            ballPlaceTasks.append(Task(Skill.RushTo(getBallPlacementPos(i), 0, ACC, otherflag())))
            if curindex >= 9:
                break
            matchStr += subStr[curindex]
            curindex += 1
    matchStr += ")"
    debugEngine.gui_debug_msg(CGeoPoint(0, (-Params.pitchWidth / 2 - 200) * (-1 if Global.isRight else 1)), matchStr)


def ballplaceMatch():
    return matchStr


def ballplaceTask(index):
    return ballPlaceTasks[index]

def play_switch():
    global run_once, last_cycle
    if Conditions.isGameOn():
        return "exit"
    if vision.getCycle() - last_cycle > 5:
        run_once = True
    generateBallPlaceTasks()
    if beckhamDecision.KickNumChanged() or run_once:
        run_once = False
        return "Run"
    last_cycle = vision.getCycle()
    return ""


class Beginning(State):
    def getTasks(self) -> "dict[str, Task]":
        return {
            "G": Task(Skill.Goalie()),
            "L": Task(Skill.Stop()),
            "A": Task(Skill.Stop()),
            "S": Task(Skill.Stop()),
            "M": Task(Skill.Stop()),
            "D": Task(Skill.Stop()),
            "B": Task(Skill.Stop()),
            "R": Task(Skill.Stop()),
            "F": Task(Skill.Stop()),
            "K": Task(Skill.Stop()),
            "C": Task(Skill.Stop()),
        }

    def getMatchString(self) -> str:
        return "[LASMDBRFKC]"

    def transFunction(self) -> str:
        return play_switch()


class Run(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "G": ballplaceTask(0),
            "A": ballplaceTask(1),
            "L": ballplaceTask(2),
            "S": ballplaceTask(3),
            "M": ballplaceTask(4),
            "D": ballplaceTask(5),
            "B": ballplaceTask(6),
            "R": ballplaceTask(7),
            "F": ballplaceTask(8),
            "K": ballplaceTask(9),
            "C": ballplaceTask(10),
        }

    def getMatchString(self) -> str:
        return ballplaceMatch()

    def transFunction(self) -> str:
        return play_switch()

@declare_state_machine(
    Beginning,
    Run
)
class BallPlace(StateMachine):
    pass