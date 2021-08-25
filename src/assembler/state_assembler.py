import json
from typing import Dict, Union, Any, Optional

from model.state import DeviceState, EnvironmentState
from util.constants import *

class StateAssembler:

    def __read_dto_value(
            self,
            dto: Dict[str, Any],
            key: str
          ) -> Union[str, int]:
        return dto[key][1] if isinstance(dto[key], list) else dto[key]

    def dto_from_device_state(self, state: DeviceState) -> Optional[Dict[str, Any]]:
        dto = {
            "fmod": state.fan_mode.value,
            "fnsp": state.speed.value,
            "oson": state.oscillation.value,
            "qtar": state.quality_target.value,
            "rhtm": state.standby_monitoring.value,
            "nmod": state.night_mode.value
        }
        return dto

    def state_from_message_json(
            self,
            dto: bytes
          ) -> Optional[Union[DeviceState, EnvironmentState]]:

        dto = json.loads(dto)

        if not isinstance(dto, dict):
            return None

        command_type = (StateType(dto["msg"])
                        if "msg" in dto else None)
        if command_type == None:
            return None

        if (command_type == StateType.CURRENT_STATE
              or command_type == StateType.STATE_CHANGE):
            return (self.__device_state_from_state_json(dto["product-state"])
                    if "product-state" in dto else None)
        elif command_type == StateType.ENVIRONMENTAL_DATA:
            return (self.__environment_state_from_state_json(dto["data"])
                    if "data" in dto else None)
        return None

    def __device_state_from_state_json(
            self,
            dto: Dict[str, Any]
          ) -> DeviceState:

        if isinstance(dto, dict) == False:
            return None

        fan_mode = (FanMode(self.__read_dto_value(dto, "fmod"))
                    if "fmod" in dto else None)
        fan_state = (FanState(self.__read_dto_value(dto, "fnst"))
                    if "fnst" in dto else None)
        fan_speed = (FanSpeed(self.__read_dto_value(dto, "fnsp"))
                    if "fnsp" in dto else None)
        quality_target = (QualityTarget(self.__read_dto_value(dto, "qtar"))
                    if "qtar" in dto else None)
        oscillation = (Oscillation(self.__read_dto_value(dto, "oson"))
                    if "oson" in dto else None)
        monitoring = (StandbyMonitoring(self.__read_dto_value(dto, "rhtm"))
                    if "rhtm" in dto else None)
        night_mode = (NightMode(self.__read_dto_value(dto, "nmod"))
                    if "nmod" in dto else None)

        return DeviceState(fan_mode,
                           fan_state,
                           night_mode,
                           fan_speed,
                           oscillation,
                           quality_target,
                           monitoring)

    def __environment_state_from_state_json(
            self,
            dto: Dict[str, Any]
          ) -> DeviceState:

        if isinstance(dto, dict) == False:
            return None

        try:
            humidity = (int(self.__read_dto_value(dto, "hact"))
                        if "hact" in dto else None)
        except Exception:
            humidity = 0

        try:
            vocs = (int(self.__read_dto_value(dto, "vact"))
                                if "vact" in dto else None)
        except Exception:
            vocs = 0

        try:
            temp = (float(self.__read_dto_value(dto, "tact")) / 10
                    if "tact" in dto else None)
        except Exception:
            temp = 0

        try:
            dust = (int(self.__read_dto_value(dto, "pact"))
                    if "pact" in dto else None)
        except Exception:
            dust = 0

        return EnvironmentState(humidity,
                                vocs,
                                temp,
                                dust)

