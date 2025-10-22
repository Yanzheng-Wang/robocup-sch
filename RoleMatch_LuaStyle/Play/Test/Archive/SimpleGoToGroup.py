from RoleMatch_LuaStyle import StateMachine, declare_state_machine, declare_state
from RoleMatch_LuaStyle.Skills.Skill import SimpleGoTo
import CppPackage as C
import Global
from RoleMatch_LuaStyle.Task import Task


def trans_GO_FORWARD():
    if Global.ball().Pos().x() > 0:
        return "GO_FORWARD"
    return "GO_BACKWARD"
@declare_state(
    # 状态名称即类名称
    # transition function, 用于状态切换
    # transFunction=lambda: Global.ball().Pos().x() > 0 and "GO_FORWARD" or "GO_BACKWARD",
    transFunction=trans_GO_FORWARD,
    tasks=[
        # 所有要执行的任务列表
        SimpleGoto_old(C.CGeoPoint(1000, -500), 0, 0),
        SimpleGoto_old(C.CGeoPoint(1000, 500), 0, 0),
    ]
)
class GO_FORWARD:
    pass


# @taskGroupLuaStyle.state_class(
#     # 状态名称，用于状态机识别和切换
#     state_name="GO_FORWARD",
#     # transition function, 用于状态切换
#     # transFunction=lambda: Global.ball().Pos().x() > 0 and "GO_FORWARD" or "GO_BACKWARD",
#
#     transFunction = myTrans,
#     freeTasks=[
#         # 所有要执行的任务列表
#         SimpleGoto(C.CGeoPoint(1000, -500), 0, 0),
#         SimpleGoto(C.CGeoPoint(1000, 500), 0, 0),
#     ]
# )
# class GO_FORWARD:
#     def myTrans(self):
#         if Global.ball().Pos().x() > 0:
#             return "GO_FORWARD"
#         return "GO_BACKWARD"
#     pass


@declare_state(
    #老三元表达式写法
    # transFunction=lambda: Global.ball().Pos().x() > 0 and "GO_FORWARD" or "GO_BACKWARD",
    transFunction=lambda: "GO_FORWARD" if Global.ball().Pos().x() > 0 else "GO_BACKWARD",
    tasks=[
        # SimpleGoto_old(C.CGeoPoint(-1000, -500), 0, 0),
        # SimpleGoto_old(C.CGeoPoint(-1000, 500), 0, 0),
        Task(SimpleGoTo(C.CGeoPoint(-1000, -500), 0, 0)),
        Task(SimpleGoTo(C.CGeoPoint(-1000, -500), 0, 0)),
        Task(SimpleGoTo(C.CGeoPoint(-1000, -500), 0, 0), fixedNumber=0)
    ]
)
class GO_BACKWARD:
    pass

# 第一个状态是最初状态（GO_FORWARD）
@declare_state_machine("SampleGroup",
                       GO_FORWARD,
                       GO_BACKWARD
                       )
class SampleGroup(StateMachine):
    """示例任务组：继承自 StateMachine，定义具体的状态和任务"""
    pass






