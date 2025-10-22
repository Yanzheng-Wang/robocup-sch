import Global
from Geometry import *
from Global import debugEngine
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Strategy import *
from Vision import *
from Vision import Enemy
from WorldModel import Flags, Conditions, Params


def getAttackerNum(num):
    return defenceSequence.getFreeDefNum(num)


FreeKickDef_mode = 3
matchStr = ""
lastMatchStr = ""
defenceTasks = []
free_def_cnt = 0


def getFreeKickDefPos(index):
    return CppPackage.getPosModulePos(index, FreeKickDef_mode)


def generateDefenceTasks():
    global defenceTasks, matchStr
    defenceTasks = []
    backNum = 3
    subStr = ["A", "S", "M", "D", "B", "R", "C", "F", "K"]
    curindex = 1
    posNum = 11
    enemyNum = defenceSequence.attackerAmount()
    defendNum = 0
    matchStr = "("
    # back
    if Ball.posX() > -Params.pitchLength / 4:
        RealDefendNum = 0
        for i in range(enemyNum):
            if not Enemy.IsTooClose2Ball(getAttackerNum(i)):
                RealDefendNum += 1
        if Conditions.validNum() - 3 < RealDefendNum:
            backNum = 1
        if Ball.posX() > Params.pitchLength / 8 and Conditions.validNum() - 2 < RealDefendNum:
            backNum = 0
    for i in range(1, backNum + 1):
        defenceTasks.append(Task(Skill.WBack(backNum, i)))
        if curindex >= 9:
            break
        matchStr += subStr[curindex - 1]
        curindex += 1
    matchStr += ")("
    # marking
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
            defenceTasks.append(Task(Skill.WMarking(i, flag=Flags.avoid_stop_ball_circle, num=getAttackerNum(i))))
            if curindex >= 9:
                break
            matchStr += subStr[curindex - 1]
            curindex += 1
    matchStr += ")(L)"
    defenceTasks.append(Task(Skill.Marking(Enemy.nearest1(), True, 5000)))
    matchStr += "("
    # normalPos
    for i in range(posNum + 1):
        defenceTasks.append(Task(
            lambda runner: Skill.SmartGoTo(getFreeKickDefPos(i), Player.toBallDir(runner), Flags.allow_dss + Flags.avoid_stop_ball_circle)))
        if curindex >= 9:
            break
        matchStr += subStr[curindex - 1]
        curindex += 1
    matchStr += ")"
    debugEngine.gui_debug_msg(CGeoPoint(0, (-Params.pitchWidth / 2 - 200) * (-1 if Global.isRight else 1)), matchStr)


def defendMatch():
    return matchStr


def defendTask(index):
    return defenceTasks[index]





def play_switch_run():
    global lastMatchStr
    # if Conditions.ballMoved():
    #     return "exit"
    if Conditions.ballMoved() and not Conditions.isGameStop():
        return "exit"
    if Conditions.isGameOn():
        return "exit"
    generateDefenceTasks()
    if lastMatchStr != matchStr:
        lastMatchStr = matchStr
        return "Run"
    return ""


class Beginning(State):
    def transFunction(self) -> str:
        generateDefenceTasks()  # 初始的时候需要generate一下
        global free_def_cnt
        free_def_cnt = 0
        return "Run"

    def getMatchString(self) -> str:
        return "[L][ASMDBRCFK]"

    def getTasks(self) -> "dict[str, Task]":
        Tasks = {
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
            "G": Task(Skill.Goalie())
        }
        return Tasks


class Run(State):
    def transFunction(self) -> str:
        return play_switch_run()

    def getMatchString(self) -> str:
        return defendMatch()

    def getTasks(self) -> "dict[str, Task]":
        Tasks = {
            "A": defendTask(0),
            "S": defendTask(1),
            "M": defendTask(2),
            "D": defendTask(3),
            "L": defendTask(4),
            "B": defendTask(5),
            "R": defendTask(6),
            "C": defendTask(7),
            "F": defendTask(8),
            "K": defendTask(9),
            "G": Task(Skill.Goalie()),
        }
        return Tasks

@declare_state_machine(
    Beginning,
    Run
)
class FreeKickDefend(StateMachine):
    pass
"""

gPlayTable.CreatePlay({
    "firstState": "beginning",

    "beginning": {
        "switch": play_switch_beginning,
        "L":   Task(Skill.Stop()),
        "A": Task(Skill.Stop()),
        "S":  Task(Skill.Stop()),
        "M":   Task(Skill.Stop()),
        "D": Task(Skill.Stop()),
        "B":  Task(Skill.Stop()),
        "R": Task(Skill.Stop()),
        "C":   Task(Skill.Stop()),
        "F":  Task(Skill.Stop()),
        "K":   Task(Skill.Stop()),
        "G":   Task(Skill.Goalie()),
        "match": "[L][ASMDBRCFK]"
    },

    "run": {
        "switch": play_switch_run,
        "A": defendTask(1),
        "S":  defendTask(2),
        "M":   defendTask(3),
        "D": defendTask(4),
        "L":   defendTask(5),
        "B":  defendTask(6),
        "R": defendTask(7),
        "C":   defendTask(8),
        "F":  defendTask(9),
        "K":   defendTask(10),
        "G":   Task(Skill.Goalie()),
        "match": defendMatch
    },

    "name": "Ref_FreeKickDef_11vs11",
    "applicable": {
        "exp": "a",
        "a": True
    },
    "attribute": "defense",
    "timeout": 99999
})
"""
