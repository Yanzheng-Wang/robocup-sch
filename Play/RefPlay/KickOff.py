import math

import Global
from Geometry import *
from Global import getRoleNumber
from RoleMatch_LuaStyle import Task, State, declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Skills import Skill
from Strategy import *
from Strategy.AttackInfomation import generateShootPoint
from Utils import buffered_condition
from Vision import *
from WorldModel import Flags, Conditions, Params, Positions, KickPower, Directions, ChipPower

nextRoleNumber = Global.NextRoleNumber()

f = Flags.dribbling + Flags.allow_dss
DSS_FLAG = Flags.allow_dss + Flags.dodge_ball
KickOff_mode = 4
ACC = 5000

ToGoalPoint = [
    CGeoPoint(Params.pitchLength / 2, 0),
    Ball.refSyntYPos(CGeoPoint(Params.pitchLength / 2, Params.goalWidth / 2)),
    Ball.refAntiYPos(CGeoPoint(Params.pitchLength / 2, Params.goalWidth / 2 - 100)),
]

wait_pos = CGeoPoint(-500, 0)


def getKickOffPos(index):
    return CppPackage.getPosModulePos(index, KickOff_mode)


class Start(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.RushTo(Player.shootGen(200, math.pi), Directions.playerToBall("L"), ACC, DSS_FLAG)),
            "A": Task(Skill.RushTo(getKickOffPos(0), 0, ACC, DSS_FLAG)),
            "S": Task(Skill.RushTo(getKickOffPos(1), 0, ACC, DSS_FLAG)),
            "B": Task(Skill.RushTo(getKickOffPos(2), 0, ACC, DSS_FLAG)),
            "R": Task(Skill.RushTo(getKickOffPos(3), 0, ACC, DSS_FLAG)),
            "C": Task(Skill.RushTo(getKickOffPos(4), 0, ACC, DSS_FLAG)),
            "F": Task(Skill.RushTo(getKickOffPos(5), 0, ACC, DSS_FLAG)),
            "K": Task(Skill.WBack(3, 1)),
            "M": Task(Skill.WBack(3, 2)),
            "D": Task(Skill.WBack(3, 3)),
            "G": Task(Skill.Goalie()),
        }
        nextRoleNumber.adjustNextRoleNumber(tasks)
        return tasks

    def getMatchString(self) -> str:
        return "{L}[MDK][ASBRCF]"

    def transFunction(self) -> str:
        nextRoleNumber.resetNextRoleNumber()
        nextRoleNumber["L"] = beckhamDecision.kickNum()
        if Conditions.isNormalStart():
            # if Conditions.ourvalidNum() < 5:
            return "DirectShoot"
            # else:
            #     return "run"
        return ""


class Run(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(
                lambda executor: Skill.StaticGetBall(
                    self.playerPos("A"),
                    KickPower.getKickPower(self.playerPos("A"), self.playerPos("L")),
                    ChipPower.toTargetPos(self.playerPos("A"))
                )
            ),
            "A": Task(Skill.RushTo(getKickOffPos(0), Player.toPlayerDir("L"), ACC, DSS_FLAG)),
            "S": Task(Skill.RushTo(getKickOffPos(1), 0, ACC, DSS_FLAG)),
            "B": Task(Skill.RushTo(getKickOffPos(2), 0, ACC, DSS_FLAG)),
            "R": Task(Skill.RushTo(getKickOffPos(3), 0, ACC, DSS_FLAG)),
            "C": Task(Skill.RushTo(getKickOffPos(4), 0, ACC, DSS_FLAG)),
            "F": Task(Skill.RushTo(getKickOffPos(5), 0, ACC, DSS_FLAG)),
            "K": Task(Skill.WBack(3, 1)),
            "M": Task(Skill.WBack(3, 2)),
            "D": Task(Skill.WBack(3, 3)),
            "G": Task(Skill.Goalie()),
        }
        nextRoleNumber.adjustNextRoleNumber(tasks)
        return tasks

    def getMatchString(self) -> str:
        return "{L}[MDK][ASBRCF]"

    def transFunction(self) -> str:
        nextRoleNumber.resetNextRoleNumber()
        if buffered_condition(Player.kickBall("L") or Ball.velMod() > 1000, 1, 90 * 6):
            nextRoleNumber["L"], nextRoleNumber["A"] = getRoleNumber("A"), getRoleNumber("L")
            return "Shoot"
        # if buffered_condition(messiDecision.nextState() == "GetBall", 10):
        #     return "exit"
        return ""


class Shoot(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.GoAndTurnKick(Positions.theirGoal, power=6000)),
            "A": Task(Skill.RushTo(wait_pos, Player.toPlayerDir("L"), ACC, DSS_FLAG)),
            "S": Task(Skill.RushTo(getKickOffPos(1), 0, ACC, DSS_FLAG)),
            "B": Task(Skill.RushTo(getKickOffPos(2), 0, ACC, DSS_FLAG)),
            "R": Task(Skill.RushTo(getKickOffPos(3), 0, ACC, DSS_FLAG)),
            "C": Task(Skill.RushTo(getKickOffPos(4), 0, ACC, DSS_FLAG)),
            "F": Task(Skill.RushTo(getKickOffPos(5), 0, ACC, DSS_FLAG)),
            "K": Task(Skill.WBack(3, 1)),
            "M": Task(Skill.WBack(3, 2)),
            "D": Task(Skill.WBack(3, 3)),
            "G": Task(Skill.Goalie()),
        }

        nextRoleNumber.adjustNextRoleNumber(tasks)
        return tasks

    def getMatchString(self) -> str:
        return "{L}[MDK][ASBRCF]"

    def transFunction(self) -> str:
        if buffered_condition(Player.kickBall("L") or Ball.velMod() > 1000, 1, int(75 * 2.5)):
            return "exit"
        # if buffered_condition(messiDecision.nextState() == "GetBall", 10):
        #     return "exit"
        return ""


class DirectShoot(State):

    def getTasks(self) -> "dict[str, Task]":
        tasks = {
            "L": Task(Skill.Shoot(generateShootPoint(40), isChip=True, power=8000)),
            "A": Task(Skill.RushTo(getKickOffPos(0), 0, ACC, DSS_FLAG)),
            "S": Task(Skill.RushTo(getKickOffPos(1), 0, ACC, DSS_FLAG)),
            "B": Task(Skill.RushTo(getKickOffPos(2), 0, ACC, DSS_FLAG)),
            "R": Task(Skill.RushTo(getKickOffPos(3), 0, ACC, DSS_FLAG)),
            "C": Task(Skill.RushTo(getKickOffPos(4), 0, ACC, DSS_FLAG)),
            "F": Task(Skill.RushTo(getKickOffPos(5), 0, ACC, DSS_FLAG)),
            "K": Task(Skill.WBack(3, 1)),
            "M": Task(Skill.WBack(3, 2)),
            "D": Task(Skill.WBack(3, 3)),
            "G": Task(Skill.Goalie()),
        }

        nextRoleNumber.adjustNextRoleNumber(tasks)
        return tasks

    def getMatchString(self) -> str:
        return "{L}[MDK][ASBRCF]"

    def transFunction(self) -> str:
        if buffered_condition(Player.kickBall("L") or Ball.velMod() > 1000, 1, 180):
            return "exit"
        return ""

@declare_state_machine(
    Start,
    Run,
    Shoot,
    DirectShoot
)
class KickOff(StateMachine):
    pass

"""
gPlayTable.CreatePlay{

firstState = "start",

["start"] = {
	switch = function()
        gRoleNum["Leader"] = beckham:kickNum()
		if cond.isNormalStart() then
			-- if cond.ourvalidNum() < 5 then
                return "directshoot"
            -- else
            --     return "run"
            -- end
		end
	end,
	Leader   = task.goCmuRush(player.shootGen(200,math.pi),dir.playerToBall,ACC,DSS_FLAG),
	Assister = task.goCmuRush(getKickOffPos(0),0,ACC,DSS_FLAG),
	Special  = task.goCmuRush(getKickOffPos(1),0,ACC,DSS_FLAG),
	Breaker  = task.goCmuRush(getKickOffPos(2),0,ACC,DSS_FLAG),
	Receiver = task.goCmuRush(getKickOffPos(3),0,ACC,DSS_FLAG),
    Center   = task.goCmuRush(getKickOffPos(4),0,ACC,DSS_FLAG),
    Fronter  = task.goCmuRush(getKickOffPos(5),0,ACC,DSS_FLAG),
    Kicker   = task.wback(3,1),
	Middle   = task.wback(3,2),
	Defender = task.wback(3,3),
	Goalie   = task.goalie(),
	match = "{L}[MDK][ASBRCF]"
},

["run"] = {
	switch = function()
		if bufcnt(player.kickBall("Leader") or ball().velMod()>1000,1,90*6) then
            local temp = gRoleNum["Leader"]
            gRoleNum["Leader"] = gRoleNum["Assister"]
            gRoleNum["Assister"] = temp
			return "shoot"
		end
		-- if bufcnt(messi:nextState() == "GetBall",10) then
		-- 	 return "exit"
		-- end
	end,
	Leader   = task.staticGetBall("Assister",kp.toTarget("Assister","Leader"),cp.toTarget("Assister")),
	Assister = task.goCmuRush(getKickOffPos(0),player.toPlayerDir("Leader"),ACC,DSS_FLAG),
	Special  = task.goCmuRush(getKickOffPos(1),0,ACC,DSS_FLAG),
	Breaker  = task.goCmuRush(getKickOffPos(2),0,ACC,DSS_FLAG),
	Receiver = task.goCmuRush(getKickOffPos(3),0,ACC,DSS_FLAG),
	Center   = task.goCmuRush(getKickOffPos(4),0,ACC,DSS_FLAG),
    Fronter  = task.goCmuRush(getKickOffPos(5),0,ACC,DSS_FLAG),
    Kicker   = task.wback(3,1),
	Middle   = task.wback(3,2),
	Defender = task.wback(3,3),
	Goalie   = task.goalie(),
	match = "{L}[MDK][ASBRCF]"
},

["shoot"] = {
	switch = function()
		if bufcnt(player.kickBall("Leader") or ball().velMod()>1000,1,75*2.5) then
			return "exit"
		end
		-- if bufcnt(messi:nextState() == "GetBall",10) then
		-- 	 return "exit"
		-- end
	end,
	Leader   = task.goandTurnKick(pos.theirGoal,_,6000),
	Assister = task.goCmuRush(wait_pos,player.toPlayerDir("Leader"),ACC,DSS_FLAG),
	Special  = task.goCmuRush(getKickOffPos(1),0,ACC,DSS_FLAG),
	Breaker  = task.goCmuRush(getKickOffPos(2),0,ACC,DSS_FLAG),
	Receiver = task.goCmuRush(getKickOffPos(3),0,ACC,DSS_FLAG),
	Center   = task.goCmuRush(getKickOffPos(4),0,ACC,DSS_FLAG),
    Fronter  = task.goCmuRush(getKickOffPos(5),0,ACC,DSS_FLAG),
    Kicker   = task.wback(3,1),
	Middle   = task.wback(3,2),
	Defender = task.wback(3,3),
	Goalie   = task.goalie(),
	match = "{L}[MDK][ASBRCF]"
},

["directshoot"] = {
	switch = function()
		if bufcnt(player.kickBall("Leader") or ball().velMod()>1000,1,180) then
			return "exit"
		end
	end,
	Leader   = DSHOOT_TASK("Leader"),
	Assister = task.goCmuRush(getKickOffPos(0),0,ACC,DSS_FLAG),
	Special  = task.goCmuRush(getKickOffPos(1),0,ACC,DSS_FLAG),
	Breaker  = task.goCmuRush(getKickOffPos(2),0,ACC,DSS_FLAG),
	Receiver = task.goCmuRush(getKickOffPos(3),0,ACC,DSS_FLAG),
	Center   = task.goCmuRush(getKickOffPos(4),0,ACC,DSS_FLAG),
    Fronter  = task.goCmuRush(getKickOffPos(5),0,ACC,DSS_FLAG),
    Kicker   = task.wback(3,1),
	Middle   = task.wback(3,2),
	Defender = task.wback(3,3),
	Goalie   = task.goalie(),
	match = "{L}[MDK][ASBRCF]"
},


name = "Ref_KickOff_11vs11",
applicable={
	exp = "a",
	a = true
},
attribute = "attack",
timeout = 99999
}
"""
