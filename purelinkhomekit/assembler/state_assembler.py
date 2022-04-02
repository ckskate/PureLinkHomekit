"""converts between json and fan states."""

import json
from typing import Dict, Union, Any, Optional

from src import model


def dto_from_device_state(state: model.DeviceState
                         ) -> Optional[Dict[str, Any]]:
  """creates json dto from device state."""

  dto = {
    "fmod": state.fan_mode.value,
    "fnsp": state.speed.value,
    "oson": state.oscillation.value,
    "qtar": state.quality_target.value,
    "rhtm": state.standby_monitoring.value,
    "nmod": state.night_mode.value
  }
  return dto

def state_from_message_json(dto: bytes) -> Optional[model.DeviceState]:
  """creates device state from dto."""

  dto = json.loads(dto)

  if not isinstance(dto, dict):
    return None

  command_type = (model.StateType(dto["msg"])
                  if "msg" in dto else None)
  if command_type is None:
    return None

  if (command_type in (model.StateType.CURRENT_STATE,
                       model.StateType.STATE_CHANGE)):
    return (__device_state_from_state_json(dto["product-state"])
            if "product-state" in dto else None)
  return None

def __read_dto_value(dto: Dict[str, Any],
                     key: str) -> Union[str, int]:
  return dto[key][1] if isinstance(dto[key], list) else dto[key]

def __device_state_from_state_json(dto: Dict[str, Any]) -> model.DeviceState:
  if not isinstance(dto, dict):
    return None

  fan_mode: Optional[model.FanMode] = None
  fan_state: Optional[model.FanState] = None
  fan_speed: Optional[model.FanSpeed] = None
  quality_target: Optional[model.QualityTarget] = None
  oscillation: Optional[model.Oscillation] = None
  monitoring: Optional[model.StandbyMonitoring] = None
  night_mode: Optional[model.NightMode] = None

  if "fmod" in dto:
    fan_mode = model.FanMode(__read_dto_value(dto, "fmod"))
  if "fnst" in dto:
    fan_state = model.FanState(__read_dto_value(dto, "fnst"))
  if "fnsp" in dto:
    fan_speed = model.FanSpeed(__read_dto_value(dto, "fnsp"))
  if "qtar" in dto:
    quality_target = model.QualityTarget(__read_dto_value(dto, "qtar"))
  if "oson" in dto:
    oscillation = model.Oscillation(__read_dto_value(dto, "oson"))
  if "rhtm" in dto:
    monitoring = model.StandbyMonitoring(__read_dto_value(dto, "rhtm"))
  if "nmod" in dto:
    night_mode = model.NightMode(__read_dto_value(dto, "nmod"))

  return model.DeviceState(fan_mode,
                           fan_state,
                           night_mode,
                           fan_speed,
                           oscillation,
                           quality_target,
                           monitoring)
