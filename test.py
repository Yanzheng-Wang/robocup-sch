#python版本：3.12.10
# import CppPackage
# import os
# os.add_dll_directory(r"D:\Documents\SRCrobocup\MilkForPython\ZBin")
# print("CppPackage:", dir(CppPackage))
# print("Strategy:", dir(CppPackage.Strategy))
# print("Skill:", dir(CppPackage.Strategy.Skill))
# from CppPackage.Strategy import Skill

# import functools
#
# def delay_execution(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         return lambda: func(*args, **kwargs)
#     return wrapper
#
#
# def argOfError(executor):
#     # 这个函数故意引发一个错误
#     raise ValueError("This is a test error for debugging purposes.")
#
# def myFun(arg1, age:int):
#     pass
#
# class myClass:
#     def __init__(self, func):
#         self.func = func
#
# myClass(myFun(argOfError(3),10))

# gRoleLookUpTable = {
#     # "G": "Goalie", "K": "Kicker", "T": "Tier", "R": "Receiver",
#     # "A": "Assister", "S": "Special", "D": "Defender", "M": "Middle",
#     # "L": "Leader", "B": "Breaker", "F": "Fronter", "C": "Center",
#     **{chr(i): chr(i) for i in range(ord('A'), ord('Z') + 1)}
# }

# def DecodeMatchStr(matchRule):
#     strTable = []
#     teamCnt = 0
#     if callable(matchRule):
#         return matchRule
#     elif isinstance(matchRule, str):
#         s = matchRule
#     else:
#         print("RoleMatch:not a valid matchRule type!!")
#         return []
#     while s:
#         character = s[0]
#         if character == '[':
#             endChar, mode = ']', "RealTime"
#         elif character == '(':
#             endChar, mode = ')', "Once"
#         elif character == '{':
#             endChar, mode = '}', "Never"
#         else:
#             break
#         endPos = s.find(endChar)
#         teamTable = [c for c in s[1:endPos]]
#         # teamTable = list(teamTable)
#         teamTable.append(("mode", mode))
#         strTable.append(teamTable)
#         s = s[endPos+1:]
#         if not s:
#             break
#     # 转换为dict结构
#     result = []
#     for team in strTable:
#         mode = None
#         if isinstance(team[-1], tuple) and team[-1][0] == "mode":
#             mode = team[-1][1]
#             team = team[:-1]
#         result.append({"mode": mode, "roles": team})
#     return result

# a = DecodeMatchStr("[AB]{CD}(E)")

import debugpy
print("==== BEFORE LISTEN ====")
debugpy.listen(5678,in_process_debug_adapter=True) #一定要加in_process_debug_adapter=True才能让vs code监听成功处于待连接的状态，这边的端口号和launch.json中的一致
print("==== AFTER LISTEN ====")
debugpy.wait_for_client()
print("Debugging!")
debugpy.breakpoint() #会在此处停下