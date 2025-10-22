from WorldModel import Params

gRoleNum = {
    "Goalie": -1, "Kicker": -1, "Assister": -1, "Special": -1, "Defender": -1, "Middle": -1,
    "Leader": -1, "Tier": -1, "Breaker": -1, "Fronter": -1, "Receiver": -1, "Center": -1,
    **{chr(i): -1 for i in range(ord('a'), ord('z') + 1)}
}

gLastRoleNum = {}
gRolePos = {} # table,对应每个角色的matchPos是什么。比如"A": CGeoPoint(100,200)
gRolePriority = ["Goalie", "Tier"]
gOurExistNum = [-1] * 12  # 假设最大12个机器人

gRoleLookUpTable = {
    # "G": "Goalie", "K": "Kicker", "T": "Tier", "R": "Receiver",
    # "A": "Assister", "S": "Special", "D": "Defender", "M": "Middle",
    # "L": "Leader", "B": "Breaker", "F": "Fronter", "C": "Center",
    **{chr(i): chr(i) for i in range(ord('A'), ord('Z') + 1)}
}

def DecodeMatchStr(matchRule):
    """
    str转为分配规则列表

    输入输出示例：
In[11]: DecodeMatchStr("[AB]{CD}(E)")
Out[11]:
[{'mode': 'RealTime', 'roles': ['A', 'B']},
 {'mode': 'Never', 'roles': ['C', 'D']},
 {'mode': 'Once', 'roles': ['E']}]
    :param matchRule:
    :return:
    """
    strTable = []
    teamCnt = 0
    if callable(matchRule):
        return matchRule
    elif isinstance(matchRule, str):
        s = matchRule
    else:
        print("RoleMatch:not a valid matchRule type!!")
        return []
    while s:
        character = s[0]
        if character == '[':
            endChar, mode = ']', "RealTime"
        elif character == '(':
            endChar, mode = ')', "Once"
        elif character == '{':
            endChar, mode = '}', "Never"
        else:
            break
        endPos = s.find(endChar)
        teamTable = [gRoleLookUpTable.get(c, c) for c in s[1:endPos]]
        teamTable = list(teamTable)
        teamTable.append(("mode", mode))
        strTable.append(teamTable)
        s = s[endPos+1:]
        if not s:
            break
    # 转换为dict结构
    result = []
    for team in strTable:
        mode = None
        if isinstance(team[-1], tuple) and team[-1][0] == "mode":
            mode = team[-1][1]
            team = team[:-1]
        result.append({"mode": mode, "roles": team})
    return result

def GetMatchPotential(num, role):
    # 依赖外部 world, player
    if callable(gRolePos.get(role)):
        targetPos = gRolePos[role](num)
    else:
        targetPos = gRolePos.get(role)
    t = world.timeToTarget(num, targetPos) * 10
    t2 = t ** 5
    playerPos = player.pos(num)
    # if DEBUG_MATCH:
    #     debugEngine.gui_debug_line(targetPos, playerPos, 4)
    #     debugEngine.gui_debug_msg(playerPos + (targetPos - playerPos) / 3, "%.2f" % t, 3)
    return t2

def RemoveExistNum(num):
    # 将编号为num的机器人标记为不可用（已分配或移除），-1表示不可用/已经分配了
    gOurExistNum[num] = -1

def DoRoleMatchReset(s):
    # 该函数用于根据字符串s重置角色与机器人编号的分配关系
    # s的格式如"[GKAT]"，表示需要分配的角色集合
    while s:
        character = s[0]
        if character != '[':
            # 只处理以'['开头的分配段，遇到其他字符则退出
            break
        endPos = s.find(']')
        # 解析出本段需要分配的角色列表（如['G', 'K', 'A', 'T']）
        roleTable = [gRoleLookUpTable.get(c, c) for c in s[1:endPos]]
        # 获取这些角色当前对应的机器人编号（-1表示未分配）
        numTable = [gRoleNum.get(r, -1) for r in roleTable]
        nrows, ncols = len(roleTable), len(numTable)
        # 构建一个nrows行ncols列的代价矩阵，行表示角色，列表示机器人编号
        matrix = Matrix_double_(nrows, ncols)
        for row in range(nrows):
            for col in range(ncols):
                # 计算numTable[col]号机器人分配给roleTable[row]角色的代价
                matrix.setValue(row, col, GetMatchPotential(numTable[col], roleTable[row]))
        # 使用Munkres算法（匈牙利算法）进行最优分配
        m = Munkres()
        m.solve(matrix)
        # 遍历分配结果，找到代价为0的分配对，进行角色与机器人编号的绑定
        for row in range(nrows):
            for col in range(ncols):
                if matrix.getValue(row, col) == 0:
                    gRoleNum[roleTable[row]] = numTable[col]
                    break
        # 处理下一个分配段（如果有）
        s = s[endPos+1:]
        if not s:
            break

def DoMunkresMatch(rolePos):
    # 获取需要分配的角色数量
    nrows = len(rolePos)
    ncolsIndex = []
    ncols = 0
    # 统计当前可用的机器人编号（gOurExistNum中不为-1的下标）
    for i, val in enumerate(gOurExistNum):
        if val != -1:
            ncols += 1
            ncolsIndex.append(i)
    # 创建一个nrows行ncols列的矩阵，用于存储每个机器人与每个角色的匹配代价
    matrix = Matrix_double_(nrows, ncols)
    for row in range(nrows):
        for col in range(ncols):
            # 计算机器人gOurExistNum[ncolsIndex[col]]与rolePos[row]角色的匹配代价
            matrix.setValue(row, col, GetMatchPotential(gOurExistNum[ncolsIndex[col]], rolePos[row]))
    # 使用Munkres算法（匈牙利算法）求解最优分配
    m = Munkres()
    m.solve(matrix)
    eraseList = []
    # 遍历分配结果，找到分配成功（代价为0）的机器人-角色对
    for row in range(nrows):
        for col in range(ncols):
            if matrix.getValue(row, col) == 0:
                # 记录分配结果：将机器人编号分配给对应角色
                gRoleNum[rolePos[row]] = gOurExistNum[ncolsIndex[col]]
                # 记录已分配的机器人编号，后续需要从可用列表中移除
                eraseList.append(gOurExistNum[ncolsIndex[col]])
                break
    # 从可用机器人编号列表中移除已分配的机器人
    for value in eraseList:
        RemoveExistNum(value)

def DoFixNumMatch(fixNums):
    # 固定分配函数：尝试将fixNums中的机器人编号分配出去
    # fixNums: 需要固定分配的机器人编号列表
    for fixNum in fixNums:
        for i, val in enumerate(gOurExistNum):
            if val == fixNum:
                # 找到后将其标记为已分配（-1），并返回其索引
                gOurExistNum[i] = -1
                return i
    # 没有找到可用的固定编号，返回-1
    return -1

def SetNoMatchRoleZero():
    # 将所有未分配编号的角色（gRoleNum值为None）统一设置为-1
    for rolename in gRoleLookUpTable.values():
        if gRoleNum.get(rolename) is None:
            gRoleNum[rolename] = -1

def UpdateRole(matchTactic, isPlaySwitched, isStateSwitched):
    """
    角色分配主流程，根据当前战术、状态切换等情况，动态分配机器人编号到各角色。
    matchTactic: 当前战术分配规则（字符串或函数）
    isPlaySwitched: 是否发生了战术切换，比如根据裁判盒切换了运行脚本了
    isStateSwitched: 是否发生了状态切换，用于对于{}这种进入该状态只匹配一次的情形
    """
    global gRoleNum, gLastRoleNum
    if isPlaySwitched:
        # 战术切换时清空角色分配表
        # 已经提前到外部处理，感觉不是这个类的职责啊！
        gRoleNum = {}
    # 重新初始化可用机器人编号列表，只有有效的机器人编号才可用
    # for i in range(len(gOurExistNum)):
    for i in range(Params.maxPlayer - 1):
        if player.valid(i):
            gOurExistNum[i] = i
        else:
            gOurExistNum[i] = -1
    # 优先分配优先级角色（如守门员、Tier等），进行固定编号分配
    # 原来priority是优先的角色的意思！！！
    for roleName in gRolePriority:
        for existname in gRolePos:
            if roleName == existname and isinstance(gRoleFixNum[roleName], list):
                gRoleNum[roleName] = DoFixNumMatch(gRoleFixNum[roleName])
                if roleName == "Goalie":
                    # 特殊处理守门员角色，注册守门员编号
                    CRegisterRole(gRoleNum[roleName], "goalie")
    matchList = []
    # 如果战术分配规则是函数，先解码为分配结构
    if callable(matchTactic):
        matchTactic = DecodeMatchStr(matchTactic())
    # todo:这边是核心，根据部分算法自己重写逻辑即可。下面的全是屎山代码
    # 遍历所有分配规则，按模式决定是否需要重新分配
    for matchGroup in matchTactic:
        mode = matchGroup.get("mode")
        roles = matchGroup.get("roles")
        # 实时分配、战术切换、状态切换（且模式为Once）时，加入待分配列表
        if mode == "RealTime" or isPlaySwitched or (isStateSwitched and mode == "Once"):
            matchList.append(roles)
        else:
            # 否则沿用上一次分配结果，并将已分配编号从可用列表移除
            for roleName in roles:
                gRoleNum[roleName] = gLastRoleNum.get(roleName, -1)
                RemoveExistNum(gRoleNum[roleName])
    # 对所有需要重新分配的角色组，进行分配
    # note: 这边就是涉及到角色组如何处理的算法了
    for matchGroup in matchList:
        role = []
        for index, roleName in enumerate(matchGroup):
            """
            比如
            matchList = [['A', 'B'], ['C', 'D'], ['E']]
            matchGroup = ["A","B"]（第一次循环）
            则index和roleName分别为0、"A"和1、"B"，这就是enumerate的作用
            实际上这段代码翻译过来的时候逻辑错误了。canMatchNum >= index + 1是不对的，原lua里面的index是逐个递增的，和matchGroup无关
            并且原lua代码对于canMatchNum的gOurExistNum也没有进行已经分配的调整
            """
            haveMatchRobot = False
            # 统计当前可用机器人数量
            canMatchNum = sum(1 for i in gOurExistNum if i != -1)
            for rolename2 in gRolePos:
                # 只有gRolePos中存在该角色且可用机器人数量足够时才分配
                if roleName == rolename2 and canMatchNum >= index + 1:
                    role.append(rolename2)
                    haveMatchRobot = True
                    break
            if not haveMatchRobot:
                # 没有可分配机器人时，角色编号设为-1
                gRoleNum[roleName] = -1
        # 用匈牙利算法进行最优分配
        DoMunkresMatch(role)
    # 对所有未分配编号的角色，统一设为-1
    SetNoMatchRoleZero()
    # 保存本次分配结果，供下次状态沿用
    gLastRoleNum = gRoleNum.copy()