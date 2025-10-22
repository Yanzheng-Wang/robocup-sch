from CppPackage import getPosModulePos
from Geometry import *
from Global import debugEngine
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Strategy import *
from Vision import *
from Vision import Enemy
from WorldModel import Flags, Conditions, Params, Positions
import Global

DefendMiddlePos = CGeoPoint(-470/1200*Params.pitchLength,0)

class Start(State):

    def getTasks(self) -> "dict[str, Task]":
        return {
            "L": Task(Skill.WMarking(priority=0,num=defenceSequence.getAttackNum(0))),
            "A": Task(Skill.WBack(1,1)),
            "G": Task(Skill.Goalie()),
        }

    def getMatchString(self) -> str:
        return "[L][A]"

    def transFunction(self) -> str:
        if Conditions.isGameOn():
            return "exit"
        return "Start"
    
@declare_state_machine(
    Start
)
class InDirectKick_2023(StateMachine):
    pass