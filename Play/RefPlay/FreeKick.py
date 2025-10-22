import Global
from Geometry import *
from Global import debugEngine
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Strategy import *
from Vision import *
from WorldModel import Flags, Params, Positions

f = Flags.dribbling + Flags.allow_dss
DSS_FLAG = Flags.dodge_ball + Flags.min_dss
Free_kick_mode = 2
prematchStr = ""
matchStr = ""
lasteMatchStr = ""
attackPreTasks = []
attackTasks = []

play_cycle = 0
last_Cycle = 0
nextRoleNumber = Global.NextRoleNumber()


def getPassPos():
    return beckhamDecision.get_passPos()


def getFlatPassVel():
    return beckhamDecision.flatPassVel()


def getChipPassVel():
    return beckhamDecision.chipPassVel()


def getFreeKickPos(index):
    return beckhamDecision.get_waitPos(index)


def getPlayerNum(index):
    if index == 0:
        return Global.getRoleNumber("A")
    elif index == 1:
        return Global.getRoleNumber("S")
    elif index == 2:
        return Global.getRoleNumber("M")
    elif index == 3:
        return Global.getRoleNumber("D")
    elif index == 4:
        return Global.getRoleNumber("B")
    elif index == 5:
        return Global.getRoleNumber("R")
    elif index == 6:
        return Global.getRoleNumber("C")
    elif index == 7:
        return Global.getRoleNumber("F")
    elif index == 8:
        return Global.getRoleNumber("K")
    else:
        return Global.getRoleNumber("L")


def generatePreAttackTasks():
    global attackPreTasks, prematchStr, play_cycle
    nextRoleNumber.resetNextRoleNumber()
    attackPreTasks = []
    backNum = 3
    subStr = ["A", "S", "M", "D", "B", "R", "C", "F", "K"]
    curindex = 1
    start = 0
    posNum = 11

    if Player.valid(beckhamDecision.kickNum()):
        prematchStr = "{L}"
        nextRoleNumber["L"] = beckhamDecision.kickNum()
    else:
        prematchStr = "(L)"
    attackPreTasks.append(Task(Skill.StaticGetBall(getPassPos(), getFlatPassVel(), getChipPassVel()))) # todo: 这边为什么是这个点位？

    # recv
    if Player.valid(beckhamDecision.firstrecvNum()):
        if Ball.posX() >= -Params.pitchLength / 8:
            attackPreTasks.append(
                Task(lambda runner: Skill.RushTo(getFreeKickPos(0), Player.toTheirGoalDir(runner), None, DSS_FLAG + Flags.free_kick)))
            prematchStr += "{A}"
            nextRoleNumber["A"] = beckhamDecision.firstrecvNum()
            curindex += 1
            start += 1
    if Player.valid(beckhamDecision.secondrecvNum()):
        if Ball.posX() >= -Params.pitchLength / 8:
            prematchStr += "{S}"
            nextRoleNumber["S"] = beckhamDecision.secondrecvNum()
            attackPreTasks.append(
                Task(lambda runner: Skill.RushTo(getFreeKickPos(1), Player.toTheirGoalDir(runner), None, DSS_FLAG + Flags.free_kick)))
            curindex += 1
            start += 1
    debugEngine.gui_debug_msg(CGeoPoint(0, 500), str(beckhamDecision.firstrecvNum()))

    # back
    prematchStr += "["
    # 这里的backNum调整逻辑可根据实际情况补充
    for i in range(1, backNum + 1):
        attackPreTasks.append(Task(Skill.WBack(backNum, i)))
        if curindex >= 9:
            break
        prematchStr += subStr[curindex]
        curindex += 1
    prematchStr += "]"

    if play_cycle < 3:
        prematchStr += "["
    else:
        prematchStr += "{"
    # normalPos
    for i in range(start, posNum + 1):
        attackPreTasks.append(
            Task(lambda runner: Skill.RushTo(getFreeKickPos(i), Player.toTheirGoalDir(runner), None, DSS_FLAG + Flags.free_kick)))
        if curindex >= 9:
            break
        prematchStr += subStr[curindex]
        curindex += 1
    if play_cycle < 3:
        prematchStr += "]"
    else:
        prematchStr += "}"
    debugEngine.gui_debug_msg(CGeoPoint(0, (-Params.pitchWidth / 2 - 200) * (-1 if Global.isRight else 1)), prematchStr)


def generateAttackTasks():
    global attackTasks, matchStr, play_cycle
    nextRoleNumber.resetNextRoleNumber()
    attackTasks = []
    backNum = 3
    subStr = ["A", "S", "M", "D", "B", "R", "C", "F", "K"]
    curindex = 1
    start = 0
    posNum = 11

    if Player.valid(beckhamDecision.kickNum()):
        matchStr = "{L}"
        nextRoleNumber["L"] = beckhamDecision.kickNum()
    else:
        matchStr = "[L]"
    attackTasks.append(Task(Skill.WBack(1, 1)))

    # recv
    if Player.valid(beckhamDecision.firstrecvNum()):
        matchStr += "{A}"
        if beckhamDecision.firstrecvNum() == beckhamDecision.nextKicker():
            attackTasks.append(
                Task(Skill.Shoot(Positions.theirGoal, isChip=False)))
        else:
            attackTasks.append(
                Task(lambda runer: Skill.RushTo(getFreeKickPos(0), Player.toTheirGoalDir(runer), 0, DSS_FLAG)))
        curindex += 1
        start += 1
    if Player.valid(beckhamDecision.secondrecvNum()):
        matchStr += "{S}"
        if beckhamDecision.secondrecvNum() == beckhamDecision.nextKicker():
            attackTasks.append(
                Task(Skill.Shoot(Positions.theirGoal, isChip=False)))
        else:
            attackTasks.append(
                Task(lambda runner: Skill.RushTo(getFreeKickPos(1), Player.toTheirGoalDir(runner), 0, DSS_FLAG)))
        curindex += 1
        start += 1

    # back
    matchStr += "["
    for i in range(1, backNum + 1):
        attackTasks.append(Task(Skill.WBack(backNum, i)))
        if curindex >= 9:
            break
        matchStr += subStr[curindex]
        curindex += 1
    matchStr += "]{"
    # normalPos
    for i in range(start, posNum + 1):
        if getPlayerNum(i) == beckhamDecision.nextKicker():
            attackTasks.append(
                Task(Skill.Shoot(Positions.theirGoal, isChip=False)))
        else:
            attackTasks.append(
                Task(lambda executor: Skill.RushTo(getFreeKickPos(i), Player.toTheirGoalDir(executor), None, DSS_FLAG)))
        if curindex >= 9:
            break
        matchStr += subStr[curindex]
        curindex += 1
    matchStr += "}"
    debugEngine.gui_debug_msg(CGeoPoint(0, (-Params.pitchWidth / 2 - 400) * (-1 if Global.isRight else 1)), matchStr)


def attackMatch():
    if beckhamDecision.leaderKicked():
        return matchStr
    else:
        return prematchStr


def attackTask(index):
    if beckhamDecision.leaderKicked():
        return attackTasks[index]
    else:
        return attackPreTasks[index]


def play_cycle_selfadd():
    global play_cycle
    play_cycle += 1


ToGoalPoint = [
    CGeoPoint(Params.pitchLength / 2, 0),
    Ball.refSyntYPos(CGeoPoint(Params.pitchLength / 2, Params.goalWidth / 2 - 200)),
    Ball.refAntiYPos(CGeoPoint(Params.pitchLength / 2, Params.goalWidth / 2 - 200)),
]


def play_switch():
    global play_cycle, last_Cycle
    play_cycle_selfadd()
    if beckhamDecision.judgeExitState():
        play_cycle = 0
        return "exit"
    if vision.getCycle() - last_Cycle > 6:
        play_cycle = 0
    last_Cycle = vision.getCycle()
    generatePreAttackTasks()
    generateAttackTasks()
    messiDecision.setUseFreeRec(True)
    return "Run"


class Stop(State):
    def getTasks(self) -> "dict[str, Task]":
        return {
            "L": Task(Skill.Stop()),
            "A": Task(Skill.Stop()),
            "S": Task(Skill.Stop()),
            "M": Task(Skill.Stop()),
            "D": Task(Skill.Stop()),
            "B": Task(Skill.Stop()),
            "R": Task(Skill.Stop()),
            "C": Task(Skill.Stop()),
            "F": Task(Skill.Stop()),
            "K": Task(Skill.Stop()),
            "G": Task(Skill.Goalie()),
        }

    def getMatchString(self) -> str:
        return "[L][ASMDBRCFK]"

    def transFunction(self) -> str:
        return play_switch()


class Run(State):
    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": attackTask(0),
            "A": attackTask(1),
            "S": attackTask(2),
            "M": attackTask(3),
            "D": attackTask(4),
            "B": attackTask(5),
            "R": attackTask(6),
            "C": attackTask(7),
            "F": attackTask(8),
            "K": attackTask(9),
            "G": Task(Skill.Goalie()),
        }
        nextRoleNumber.adjustNextRoleNumber(tasks)
        return tasks

    def getMatchString(self) -> str:
        return attackMatch()

    def transFunction(self) -> str:
        return play_switch()


@declare_state_machine(
    Stop,
    Run,
)
class FreeKick(StateMachine):
    pass
