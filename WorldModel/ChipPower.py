from numbers import Number
from Geometry import *
from Utils import constrain
from Vision import Player, Ball

minimumPower = 1500
slightPower = 1800
middlePower = 2200
normalPower = 2400
touchPower = 4800
fullPower = 5500

def getChipPower(target: CGeoPoint, originalPos: CGeoPoint=None)->Number:
    """
    从originalPos踢球到target所需的力度！
    :param target:
    :param originalPos: 一般为球的位置！这边默认值也是球的位置
    :return:
    """
    if not originalPos:
        originalPos = Ball.pos()
    power = (target - originalPos).mod() * 1.8  # (0.0000973593*(math.pow(ball().toPointDist(tmpP),2)) + 1.07876 * ball().toPointDist(tmpP) + 1284.17)*0.8
    power = constrain(power, minimumPower, fullPower)
    return power

def toTargetPos(targetPos: CGeoPoint):
    """
    就是球到targetPlayer的位置所需的力度！
    与上面一个兼容
    :param targetPos:
    :return:
    """
    return getChipPower(targetPos, Ball.pos())

def toTargetPlayer(targetPlayer: str | int):
    """
    就是球到targetPlayer的位置所需的力度！
    这是lua层原toTarget函数的替代
    :param targetPlayer:
    :return:
    """
    return getChipPower(Player.Pos(targetPlayer), Ball.pos())
