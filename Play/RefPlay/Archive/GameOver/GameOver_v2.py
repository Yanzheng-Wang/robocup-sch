import math

from Geometry import *
import Utils
from Utils import buffered_condition
from Vision import Player
center = CGeoPoint(0, 0)

stoppos = [
    CGeoPoint(-1000, 100),
    CGeoPoint(-1000, -100),
    CGeoPoint(-1000, 300),
    CGeoPoint(-1000, -300),
    CGeoPoint(-1000, 500),
    CGeoPoint(-1000, -500),
    CGeoPoint(-1000, 700),
    CGeoPoint(-1000, -700),
]

standpos = [
    CGeoPoint(-1000, 0),
    CGeoPoint(1000, 0),
    CGeoPoint(0, 0) + Utils.Polar2Vector(1000, math.pi / 4),
    CGeoPoint(0, 0) + Utils.Polar2Vector(1000, math.pi / 2),
    CGeoPoint(0, 0) + Utils.Polar2Vector(1000, 3 * math.pi / 4),
    CGeoPoint(0, 0) + Utils.Polar2Vector(1000, -math.pi / 4),
    CGeoPoint(0, 0) + Utils.Polar2Vector(1000, -math.pi / 2),
    CGeoPoint(0, 0) + Utils.Polar2Vector(1000, -3 * math.pi / 4),
]

def gatherpos(role):
    def inner():
        idir = (Player.pos(role) - center).dir()
        ipos = center + Utils.Polar2Vector(400, idir)
        return ipos
    return inner

def distractpos(role):
    def inner():
        idir = (Player.pos(role) - center).dir()
        ipos = center + Utils.Polar2Vector(1000, idir)
        return ipos
    return inner

angle = 0

def THIH(total, my):
    def inner():
        return CGeoPoint(
            1000 * math.cos(angle + my * math.pi * 2 / total),
            1000 * math.sin(angle + my * math.pi * 2 / total)
        )
    return inner

count = 0

gPlayTable.CreatePlay({
    "firstState": "move",
    "move": {
        "switch": lambda: (
            "turn" if bufcnt(
                Player.toTargetDist("Assister") < 20 and
                Player.toTargetDist("Leader") < 20 and
                Player.toTargetDist("Special") < 20 and
                Player.toTargetDist("Defender") < 20 and
                Player.toTargetDist("Middle") < 20 and
                Player.toTargetDist("Center") < 20 and
                Player.toTargetDist("Breaker") < 20 and
                Player.toTargetDist("Fronter"),
                20, 999
            ) else None
        ),
        "Leader":   task.goCmuRush(standpos[0], Player.toPointDir(center), None, flag.allow_dss),
        "Special":  task.goCmuRush(standpos[1], Player.toPointDir(center), None, flag.allow_dss),
        "Middle":   task.goCmuRush(standpos[2], Player.toPointDir(center), None, flag.allow_dss),
        "Defender": task.goCmuRush(standpos[3], Player.toPointDir(center), None, flag.allow_dss),
        "Assister": task.goCmuRush(standpos[4], Player.toPointDir(center), None, flag.allow_dss),
        "Center":   task.goCmuRush(standpos[5], Player.toPointDir(center), None, flag.allow_dss),
        "Breaker":  task.goCmuRush(standpos[6], Player.toPointDir(center), None, flag.allow_dss),
        "Fronter":  task.goCmuRush(standpos[7], Player.toPointDir(center), None, flag.allow_dss),
        "match": "{LSADMCBF}"
    },
    "turn": {
        "switch": lambda: (
            "gather" if bufcnt(True, 120) else None
        ),
        "Leader":   task.goCmuRush(THIH(8, 1), Player.toPointDir(center), None, flag.allow_dss),
        "Special":  task.goCmuRush(THIH(8, 2), Player.toPointDir(center), None, flag.allow_dss),
        "Middle":   task.goCmuRush(THIH(8, 3), Player.toPointDir(center), None, flag.allow_dss),
        "Defender": task.goCmuRush(THIH(8, 4), Player.toPointDir(center), None, flag.allow_dss),
        "Assister": task.goCmuRush(THIH(8, 5), Player.toPointDir(center), None, flag.allow_dss),
        "Center":   task.goCmuRush(THIH(8, 6), Player.toPointDir(center), None, flag.allow_dss),
        "Breaker":  task.goCmuRush(THIH(8, 7), Player.toPointDir(center), None, flag.allow_dss),
        "Fronter":  task.goCmuRush(THIH(8, 8), Player.toPointDir(center), None, flag.allow_dss),
        "match": "[LSADMCBF]"
    },
    "gather": {
        "switch": lambda: (
            "distract" if bufcnt(
                Player.toTargetDist("Assister") < 20 and
                Player.toTargetDist("Leader") < 20 and
                Player.toTargetDist("Special") < 20 and
                Player.toTargetDist("Defender") < 20 and
                Player.toTargetDist("Middle") < 20 and
                Player.toTargetDist("Center") < 20 and
                Player.toTargetDist("Breaker") < 20 and
                Player.toTargetDist("Fronter"),
                20, 999
            ) else None
        ),
        "Leader":   task.goCmuRush(gatherpos("Leader"), Player.toPointDir(center), None, flag.allow_dss),
        "Special":  task.goCmuRush(gatherpos("Special"), Player.toPointDir(center), None, flag.allow_dss),
        "Middle":   task.goCmuRush(gatherpos("Middle"), Player.toPointDir(center), None, flag.allow_dss),
        "Defender": task.goCmuRush(gatherpos("Defender"), Player.toPointDir(center), None, flag.allow_dss),
        "Assister": task.goCmuRush(gatherpos("Assister"), Player.toPointDir(center), None, flag.allow_dss),
        "Center":   task.goCmuRush(gatherpos("Center"), Player.toPointDir(center), None, flag.allow_dss),
        "Breaker":  task.goCmuRush(gatherpos("Breaker"), Player.toPointDir(center), None, flag.allow_dss),
        "Fronter":  task.goCmuRush(gatherpos("Fronter"), Player.toPointDir(center), None, flag.allow_dss),
        "match": "[LSADMCBF]"
    },
    "distract": {
        "switch": lambda: (
            _distract_switch()
        ),
        "Leader":   task.goCmuRush(distractpos("Leader"), Player.toPointDir(center), None, flag.allow_dss),
        "Special":  task.goCmuRush(distractpos("Special"), Player.toPointDir(center), None, flag.allow_dss),
        "Middle":   task.goCmuRush(distractpos("Middle"), Player.toPointDir(center), None, flag.allow_dss),
        "Defender": task.goCmuRush(distractpos("Defender"), Player.toPointDir(center), None, flag.allow_dss),
        "Assister": task.goCmuRush(distractpos("Assister"), Player.toPointDir(center), None, flag.allow_dss),
        "Center":   task.goCmuRush(distractpos("Center"), Player.toPointDir(center), None, flag.allow_dss),
        "Breaker":  task.goCmuRush(distractpos("Breaker"), Player.toPointDir(center), None, flag.allow_dss),
        "Fronter":  task.goCmuRush(distractpos("Fronter"), Player.toPointDir(center), None, flag.allow_dss),
        "match": "[LSADMCBF]"
    },
    "stop": {
        "switch": lambda: None,
        "Leader":   task.goCmuRush(stoppos[0], 0, None, flag.allow_dss),
        "Special":  task.goCmuRush(stoppos[1], 0, None, flag.allow_dss),
        "Middle":   task.goCmuRush(stoppos[2], 0, None, flag.allow_dss),
        "Defender": task.goCmuRush(stoppos[3], 0, None, flag.allow_dss),
        "Assister": task.goCmuRush(stoppos[4], 0, None, flag.allow_dss),
        "Center":   task.goCmuRush(stoppos[5], 0, None, flag.allow_dss),
        "Breaker":  task.goCmuRush(stoppos[6], 0, None, flag.allow_dss),
        "Fronter":  task.goCmuRush(stoppos[7], 0, None, flag.allow_dss),
        "match": "[LSADMCBF]"
    },
    "name": "Ref_GameOverV2",
    "applicable": {
        "exp": "a",
        "a": True
    },
    "attribute": "defense",
    "timeout": 99999
})

def _distract_switch():
    global count
    if buffered_condition(
        Player.toTargetDist("Assister") < 20 and
        Player.toTargetDist("Leader") < 20 and
        Player.toTargetDist("Special") < 20 and
        Player.toTargetDist("Defender") < 20 and
        Player.toTargetDist("Middle") < 20 and
        Player.toTargetDist("Center") < 20 and
        Player.toTargetDist("Breaker") < 20 and
        Player.toTargetDist("Fronter"),
        20, 999
    ):
        count += 1
        if count != 2:
            return "turn"
        else:
            return "stop"
    return None