from RoleMatch_LuaStyle.Archive.RoleMatch import *

class MetaAddList(list):
    def __add__(self, other):
        return MetaAddList(super().__add__(other))

gPlay = MetaAddList()
gPlay += gRefPlayTable + gTestPlayTable + gBayesPlayTable  # 合并所有战术表，形成完整战术列表

gPlayTable = {}           # 存储所有战术的详细定义（字典结构，key为战术名）
gTimeCounter = 0          # 当前状态持续的周期计数
gCurrentState = ""        # 当前状态名（如"attack"、"defend"等）
gLastState = ""           # 上一状态名
gLastPlay = ""            # 上一战术名
gCurrentPlay = ""         # 当前战术名
gNextPlay = ""            # 下一个预设战术名
gRealState = ""           # 实际执行的状态名（有时与gCurrentState不同）
gLastCycle = 0            # 上一帧的周期号
gLastRefMsg = ""          # 上一条裁判消息
gActiveRole = []          # 当前激活的角色列表
gIsRefPlayExit = False    # 是否已退出裁判流程

gCurrentBallStatus = "None"   # 当前球状态
gLastBallStatus = ""          # 上一球状态
gCurrentFieldArea = "BackField"  # 当前场地区域
gLastFieldArea = ""              # 上一场地区域

gExternStopCycle = 0         # 外部停止周期计数
gExternExitCycle = 0         # 外部退出周期计数

def Next():
    # 轮流返回gPlay中的下一个战术（循环队列）
    index = [0]
    def inner():
        index[0] += 1
        return gPlay[(index[0]) % len(gPlay)]
    return inner

def CreatePlay(spec):
    # 注册一个战术spec到gPlayTable，spec需包含name、applicable、attribute、timeout等字段
    assert isinstance(spec['name'], str)
    assert spec.get('applicable') is not None
    assert spec.get('attribute') is not None
    assert isinstance(spec['timeout'], (int, float))
    # 对spec中的每个属性，如果有match字段则进行解码
    for attr, attr_table in spec.items():
        if isinstance(attr_table, dict):
            if 'match' in attr_table:
                attr_table['match'] = DecodeMatchStr(attr_table['match'])
    gPlayTable[spec['name']] = spec
    return spec

def IsRoleActive(rolename):
    # 判断某角色当前是否激活（在gActiveRole中）
    return rolename in gActiveRole

def UsePenaltyCleaner(curPlay):
    # 清理禁区内的机器人位置，防止违规
    for rolename, task in curPlay[gRealState].items():
        if isinstance(task, dict) and rolename not in ["match", "Goalie", "Leader"]:
            # 获取角色当前位置
            if callable(gRolePos.get(rolename)):
                p = gRolePos[rolename]()
            else:
                p = gRolePos[rolename]
            # 添加到禁区清理器
            CAddPenaltyCleaner(rolename[0], gRoleNum[rolename], p.x(), p.y())
    CCleanPenalty()  # 执行清理
    for rolename, task in curPlay[gRealState].items():
        if isinstance(task, dict) and rolename not in ["match", "Goalie", "Leader"]:
            x, y = CGetPenaltyCleaner(rolename[0])
            gRolePos[rolename] = CGeoPoint(x, y)
    DoRoleMatchReset(CGetResetMatchStr())  # 重置角色分配

def DoRolePosMatch(curPlay, isPlaySwitched, isStateSwitched):
    """
    角色-位置分配主流程。根据当前战术状态，统计激活角色，并更新gRolePos和gActiveRole。
    同时调用UpdateRole进行机器人编号分配。
    **这个函数有两处被调用！分别是play还没有切换的时候，还有一个是切换状态之后**
    :param curPlay:
    :param isPlaySwitched: 是否发生了战术切换，比如根据裁判盒切换了运行脚本了
    :param isStateSwitched: 是否发生了状态切换，用于对于{}这种进入该状态只匹配一次的情形
    前面两个参数都是直接往下传给UpdateRole的，这一层并未使用
    """
    global gRealState, gActiveRole
    if gCurrentState in ["exit", "finish"]:
        gRealState = gLastState
    else:
        gRealState = gCurrentState
    gActiveRole = []
    # 解包matchPos和task
    for rolename, itask in curPlay[gRealState].items():
        # 若任务为函数且不是match/switch，先执行
        if callable(itask) and rolename not in ["match", "switch"]:
            itask = itask()
        if callable(rolename):
            rolename = rolename()
        # 只处理有效角色
        if isinstance(itask, dict) and isinstance(rolename, str) and rolename != "match":
            gActiveRole.append(rolename)
            # 若任务为"continue"，则继承上一状态的任务，感觉很少人会使用这个吧？
            if itask.get('name') == "continue" and gCurrentState not in ["exit", "finish"]:
                curPlay[gRealState][rolename] = []
                for v in curPlay[gLastState][rolename]:
                    curPlay[gRealState][rolename].append(v)
                    itask.append(v)
                curPlay[gRealState][rolename].name = "continue"
            # 更新角色目标位置（matchPos）
            gRolePos[rolename] = itask[2]
    # 进行机器人编号分配
    UpdateRole(curPlay[gRealState]['match'], isPlaySwitched, isStateSwitched)

def SetNextPlay(name):
    # 设置下一个预设战术
    global gNextPlay
    gNextPlay = name

def ResetPlay(name):
    """
    战术重置流程。清空防守信息，切换到战术初始状态，并分配角色。
    """
    global gCurrentState, gTimeCounter
    curPlay = gPlayTable[name]
    world.SPlayFSMSwitchClearAll(True)
    defenceInfo.clearAll()
    defenceInfo.clearNoChangeFlag()
    defenceInfo.resetMarkingInfo()
    # 下面语句已弃用，改成StateMachine自己控制初始化逻辑
    if curPlay.get('firstState') is not None:
        gCurrentState = curPlay['firstState']
        DoRolePosMatch(curPlay, True, False) #初始化第一次匹配的时候
    else:
        print("Error in ResetPlay!!")
    gTimeCounter = 0 # 已弃用，改成StateMachine自己控制超时逻辑

def ResetPlayWithLastMatch(name):
    """
    战术重置流程（保留上一次角色分配），常用于gNextPlay切换。
    """
    global gCurrentState, gTimeCounter
    curPlay = gPlayTable[name]
    world.SPlayFSMSwitchClearAll(True)
    if curPlay.get('firstState') is not None:
        gCurrentState = curPlay['firstState']
    else:
        print("Error in ResetPlay!!")
    gTimeCounter = 0

def RunPlay(name):
    """
    战术主循环。根据当前状态和切换条件，执行状态切换、角色分配和任务分配。
    传入的name示例：NormalPlayMessi_11vs11_new
    """
    global gLastState, gCurrentState, gTimeCounter, gLastCycle
    if gPlayTable.get(name) is None:
        print("Error In RunPlay: " + name)
        return
    debugEngine.gui_debug_msg(CGeoPoint(0, 2000), gCurrentPlay)
    curPlay = gPlayTable[name]
    curState = None
    isStateSwitched = False
    # 状态切换判断
    if curPlay.get('switch') is not None:
        curState = curPlay['switch']() # 执行switch函数
    else:
        if gCurrentState not in ["exit", "finish"]:
            curState = curPlay[gCurrentState]['switch']()
    if curState is not None:
        gLastState = gCurrentState
        gCurrentState = curState
        isStateSwitched = True
        world.SPlayFSMSwitchClearAll(True)
    # 角色分配与位置分配
    DoRolePosMatch(curPlay, False, isStateSwitched)
    gExceptionNum = {}
    kickStatus.clearAll()
    # 遍历所有激活角色，分配具体任务
    for rolename, task in curPlay[gRealState].items():
        # 若任务为函数，先执行
        if callable(task) and rolename != "match" and (gRoleNum.get(rolename) is not None or callable(rolename)):
            task = task(gRoleNum[rolename])
        # 若任务为字典，且角色编号有效，执行具体动作
        if isinstance(task, dict) and rolename != "match" and (gRoleNum.get(rolename) is not None or callable(rolename)):
            if task.get(1) is None:
                task = curPlay[gLastState][rolename] # 复用上一状态的任务分配
            if isinstance(rolename, str):
                roleNum = gRoleNum[rolename]
            elif callable(rolename):
                roleNum = rolename()
            else:
                roleNum = None
            if roleNum != -1:
                # 处理踢球、带球等动作指令,
                # todo:可以改成在Task类初始化的时候新增**kwargs参数?感觉这一部分就是屎山的多余
                # 或者新增一个global？或者Task类的字段self.taskRequirements，然后单独对这个进行处理
                # 已弃用。在task.lua中返回值不是{mexe, mpos}的，都是通过这种方式在Play中单独设置踢球等开关，相当于纯写python层直接对底层进行控制。如果后人真要实现，那么就skill的返回值增加一个tuple[2]中的extraParams的dict，如果里面有对应的值则进行处理
                if task.get(3) is not None:
                    mkick = task[3](roleNum)
                    mdir = task[4](roleNum)
                    mpre = task[5](roleNum)
                    mkp = task[6](roleNum)
                    mcp = task[7](roleNum)
                    mflag = task[8]
                    isDirOk = world.KickDirArrived(vision.getCycle(), mdir, mpre, roleNum)
                    needDribble = bit._and(mflag, flag.dribbling)
                    if needDribble != 0:
                        dribbleStatus.setDribbleCommand(roleNum, 3)
                    if isDirOk or bit._and(mflag, flag.force_kick) != 0:
                        if mkick == kick.flat():
                            kickStatus.setKick(roleNum, mkp)
                        elif mkick == kick.chip():
                            kickStatus.setChipKick(roleNum, mcp)
                # 在界面上显示角色首字母
                if isinstance(rolename, str):
                    debugEngine.gui_debug_msg(vision.ourPlayer(roleNum).Pos(), rolename[0])
                # 执行角色的主任务，这就是我们直接返回的CppPackage里面的那个makeIt函数，是在处理完Task包装的参数之后调用的！
                task[1](roleNum)
    gTimeCounter += 1 #已经弃用，原lua中只用于timeOut状态的控制
    gLastCycle = vision.getCycle() #已经弃用


def NeedExit(name):
    """
    通过文件中定义的time out、finish等的额外判断是否超时退出
    **已经弃用**，改成StateMachine自己控制
    判断当前战术是否需要退出（如超时、状态为exit/finish、长时间无响应等）。
    """
    global gTimeCounter
    if name == "":
        return False
    if gPlayTable.get(name) is None:
        print("Error Skill Name In NeedExit: " + name)
        return False
    curPlay = gPlayTable[name]
    # 满足退出条件则返回True
    if gCurrentState in ["finish", "exit"] or \
            gTimeCounter > curPlay['timeout'] or \
            vision.getCycle() - gLastCycle > param.frameRate * 0.1:
        gTimeCounter = 0
        return True
    return False