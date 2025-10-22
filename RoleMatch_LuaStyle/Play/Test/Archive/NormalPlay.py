from RoleMatch_LuaStyle import StateMachine, declare_state_machine
from RoleMatch_LuaStyle.Skills.Goalie import Goalie_old
from RoleMatch_LuaStyle import declare_state
import CppPackage as C
import Global


@declare_state(
    # 状态名称，用于状态机识别和切换
    state_name="ADVANCE",
    # transition function, 用于状态切换
    transFunction=lambda: Global.ball().Pos().x() > 0 and "ADVANCE" or "DEFENCE",
    tasks=[
        # 所有要执行的任务列表
        SimpleGoto_old(C.CGeoPoint(500, 0), 0, 0),
        Goalie_old(C.CGeoPoint(500, 0), 0),
    ]
)
class Advance: #为什么不用Advance字典？
    pass


@declare_state(
    state_name="DEFENCE",
    transFunction=lambda: Global.ball().Pos().x() > 0 and "ADVANCE" or "DEFENCE",
    tasks=[
        SimpleGoto_old(C.CGeoPoint(-500, 0), 0, 0),
        Goalie_old(C.CGeoPoint(500, 0), 0),
    ]
)
class Defence:
    pass


# 第一个状态是最初状态（GO_FORWARD）
@declare_state_machine("Nor", Advance, Defence)
class Nor(StateMachine):
    pass
