import Global


def runRefPlay(curRefMsg: str):
    """
    根据实际下发的裁判盒信息进行战术映射
    :param curRefMsg:
    :return:
    """
    match curRefMsg:
        case "GameHalt":
            Global.gameStrategies["GameHalt"].runStrategy()
        case "Ref_Halt": # 感觉实际上并不会下发？
            Global.gameStrategies["GameHalt"].runStrategy()
        case "GameStop":
            Global.gameStrategies["GameStop"].runStrategy()
        case "OurBallPlacement":
            Global.gameStrategies["BallPlace"].runStrategy()
        case "OurIndirectKick":
            Global.gameStrategies["ourIndirectKick"].runStrategy()
        case "OurKickOff":
            Global.gameStrategies["KickOff"].runStrategy()
        case "OurPenaltyKick":
            Global.gameStrategies["PenaltyKick"].runStrategy()
        case "OurTimeout":
            Global.gameStrategies["TimeOut"].runStrategy()
        case "TheirBallPlacement":
            Global.gameStrategies["BallPlace"].runStrategy()
        case "TheirIndirectKick":
            Global.gameStrategies["theirIndirectKick"].runStrategy()
        case "TheirKickOff":
            Global.gameStrategies["KickOffDef"].runStrategy()
        case "TheirPenaltyKick":
            Global.gameStrategies["theirPenaltyKick"].runStrategy()
        case _:
            # GameOver已经弃用
            raise ValueError("Not supported referee massage!")