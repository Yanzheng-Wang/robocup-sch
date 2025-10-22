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


STOP_FLAG = bit._or(Flags.slowly, Flags.dodge_ball)
STOP_DSS = bit._or(bit._or(STOP_FLAG, Flags.allow_dss), Flags.avoid_stop_ball_circle)
ACC = 2000
Stop_mode = 1
run_once = True
last_cycle = 0
matchStr = ""
lasteMatchStr = ""
stopTasks = []

STOP_FLAG = Flags.avoid_stop_ball_circle + Flags.allow_dss

def getStopPos(index):
    def inner():
        return CppPackage.getPosModulePos(index, Stop_mode)
    return inner

def getAttackerNum(num):
    return defenceSequence.getFreeDefNum(num)

def generateStopTasks():
    global stopTasks, matchStr
    stopTasks = []
    backNum = 3
    subStr = ["A", "S", "M", "D", "B", "R", "C", "F", "K"]
    curindex = 1
    posNum = 11
    enemyNum = defenceSequence.attackerAmount()
    defendNum = 0
    RealDefendNum = 0

    if Player.valid(beckhamDecision.kickNum()):
        matchStr = "{L}"
        gRoleNum["L"] = beckhamDecision.kickNum()
    else:
        matchStr = "[L]"
    stopTasks.append(Task(Skill.RushTo(getStopPos(0), 0, ACC, STOP_DSS)))

    # rollpoling
    stopTasks.append(Task(Skill.RushTo(Positions.rollpolingPos, 0, ACC, STOP_DSS)))
    gRoleNum["A"] = messiDecision.worstNum()
    matchStr = matchStr + "{A}"
    curindex += 1

    matchStr = matchStr + "("
    # back
    # 这里的backNum调整逻辑可根据实际情况补充
    for i in range(1, backNum + 1):
        stopTasks.append(Task(Skill.WBack(backNum, i)))
        if curindex > 9:
            break
        matchStr = matchStr + subStr[curindex - 1]
        curindex += 1
    matchStr = matchStr + ")("

    # marking
    if Ball.posX() > 1000:
        defendNum = enemyNum
    else:
        defendNum = enemyNum
    debugEngine.gui_debug_msg(CGeoPoint(0, (Params.pitchWidth / 2 + 200) * (-1 if Global.isRight else 1)), "ourValidNum: " + str(Conditions.validNum()))
    debugEngine.gui_debug_msg(CGeoPoint(0, (Params.pitchWidth / 2 + 400) * (-1 if Global.isRight else 1)), "defendNum: " + str(defendNum))
    for i in range(defendNum):
        if not Enemy.IsTooClose2Ball(getAttackerNum(i)):
            if Ball.posX() < 0:
                stopTasks.append(Task(Skill.wmarking("Zero", Flags.avoid_stop_ball_circle, getAttackerNum(i))))
                if curindex > 9:
                    break
                matchStr = matchStr + subStr[curindex - 1]
                curindex += 1
    matchStr = matchStr + ")("

    # normalPos
    for i in range(1, posNum + 1):
        stopTasks.append(Task(Skill.RushTo(getStopPos(i), 0, ACC, STOP_DSS)))
        if curindex > 9:
            break
        matchStr = matchStr + subStr[curindex - 1]
        curindex += 1
    matchStr = matchStr + ")"
    debugEngine.gui_debug_msg(CGeoPoint(0, (-Params.pitchWidth / 2 - 200) * (-1 if Global.isRight else 1)), matchStr)

def stopMatch():
    return matchStr

def stopTask(index):
    def inner():
        return stopTasks[index]
    return inner

def play_switch():
    global run_once, last_cycle
    if Conditions.isGameOn():
        return "exit"
    if vision.getCycle() - last_cycle > 5:
        run_once = True
    generateStopTasks()
    if beckhamDecision.KickNumChanged() or run_once or gRoleNum["A"] == gRoleNum["L"] or gRoleNum["L"] != -1:
        run_once = False
        return "run"
    last_cycle = vision.getCycle()

gPlayTable.CreatePlay({
    "firstState": "stop",
    "switch": play_switch,
    "stop": {
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
        "L":   stopTask(1),
        "A": stopTask(2),
        "S":  stopTask(3),
        "M":   stopTask(4),
        "D": stopTask(5),
        "B":  stopTask(6),
        "R": stopTask(7),
        "C":   stopTask(8),
        "F":  stopTask(9),
        "K":   stopTask(10),
        "G":   Task(Skill.Goalie()),
        "match": stopMatch
    },
    "name": "Ref_Stop_11vs11",
    "applicable": {
        "exp": "a",
        "a": True
    },
    "attribute": "attack",
    "timeout": 99999
})