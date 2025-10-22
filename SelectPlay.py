# 这边是由Medusa初始化之后每帧反复频繁调用的脚本
# 调试技巧 vs code ctrl+shift+P 选择python版本！这很重要！版本要与编译的一致！！
from __future__ import annotations

import os
import sys
from pathlib import Path

import CppPackage
import Global
import Vision
from GameControl.Referee import runRefPlay
from Utils import DebugColor
from WorldModel import worldModel

# 当前脚本 所在路径
current_file_path = Path(__file__).resolve()

# 构造 dll 所在目录路径
dll_path = current_file_path.parent.parent  # 即ZBin/

if hasattr(os, "add_dll_directory"): 
    os.add_dll_directory(str(dll_path))
# dll_path = r"D:\Documents\SRCrobocup\MilkForPython\ZBin"
# os.add_dll_directory(r"D:\Documents\SRCrobocup\MilkForPython\ZBin")
# import CppPackage.Strategy.Skill as Skill
# print(dir(Skill))

script_dir = Path("./PythonScripts").resolve()
# sys.path.append(r"D:\Documents\SRCrobocup\MilkForPython\ZBin\PythonScripts")  # 将当前目录添加到搜索路径
sys.path.append(str(current_file_path))  # 将当前目录添加到搜索路径
sys.path.append(str(dll_path))
# sys.path.append(r"D:\Documents\SRCrobocup\MilkForPython\ZBin\PythonScripts\CppPackage") 
# sys.path.append(r"D:\Documents\SRCrobocup\MilkForPython\ZBin") 


from Geometry import *
from Global import debugEngine
from Vision import Ball


lastRefereeMessage = ""

# gNormalPlay = Global.GameStrategies["NormalPlay"] # gOppoConfig 已经更名为GameStrategy，在Config.py中设置，NorPlay更名为NormalPlay
# gNormalPlay弃用，体系不同，无法通过table获取Play的状态机，直接在Config.py中定义即可

# gNextPlay已经弃用，不信可以搜索gNextPlay和SetNextPlay函数的调用情况
# gTimeCounter已经弃用，用于timeOut控制，改为自行在StateMachine中控制

def isRefereePlay():
    """
    判断是不是裁判盒控制的Play
    :return:如果为true则由裁判盒控制，不需要下面的SelectPlay进入正常打的脚本
    """
    global lastRefereeMessage
    # needCancelRefPlay = False # 已经弃用
    curRefMsg = Vision.VisionModule.Instance().getCurrentRefereeMsg()  # 获取当前裁判消息
    debugEngine.gui_debug_msg(CGeoPoint(1000, 1000), curRefMsg)  # 在界面上显示当前裁判消息

    if curRefMsg == "":
        # 没有裁判消息，直接返回
        lastRefereeMessage = curRefMsg
        return False

    # 剩下都是需要RefereePlay的case
    if lastRefereeMessage != curRefMsg or curRefMsg == "GameStop":
        # 裁判消息发生变化或进入GameStop，更新球的裁判消息
        Ball.updateRefMsg()
    # curRealMsg = Vision.VisionModule.Instance().getCurrentRefereeMsg() # 神奇的sb语句
    if curRefMsg in ["OurBallPlacement", "TheirBallPlacement"]:
        # 进入摆球阶段，更新摆球位置
        Ball.updateRef2PlacePos()

    # 执行当前裁判消息对应的脚本
    # RunRefScript(curRefMsg) # todo:派人新增ref脚本,改为referee()
    lastRefereeMessage = curRefMsg
    return True


def ResetPlay():
    """
    战术重置流程。在切换不同的Play脚本的时候进行，比如NormalPlay->RefPlay。
    清空防守信息，切换到战术初始状态，并分配角色。
    """
    # global gCurrentState, gTimeCounter
    # curPlay = gPlayTable[name]
    worldModel.SPlayFSMSwitchClearAll(True)
    Global.resetRoleNumbersTableBetweenPlays()
    # WorldModel().clearBallStateCouter() #已经弃用，因为lua层的绑定都不正确
    defenceInfo = CppPackage.DefenceInfo.Instance()
    defenceInfo.clearAll()
    defenceInfo.clearNoChangeFlag()
    defenceInfo.resetMarkingInfo()


def SelectPlay():
    # 主流程：优先处理裁判指令，否则进入常规战术流程
    curRealMsg = Vision.VisionModule.Instance().getCurrentRefereeMsg()
    # print(curRealMsg)   # 获取当前裁判消息
    # return  # 先屏蔽掉，等裁判盒流程完善了再放开
    displayPos = CGeoPoint(2018, 3287) # 显示当前模式的位置
    if Global.isTestMode:
        debugEngine.gui_debug_msg(displayPos, "Test Mode Now!", debug_color=DebugColor.Yellow)  # 在界面上显示当前裁判消息
        from Config import testStrategy
        testStrategy.runStrategy()
        return
    elif isRefereePlay():
        debugEngine.gui_debug_msg(displayPos,  f"Referee: {curRealMsg}", debug_color=DebugColor.Yellow)  # 在界面上显示当前裁判消息
        Global.currentPlayName = curRealMsg
        runRefPlay(curRealMsg)
    else:
        Global.currentPlayName = "NormalPlay"
        debugEngine.gui_debug_msg(displayPos, "NormalPlay!")  # 在界面上显示当前裁判消息
        Global.gameStrategies["NormalPlay"].runStrategy()

    if Global.currentPlayName != Global.lastPlayName:
        Global.isPlaySwitched = True
        ResetPlay()
        Global.lastPlayName = Global.currentPlayName
    else:
        Global.isPlaySwitched = False

"""
传统的诸如Messi11vs11是通过：
gPlayTable.CreatePlay{
    firstState = "GetBall",
    ...
    name = "NormalPlayMessi_11vs11_new",    
}
开始状态机的书写的，也顺便把这个play注册到了gPlayTable，取用的时候直接通过str即可获取状态机的所有信息
"""
