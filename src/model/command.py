from typing import Dict, Any, Optional
import time

from util.constants import *
from model.state import DeviceState, EnvironmentState

class Command:
    commandType: CommandType
    state: Optional[DeviceState]

    def __init___(self,
                  commandType: CommandType,
                  state: Optional[DeviceState] = None):
        self.commandType = commandType
        self.state = state

