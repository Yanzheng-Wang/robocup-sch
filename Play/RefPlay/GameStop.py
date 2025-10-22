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

STOP_FLAG = Flags.slowly | Flags.dodge_ball
STOP_DSS = (STOP_FLAG | Flags.allow_dss) | Flags.avoid_stop_ball_circle
ACC = 2000
Stop_mode = 1
run_once = True
last_cycle = 0
matchStr = ""
lasteMatchStr = ""
stopTasks = []

STOP_FLAG = Flags.avoid_stop_ball_circle + Flags.allow_dss

defaultNextRoleNumber = {
    "A": -1,
    "B": -1,
    "C": -1,
    "D": -1,
    "E": -1,
    "F": -1,
    "H": -1,
    "I": -1,
    "J": -1,
    "K": -1,
    "L": -1,

    "G": -1,
}
nextRoleNumber = defaultNextRoleNumber.copy()


def resetNextRoleNumber():
    global nextRoleNumber
    nextRoleNumber = defaultNextRoleNumber.copy()  # 复制一份，避免修改默认值


def getStopPos(index):
    return getPosModulePos(index, Stop_mode)


def getAttackerNum(num):
    return defenceSequence.getFreeDefNum(num)


def generateStopTasks():
    global stopTasks, matchStr
    resetNextRoleNumber()  # 重置nextRoleNumber
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
        nextRoleNumber["L"] = beckhamDecision.kickNum()
    else:
        matchStr = "[L]"
    stopTasks.append(Task(Skill.RushTo(getStopPos(0), 0, maxAcc=ACC, flag=STOP_DSS)))

    # rollpoling
    stopTasks.append(Task(Skill.RushTo(Positions.rollpolingPos(), 0, ACC, STOP_DSS)))
    nextRoleNumber["A"] = messiDecision.worstNum()
    matchStr = matchStr + "{A}"
    curindex += 1

    matchStr = matchStr + "("
    # back
    # 这里的backNum调整逻辑可根据实际情况补充
    for i in range(1, backNum + 1):
        stopTasks.append(Task(Skill.WBack(backNum, i)))
        if curindex >= 9:
            break
        matchStr = matchStr + subStr[curindex - 1]
        curindex += 1
    matchStr = matchStr + ")("

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
            if Ball.posX() < 0:
                stopTasks.append(Task(Skill.WMarking(0, flag=Flags.avoid_stop_ball_circle, num=getAttackerNum(i))))
                if curindex >= 9:
                    break
                matchStr = matchStr + subStr[curindex - 1]
                curindex += 1
    matchStr = matchStr + ")("

    # normalPos
    for i in range(1, posNum + 1):
        stopTasks.append(Task(Skill.RushTo(getStopPos(i), 0, ACC, STOP_DSS)))
        if curindex >= 9:
            break
        matchStr = matchStr + subStr[curindex - 1]
        curindex += 1
    matchStr = matchStr + ")"
    debugEngine.gui_debug_msg(CGeoPoint(0, (-Params.pitchWidth / 2 - 200) * (-1 if Global.isRight else 1)), matchStr)


def stopMatch():
    return matchStr

def play_switch():
    global run_once, last_cycle
    if Conditions.isGameOn():
        return "exit"  # ???不是顶层会直接退出吗？这边为什么还要手动写这个神奇的东西？
    if vision.getCycle() - last_cycle > 5:
        run_once = True
    generateStopTasks()
    if beckhamDecision.KickNumChanged() or run_once or Global.getLastRoleNumber("A") == Global.getLastRoleNumber(
            "L") or Global.getLastRoleNumber("L") != -1:
        run_once = False
        return "Run"
    last_cycle = vision.getCycle()
    return ""


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
            "L": stopTasks[0],
            "A": stopTasks[1],
            "S": stopTasks[2],
            "M": stopTasks[3],
            "D": stopTasks[4],
            "B": stopTasks[5],
            "R": stopTasks[6],
            "C": stopTasks[7],
            "F": stopTasks[8],
            "K": stopTasks[9],

            "G": Task(Skill.Goalie()),
        }
        return tasks

    def getMatchString(self) -> str:
        return stopMatch()

    def transFunction(self) -> str:
        return play_switch()


@declare_state_machine(
    Stop,
    Run
)
class GameStop(StateMachine):
    pass


"""
gPlayTable.CreatePlay({
    "firstState": "stop",
    "switch": play_switch, # 神奇？为什么放在这边？？？
    "stop": {
        "Leader":   Task(Skill.stop()),
        "Assister": Task(Skill.stop()),
        "Special":  Task(Skill.stop()),
        "Middle":   Task(Skill.stop()),
        "Defender": Task(Skill.stop()),
        "Breaker":  Task(Skill.stop()),
        "Receiver": Task(Skill.stop()),
        "Center":   Task(Skill.stop()),
        "Fronter":  Task(Skill.stop()),
        "Kicker":   Task(Skill.stop()),
        "Goalie":   Task(Skill.goalie()),
        "match": "[L][ASMDBRCFK]"
    },
    "run": {
        "Leader":   stopTask(1),
        "Assister": stopTask(2),
        "Special":  stopTask(3),
        "Middle":   stopTask(4),
        "Defender": stopTask(5),
        "Breaker":  stopTask(6),
        "Receiver": stopTask(7),
        "Center":   stopTask(8),
        "Fronter":  stopTask(9),
        "Kicker":   stopTask(10),
        "Goalie":   Task(Skill.goalie()),
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
"""
