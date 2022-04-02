"""fan command related types."""

from enum import Enum
from typing import Optional

from src import model

class CommandType(Enum):
  """types of commands you can send the fan."""

  REQUEST_ENVIRONMENT_STATE = 'REQUEST-PRODUCT-ENVIRONMENT-CURRENT-SENSOR-DATA'
  REQUEST_STATE = 'REQUEST-CURRENT-STATE'
  SET_STATE = 'STATE-SET'

class Command:
  """command that can be sent or received from the fan."""

  command_type: model.CommandType
  state: Optional[model.DeviceState]

  def __init__(self,
               command_type: model.CommandType,
               state: Optional[model.DeviceState] = None):
    self.command_type = command_type
    self.state = state
