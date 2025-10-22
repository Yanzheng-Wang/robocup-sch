from enum import Enum

import CppPackage

from .Positions import *

taskMediator = CppPackage.TaskMediator.Instance()
worldModel = CppPackage.WorldModel.Instance()
kickStatus = CppPackage.KickStatus.Instance()

class KickMode(Enum):
    none = 0,
    flat = 1,
    chip = 2,