# 类比Config.lua，用于配置变量，尽量不定义变量
import copy

import Global
from Play.Test.Test_GetBall import Test_GetBall
from Play.RefPlay import *
# from Play.Normal.NormalPlay_3vs3_wyz import NormalPlay_3vs3_wyz
# from Play.Normal.Wyz_v2 import Wyz_v2
from Play.Normal.Defend import Defend
from Play.Normal.Jyz_v8 import Jyz_v8 
from Play.Normal.Wyz_v7 import Wyz_v7
from Play.Normal.NoPass import NoPass
# from Play.Normal.Test111 import Test111
# from Play.Normal.TestPass import TestPass

Global.isSmallField = True  # 是否为小场地比赛
Global.isTestMode = False  # test mode下不会受到裁判盒控制
Global.needDetailedRuntimeDebugInfo = False

class GameStrategy:  # 类似c++的结构体而已，封装一下，后面可能新增参数，使得用法更加多样
    def __init__(self, blueTeam, yellowTeam=None):
        """

        :param blueTeam:
        :param yellowTeam: 可以省略，此时blue和yellow使用同一个策略
        """
        self.blueTeam = blueTeam
        if not yellowTeam:
            self.yellowTeam = blueTeam
        else:
            self.yellowTeam = yellowTeam

    def runStrategy(self):
        if Global.isYellow:
            self.yellowTeam.planTasks()
        else:
            self.blueTeam.planTasks()

# 这些Import必须放在Config.py的后面，gameStrategies调整的前面，否则会引起循环import
from Play.Normal.NormalPlay_3vs3 import NormalPlay_3vs3
from Play.RefPlay import *

Global.gameStrategies = {
    # 从Other.lua中迁移过来，对应脚本的原始关系参照Other.lua
    # -------------------------Normal Play--------------------------------------------
    "NormalPlay": GameStrategy(NoPass(), Wyz_v7()),
    # NorPlay更名为NormalPlay "NormalPlayMessi_11vs11_new",   # "NormalPlayMessi_8vs8tozju", # "NormalPlayMessi_8vs8tozju",

    # -------------------------Kick--------------------------------------------
    "KickOff": GameStrategy(Test_GetBall(),Test_GetBall()),  # 接近球也是开球启动程序
    "KickOffDef": GameStrategy(KickOff_2023(),NormalPlay_3vs3()),  # 完成

    "FreeKick": GameStrategy(DirectKick_2023(),DirectKick_2023()),
    "FreeKickDef": GameStrategy(InDirectKick_2023(),InDirectKick_2023()),

    "ourDirectKick": GameStrategy(DirectKick_2023(),NormalPlay_3vs3()),
    "ourIndirectKick": GameStrategy(DirectKick_2023(),DirectKick_2023()),
    "theirDirectKick": GameStrategy(InDirectKick_2023(),InDirectKick_2023()),
    "theirIndirectKick": GameStrategy(InDirectKick_2023(),InDirectKick_2023()),

    # ---------------------Penalty-----------------------------------
    "PenaltyKick": GameStrategy(PenaltyKick()),  # 强队用V0，弱队用V1，大点球用V3，已调试,1
    "theirPenaltyKick": GameStrategy(PenaltyDefend()),  # 大点球用V1，小点球V0


    # ------------------- Other ------------------------------------------------
    "BallPlace": GameStrategy(BallPlace()),
    "TimeOut": GameStrategy(OurTimeout()),
    "GameStop": GameStrategy(GameStop_2023(),GameStop_2023()),
    # "GameOver":    "Ref_GameOverV2",              # GameOver裁判盒不会发送，已经弃用 # 省赛用V1 国赛用V2
    "GameHalt": GameStrategy(GameHalt()),
    "IfHalfField": False,
    "USE_ZPASS": False,
}

testStrategy = GameStrategy(Test_GetBall())

# 这边可以调整守门员等默认编号
Global.goalieNumber = 0
Global.defaultRoleNumberStructTable["G"] = Global.RoleNumberStruct(Global.RoleNumberStruct.MatchType.Fixed,
                                                                   Global.goalieNumber)  # 守门员G号固定为1
