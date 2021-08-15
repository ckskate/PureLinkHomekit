from typing import Dict, Union, Any, Optional

from state import DeviceState, EnvironmentState
from assembler import StateAssembler
from command import Command
from constants import *

class CommandAssembler:

    def json_from_command(
            self,
            command: Command) -> Optional[str]:
        if (command.commandType == CommandType.REQUEST_ENVIRONMENT_STATE
                or command.commandType == CommandType.REQUEST_STATE):
            return self.__json_for_request_command(command.commandType)
        elif (command.commandType == CommandType.SET_STATE
                and isinstance(command.state, DeviceState):
            return self.__json_for_set_state_command(command.state)
        return None

    def __json_for_request_command(self,
                                   commandType: CommandType
            ) -> Optional[str]:
        payload = {
            "msg": commandType.value,
            "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        return json.dumps(payload)

    def __json_for_set_state_command(self,
                                    state: DeviceState
            ) -> Optional[str]:
        data = StateAssembler().dto_from_device_state(state)

        if data == None:
            return None

        payload = {
            "msg": CommandType.SET_STATE.value,
            "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "mode-reason": "LAPP",
            "data": data
        }
        return json.dumps(payload)

