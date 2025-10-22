# 是否使用传球
isUsePass = False
# 标志位，表示带球
f = flag.dribbling
# DSS_FLAG为避障和允许DSS的组合标志
DSS_FLAG = flag.dodge_ball + flag.allow_dss
# 球场参数
pl = param.pitchLength
pw = param.pitchWidth
pew = param.penaltyWidth
ped = param.penaltyDepth
goal = param.goalWidth

# 匹配字符串，用于角色分配描述
matchStr = ""
lastMatchStr = ""
needChangeState = False  # 是否需要切换状态
defendTaskTable = []     # 防守任务表
attackTaskTable = []     # 进攻任务表

lastCycle = 0
laststate = "GetBall"
attackerAmount = defenceSequence.attackerAmount()  # 当前对方进攻人数

# 获取当前己方进攻核心编号
def leaderNum():
    return messi.leaderNum()

# 获取当前己方接球手编号
def receiverNum():
    return messi.receiverNum()

# 获取门将传球目标点
def goaliePassPos():
    def gPos():
        return messi.goaliePassPos()
    return gPos

# 获取第i个对方进攻球员编号
def getAttackerNum(i):
    def inner():
        return defenceSequence.getFreeDefNum(i)
    return inner

# 获取传球目标点
def getPassPos():
    def rPos():
        return messi.passPos()
    return rPos

# 获取传球速度
def getPassVel():
    def vel():
        if messi.needChip():
            return messi.passVel() * 1
        return messi.passVel() * 1
    return vel

# 进攻核心的踢球任务
def KICK_TASK():
    def inner():
        # 这里可以切换不同的踢球策略
        # return task.goandTurnKick(getPassPos(),_,getPassVel())
        # return task.zAttackv2(getPassPos(),_,getPassVel())
        return task.Crosserover(getPassPos(), None, getPassVel(), None, False)
    return inner

# 接球手的任务
def receiverTask():
    def inner():
        # 若人数较少且下一个状态为GetBall，则采用盯防
        # if getOurNum() <= 3 and messi.nextState() == "GetBall":
        #     return task.wmarking("Zero", None, getAttackerNum(0))
        # else:
        return task.goCmuRush(pos.getReceivePos(), player.toBallDir, None, DSS_FLAG)
    return inner

# 生成进攻任务表和角色分配字符串
def generateAttackTask():
    global attackTaskTable, matchStr, needChangeState, attackerAmount
    attackTaskTable = []
    leader = leaderNum()
    receiver = receiverNum()
    markingIndex = 0
    otherIndex = 0
    curIndex = 1
    backNum = 3
    posNum = 11
    subStr = ["A","S","M","D","B","R","C","F","K"]  # 角色简写
    attackerAmount = defenceSequence.attackerAmount()
    attackTaskTable.append(KICK_TASK()())  # 进攻核心任务
    global gRoleNum
    # 角色分配与状态切换判断
    if leader != receiver and player.valid(receiver) and leader != gRoleNum["Goalie"] and receiver != gRoleNum["Goalie"]:
        if gRoleNum["Leader"] != leader or gRoleNum["Assister"] != receiver:
            needChangeState = True
        gRoleNum["Leader"] = leader
        gRoleNum["Assister"] = receiver
        matchStr = "{LA}"
    else:
        if gRoleNum["Leader"] != leader and leader != gRoleNum["Goalie"]:
            needChangeState = True
        gRoleNum["Leader"] = leader
        matchStr = "{L}[A]"
    # receiver
    attackTaskTable.append(receiverTask()())
    curIndex += 1
    matchStr += "("
    # danger marking
    attackTaskTable.append(task.wmarking("Zero", None, getAttackerNum(0)))
    matchStr += subStr[curIndex-1]
    curIndex += 1
    matchStr += ")"
    # back
    matchStr += "("
    if ball().posX() > -1000 and (cond.validNum() < 4):
        backNum = 1
    for i in range(1, backNum+1):
        attackTaskTable.append(task.wback(backNum, i))
        if curIndex >= 9:
            break
        matchStr += subStr[curIndex-1]
        curIndex += 1
    matchStr += ")("
    # marking
    for i in range(1, attackerAmount-1):
        attackTaskTable.append(task.wmarking("Zero", None, getAttackerNum(i)))
        if curIndex >= 9:
            break
        matchStr += subStr[curIndex-1]
        curIndex += 1
        markingIndex += 1
    matchStr += ")("
    # otherpos
    for i in range(0, posNum+1):
        attackTaskTable.append(task.wdrag(pos.getOtherPos(otherIndex)))
        if curIndex >= 9:
            break
        matchStr += subStr[curIndex-1]
        curIndex += 1
        otherIndex += 1
    matchStr += ")"

# 生成防守任务表和角色分配字符串
def generateDefendTask():
    global defendTaskTable, matchStr, needChangeState, attackerAmount
    defendTaskTable = []
    leader = leaderNum()
    receiver = receiverNum()
    markingIndex = 0
    otherIndex = 0
    curIndex = 1
    backNum = 3
    posNum = 11
    subStr = ["A","S","M","D","B","R","C","F","K"]
    attackerAmount = defenceSequence.attackerAmount()
    defendTaskTable.append(KICK_TASK()())
    global gRoleNum
    if gRoleNum["Leader"] != leader and leader != gRoleNum["Goalie"]:
        needChangeState = True
    gRoleNum["Leader"] = leader
    matchStr = "{L}("
    # danger marking
    attackTaskTable.append(task.wmarking("Zero", None, getAttackerNum(0))) # 不应该是defendTaskTable吗？
    matchStr += subStr[curIndex-1]
    curIndex += 1
    matchStr += ")("
    # back
    if ball().posX() > 0 and (cond.validNum() < 4):
        backNum = 1
    for i in range(1, backNum+1):
        defendTaskTable.append(task.wback(backNum, i))
        if curIndex >= 9:
            break
        matchStr += subStr[curIndex-1]
        curIndex += 1
    matchStr += ")("
    # marking
    for i in range(1, attackerAmount):
        defendTaskTable.append(task.wmarking("Zero", None, getAttackerNum(i)))
        if curIndex >= 9:
            break
        matchStr += subStr[curIndex-1]
        curIndex += 1
        markingIndex += 1
    matchStr += ")("
    # receiver
    defendTaskTable.append(receiverTask()())
    matchStr += ")("
    # otherpos
    for i in range(0, posNum+1):
        defendTaskTable.append(task.wdrag(pos.getOtherPos(otherIndex)))
        if curIndex >= 9:
            break
        matchStr += subStr[curIndex-1]
        curIndex += 1
        otherIndex += 1
    matchStr += ")"

# 状态切换条件判断（进攻/防守）
def ourBallJumpCond():
    global laststate, lastMatchStr, needChangeState
    state = messi.nextState()
    leader = leaderNum()
    receiver = receiverNum()
    needChangeState = False
    if state == "Pass":
        generateAttackTask()
        if matchStr != lastMatchStr:
            lastMatchStr = matchStr
            needChangeState = True
        if defenceSequence.enemyOrderChangedNew():
            needChangeState = True
    elif state == "GetBall":
        generateDefendTask()
        if gRoleNum["Leader"] != leader and gRoleNum["Goalie"] != leader:
            gRoleNum["Leader"] = leader
            needChangeState = True
        if matchStr != lastMatchStr:
            lastMatchStr = matchStr
            needChangeState = True
        if defenceSequence.enemyOrderChangedNew():
            needChangeState = True
    debugEngine.gui_debug_msg(CGeoPoint(-600, 3000), state)
    if laststate != state or needChangeState:
        laststate = state
        return state

# 获取当前角色分配字符串
def getMatch():
    debugEngine.gui_debug_msg(CGeoPoint(-2000, 0), matchStr)
    return matchStr

# 获取第index个进攻任务
def attackTask(index):
    def inner():
        return attackTaskTable[index-1]
    return inner

# 获取第index个防守任务
def defendTask(index):
    def inner():
        return defendTaskTable[index-1]
    return inner

# 注册战术到全局战术表
gPlayTable.CreatePlay({
    "firstState": "GetBall",
    "GetBall": {
        "switch": lambda: ourBallJumpCond(),
        "Leader": defendTask(1), #对应为新写脚本的L
        "Assister": defendTask(2), #对应为A
        "Special": defendTask(3),
        "Middle": defendTask(4),
        "Defender": defendTask(5),
        "Breaker": defendTask(6),
        "Receiver": defendTask(7),
        "Center": defendTask(8),
        "Fronter": defendTask(9),
        "Kicker": defendTask(10),
        "Goalie": task.goalie(goaliePassPos()),
        "match": getMatch
    },
    "Pass": {                 # 进攻状态
        "switch": lambda: ourBallJumpCond(),
        "Leader": attackTask(1),
        "Assister": attackTask(2),
        "Special": attackTask(3),
        "Middle": attackTask(4),
        "Defender": attackTask(5),
        "Breaker": attackTask(6),
        "Receiver": attackTask(7),
        "Center": attackTask(8),
        "Fronter": attackTask(9),
        "Kicker": attackTask(10),
        "Goalie": task.goalie(goaliePassPos()),
        "match": getMatch
    },
    "name": "NormalPlayMessi_11vs11_new",  # 战术名称
    "applicable": {
        "exp": "a",
        "a": True
    },
    "attribute": "attack",    # 战术属性
    "timeout": 99999          # 超时时间
})