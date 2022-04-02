"""handles conversion between json dtos and fan commands."""

from typing import Optional
import time
import json

from purelinkhomekit import model
from purelinkhomekit import assembler


def command_to_json(command: model.Command) -> Optional[str]:
  """converts a fan command to its json representation."""

  if command.commandType == model.CommandType.REQUEST_STATE:
    return __request_state_to_json(command.commandType)
  if (command.commandType == model.CommandType.SET_STATE
      and isinstance(command.state, model.DeviceState)):
    return __set_state_to_json(command.state)
  return None

def __request_state_to_json(command_type: model.CommandType
                           ) -> Optional[str]:
  payload = {
    "msg": command_type.value,
    "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
  }
  return json.dumps(payload)


def __set_state_to_json(state: model.DeviceState) -> Optional[str]:
  data = assembler.state_assembler.dto_from_device_state(state)

  if data is None:
    return None

  payload = {
    "msg": model.CommandType.SET_STATE.value,
    "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "mode-reason": "LAPP",
    "data": data
  }
  return json.dumps(payload)
