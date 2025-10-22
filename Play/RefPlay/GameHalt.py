import Global
from RoleMatch_LuaStyle import State, Task, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill


class Halt(State):
    def transFunction(self) -> str:
        return super().transFunction() # 调用默认的，也就是不跳转

    def getMatchString(self) -> str:
        return super().getMatchString() # 调用默认的，也就是返回空字符串，实时匹配

    def getTasks(self) -> "dict[str, Task]":
        Tasks = {}
        for roleName, _ in Global.roleNumberStructTable.items():
            Tasks[roleName] = Task(Skill.Stop()) # 全部赋值成Stop()
        return Tasks

@declare_state_machine(
    Halt
)
class GameHalt(StateMachine):
    pass