from typing import Dict, Union, Any, Optional

from state import DeviceState
from constants import *

class StateAssembler:

    def read_dto_value(
            self,
            dto: Dict[str, Any],
            key: str
          ) -> Union[str, int]:
        return dto[key][1] if isinstance(dto[key], list) else dto[key]

    def state_from_command_json(
            self,
            dto: Dict[str, Any]
          ) -> Optional[DeviceState]:
        if "product-state" in dto:
            return self.device_state_from_state_json(dto["product-state"])
        return None

    def device_state_from_state_json(
            self,
            dto: Dict[str, Any]
          ) -> DeviceState:

        if isinstance(dto, dict) == False:
            return None

        fan_mode = None
        fan_state = None
        fan_speed = None
        quality_target = None
        oscillation = None
        standby_monitoring = None
        night_mode = None

        if "fmod" in dto:
            fan_mode = FanMode(self.read_dto_value(dto, "fmod"))
        if "fnst" in dto:
            fan_state = FanState(self.read_dto_value(dto, "fnst"))
        if "fnsp" in dto:
            fan_speed = FanSpeed(self.read_dto_value(dto, "fnsp"))
        if "qtar" in dto:
            quality_target = QualityTarget(self.read_dto_value(dto, "qtar"))
        if "oson" in dto:
            oscillation = Oscillation(self.read_dto_value(dto, "oson"))
        if "rhtm" in dto:
            standby_monitoring = StandbyMonitoring(self.read_dto_value(dto, "rhtm"))
        if "nmod" in dto:
            night_mode = NightMode(self.read_dto_value(dto, "nmod"))

        return DeviceState(fan_mode,
                           fan_state,
                           night_mode,
                           fan_speed,
                           oscillation,
                           quality_target,
                           standby_monitoring)
