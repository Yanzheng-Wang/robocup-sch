# gNormalPlay = gOppoConfig.NorPlay
import Global
from RoleMatch_LuaStyle import *

# gNormalPlay = gOppoConfig.NorPlay  # 当前默认常规战术，由配置文件决定
gNormalPlay = Global.GameStrategies["NormalPlay"]  # 当前默认常规战术，由配置文件决定

def RunRefScript(name):
    # 根据裁判消息名称，动态执行对应的裁判脚本
    filename = f"./lua_scripts/play/Ref/{name}.py"
    exec(open(filename, encoding='utf-8').read(), globals())

def SelectRefPlay():
    """
    裁判指令主流程，根据当前裁判消息决定是否切换战术或执行裁判脚本
    """
    global gLastRefMsg, gIsRefPlayExit
    curRefMsg = vision.getCurrentRefereeMsg()  # 获取当前裁判消息
    debugEngine.gui_debug_msg(CGeoPoint(1000, 1000), curRefMsg)  # 在界面上显示当前裁判消息
    if curRefMsg == "":
        # 没有裁判消息，直接返回
        gLastRefMsg = curRefMsg
        return False
    # 在球的参考位置画三个同心圆，辅助调试
    debugEngine.gui_debug_arc(ball().refPos(), 6, 0, 360, 3)
    debugEngine.gui_debug_arc(ball().refPos(), 8, 0, 360, 3)
    debugEngine.gui_debug_arc(ball().refPos(), 10, 0, 360, 3)
    if gLastRefMsg != curRefMsg or curRefMsg == "GameStop":
        # 裁判消息发生变化或进入GameStop，更新球的裁判消息
        ball().updateRefMsg()
    curRealMsg = vision.getCurrentRefereeMsg()
    if curRealMsg in ["OurBallPlacement", "TheirBallPlacement"]:
        # 进入摆球阶段，更新摆球位置
        ball().updateRef2PlacePos()
    if gLastRefMsg == curRefMsg and gNextPlay != "":
        # 如果裁判消息未变但是已经有了下一个战术，标记裁判流程已退出
        # 由于gNextPlay已经弃用，gNextPlay始终为空，所以这个判断分支弃用！！！
        gIsRefPlayExit = True
    if gLastRefMsg != curRefMsg:
        # 裁判消息变化，重置退出标记
        gIsRefPlayExit = False
    if gIsRefPlayExit:
        # 已退出裁判流程，不再执行裁判脚本
        gLastRefMsg = curRefMsg
        return False
    # 执行当前裁判消息对应的脚本
    RunRefScript(curRefMsg)
    gLastRefMsg = curRefMsg
    return True

def SelectBayesPlay():
    """
    贝叶斯战术选择流程，主要用于常规战术的切换和重置
    """
    global gCurrentPlay
    # if gNormalPlay == "NormalPlayMessi":
    # 如果当前常规战术为Messi，清空球状态计数器
    if gNormalPlay == "NormalPlayMessi":
        world.clearBallStateCouter()
    gCurrentPlay = gNormalPlay
    ResetPlay(gCurrentPlay)  # 重置当前战术

# 主流程：优先处理裁判指令，否则进入常规战术流程
if SelectRefPlay():
    # 如果当前战术发生变化或需要退出，重置战术
    if gCurrentPlay != gLastPlay or NeedExit(gCurrentPlay):
        ResetPlay(gCurrentPlay)
        if vision.getCurrentRefereeMsg() != "":
            gIsRefPlayExit = True
        print("New Play: " + str(gCurrentPlay))
else:
    # 没有裁判指令时，优先处理gNextPlay（下一个预设战术）
    if gNextPlay != "":
        gCurrentPlay = gNextPlay
        print("JINP: " + str(gCurrentPlay))
        if gCurrentPlay != gLastPlay or NeedExit(gCurrentPlay):
            ResetPlayWithLastMatch(gCurrentPlay)
    elif IS_TEST_MODE:
        # 测试模式下，显示TEST_MODE提示，并切换到测试战术
        debugEngine.gui_debug_msg(
            CGeoPoint(param.pitchLength / 2 - 1500, param.pitchWidth / 2), "TEST_MODE", 0)
        if gLastPlay == "" or NeedExit(gCurrentPlay):
            gCurrentPlay = gTestPlay
        if gCurrentPlay != gLastPlay or NeedExit(gCurrentPlay):
            ResetPlay(gCurrentPlay)
    else:
        # 常规战术流程，更新球和场地状态
        if gNormalPlay in [
            "NormalPlayPass", "NormalPlayPP", "NormalPlayMessi",
            "NormalPlayMessi_6vs6", "NormalPlayMessi_8vs8", "NormalPlayDefend"
        ]: # 什么傻逼代码，这边加装一层判断是为了防止拼写错误吗？
            # world.setBallHandler(gRoleNum["Kicker"])  # 可选：设置控球机器人
            gLastBallStatus = gCurrentBallStatus
            gCurrentBallStatus = cond.getBallStatus()
            gLastFieldArea = gCurrentFieldArea
            gCurrentFieldArea = cond.judgeFieldArea()
        # 如果战术首次进入或需要退出，重新选择常规战术
        if gLastPlay == "" or NeedExit(gCurrentPlay):
            if NeedExit(gCurrentPlay):
                print("Play: " + str(gCurrentPlay) + " Exit!!")
            SelectBayesPlay()

if gCurrentPlay != gLastPlay:
    # 战术切换时可在此处添加重置逻辑（TODO）
    pass

# 更新战术状态，准备下一轮
gLastPlay = gCurrentPlay # 在 SelectBayesPlay 设置为NormalPlay
gNextPlay = ""
debugEngine.gui_debug_msg(
    CGeoPoint(-param.pitchLength / 2, param.pitchWidth / 2 + 200), gCurrentPlay)
RunPlay(gCurrentPlay)  # 执行当前战术
gLastTask = gRoleTask
gRoleTask = {}

debugEngine.gui_debug_msg(
    CGeoPoint(-param.pitchLength / 2, param.pitchWidth / 2 + 50), gCurrentState)