import Global
import Config
if Global.isSmallField:
    maxPlayer   = 16
    pitchLength = 9000
    pitchWidth  = 6000
    goalWidth = 1000
    goalDepth = 180
    freeKickAvoidBallDist = 500
    playerRadius	= 90
    penaltyWidth    = 2000
    penaltyDepth	= 1000
    penaltyRadius	= 1800
    penaltySegment	= 500
    playerFrontToCenter = 76
    lengthRatio	= 1.5
    widthRatio	= 1.5
    stopRatio = 1.1
    frameRate = 75
else: # 大场地参数
    maxPlayer   = 13
    pitchLength = 12000
    pitchWidth  = 8550
    goalWidth = 1800
    goalDepth = 180
    freeKickAvoidBallDist = 500
    playerRadius	= 90
    penaltyWidth    = 3600
    penaltyDepth	= 1800
    penaltyRadius	= 1800
    penaltySegment	= 500
    playerFrontToCenter = 76
    lengthRatio	= 1.5
    widthRatio	= 1.5
    stopRatio = 1.1
    frameRate = 75