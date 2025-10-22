from numbers import Number

from Utils import constrain
from Vision import Player, Ball

# KickPower是平射！！！

minimumPower = 1500
fullPower = 8000
touchPower = 6500
forReflectPower = 8888
from CppPackage import CGeoPoint

def getKickPower(target: CGeoPoint, originalPos: CGeoPoint)->Number:
    """
        从originalPos踢球到target所需的力度！
        :param target:
        :param originalPos: 一般为球的位置！这边默认值也是球的位置
        :return:
        """
    if not originalPos:
        originalPos = Ball.pos()
    power = (target - originalPos).mod()
    power = constrain(power, minimumPower, fullPower)
    return power

def toTargetPos(targetPos: CGeoPoint):
    """
    就是球到targetPlayer的位置所需的力度！
    与上面一个兼容
    :param targetPos:
    :return:
    """
    return getKickPower(targetPos, Ball.pos())

def toTargetPlayer(targetPlayer: str | int):
    """
    就是球到targetPlayer的位置所需的力度！
    这是lua层原toTarget函数的替代
    :param targetPlayer:
    :return:
    """
    return getKickPower(Player.Pos(targetPlayer), Ball.pos())



# 当p有三种输入(userdate/point、role、function)
# 已经弃用，改用getKickPower
# def toTarget(p, role1):
#     def inner(role):
#         target = None
#         # inSpeed = 4500  # 需要的入嘴速度
#         if callable(p):
#             target = p()
#         elif isinstance(p, (int, float, str)):
#             target = Player.pos(p)
#         # Python中没有userdata类型，这里假设p是某种对象
#         else:
#             target = p
#
#         pw = None
#
#         if Global.isSimulation:
#             # debugEngine.gui_debug_msg(CGeoPoint.new_local(0, 0), "0")
#             if role1 is None:
#                 return Player.toPointDist(role, target) < 2500 and 2500 or Player.toPointDist(role, target)  # *1.2 --+1900
#             else:
#                 return Player.toPointDist(role1, target) < 2500 and 2500 or Player.toPointDist(role1, target)  # *1.2
#         else:
#             # if Player.num(role) == 1:
#             #     pw = Player.toPointDist(role, target)*0.553167 + 0.0000345591*math.pow(Player.toPointDist(role, target),2) + 987.004
#             # elif Player.num(role) in [0, 4, 5, 2, 3]:
#             #     pw = Player.toPointDist(role, target)*0.136966 + 0.000103831*math.pow(Player.toPointDist(role, target),2) + 774.202  # *1.5714 + 428.57
#             if role1 is None:
#                 pw = Player.toPointDist(role, target) * 1
#             else:
#                 pw = Player.toPointDist(role1, target) * 1
#
#         if pw < 1500:  # 50 --> 250 Modified by Soap, 2015/4/11
#             pw = 1500  # 50 --> 250 Modified by Soap, 2015/4/11
#         elif pw > 5000:
#             pw = 5000
#
#         return pw
#
#     return inner


