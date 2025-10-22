from enum import Enum, auto

import CppPackage
from RoleMatch_CppStyle.TaskGroups.StateMachine import StateMachine
from Vision.Ball import ball


# 类比cpp的enum class声明几个标识符而已
class SimpleGotoStates(Enum):
    GoForward = auto() #自动分配enum的整数值
    GoBackWard = auto()

class SimpleGoto(StateMachine):
    def __init__(self):
        super().__init__()
        self.current_state = SimpleGotoStates.GoForward

    def planTasks(self):
        # 状态转换
        match self.current_state:
            case SimpleGotoStates.GoForward:
                # 如果满足条件，切换到后退状态
                if ball().Pos().x() > 0:
                    self.current_state = SimpleGotoStates.GoBackWard
            case SimpleGotoStates.GoBackWard:
                # 如果满足条件，切换到前进状态
                if ball().Pos().x() <= 0:
                    self.current_state = SimpleGotoStates.GoForward
            case _:
                raise ValueError("Unknown state")

        # 状态执行
        match self.current_state:
            case SimpleGotoStates.GoForward:
                # 执行前进任务
                CppPackage.makeItSimpleGoTo(0, CppPackage.CGeoPoint(1000, -500), 0, 0)
                CppPackage.makeItSimpleGoTo(1, CppPackage.CGeoPoint(1000, 500), 0, 0)
            case SimpleGotoStates.GoBackWard:
                # 执行后退任务
                CppPackage.makeItSimpleGoTo(0, CppPackage.CGeoPoint(-1000, -500), 0, 0)
                CppPackage.makeItSimpleGoTo(1, CppPackage.CGeoPoint(-1000, 500), 0, 0)
            case _:
                raise ValueError("Unknown state")

        # freeTasks = [
        #
        #
        # ]
        # munkres(freeTasks)

        # if elif / match都不会发生case穿透问题！
        # if self.current_state == SimpleGotoStates.GoForward:
        #     # 执行前进任务
        #     CppPackage.makeitSimpleGoto(0, CppPackage.CGeoPoint(1000, -500), 0, 0)
        #     CppPackage.makeitSimpleGoto(1, CppPackage.CGeoPoint(1000, 500), 0, 0)
        #     self.current_state = SimpleGotoStates.GoBackWard
        # elif self.current_state == SimpleGotoStates.GoBackWard:
        #     # 执行后退任务
        #     CppPackage.makeitSimpleGoto(0,CppPackage.CGeoPoint(-1000, -500), 0, 0)
        #     CppPackage.makeitSimpleGoto(1,CppPackage.CGeoPoint(-1000, 500), 0, 0)
        #     self.current_state = SimpleGotoStates.GoForward
        # else:
        #     raise ValueError("Unknown state")
        # munkres_for_tasks()

