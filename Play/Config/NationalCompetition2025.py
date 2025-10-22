"""
来源于原lua的opponent/Other.lua中的战术配置

"""
GameStrategy = {
    # -------------------------Play--------------------------------------------
    "KickOff":     "Ref_KickOff_11vs11",      # 接近球也是开球启动程序
    "KickOffDef":  "Ref_KickOffDef11vs11",    # 完成

    "FreeKick":    "Ref_FreeKick_11vs11",
    "FreeKickDef": "Ref_FreeKickDef_11vs11",

    # ---------------------Penalty and Normal-----------------------------------
    "PenaltyKick": "Ref_BIGPenaltyKick_11vs11",    # 强队用V0，弱队用V1，大点球用V3，已调试,1
    "PenaltyDef":  "Ref_PenaltyDef_11vs11",        # 大点球用V1，小点球V0

    "NorPlay":     "NormalPlayMessi_11vs11_new",   # "NormalPlayMessi_8vs8tozju",

    "BallPlace":   "Ref_BallPlace_11vs11_new",

    # ------------------- Other ------------------------------------------------
    "TimeOut":     "Ref_OurTimeout_11vs11",
    "GameStop":    "Ref_Stop_11vs11",
    "GameOver":    "Ref_GameOverV2",              # 省赛用V1 国赛用V2
    "IfHalfField": False,
    "USE_ZPASS": False,
}