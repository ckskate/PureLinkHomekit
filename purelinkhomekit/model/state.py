"""fan state related types."""

from enum import Enum
from typing import Optional

DEVICE_NUMBER = "475"

class StateType(Enum):
  """state type for received message."""

  CURRENT_STATE = 'CURRENT-STATE'
  STATE_CHANGE = 'STATE-CHANGE'

class FanMode(Enum):
  """fan speed mode. can be 'off', 'fan' (which is regular), or 'auto'."""

  OFF = 'OFF'
  FAN = 'FAN'
  AUTO = 'AUTO'

  @staticmethod
  def from_homekit_value(value: int):
    """creates a dyson FanMode from the equivalent homekit value."""
    if value == 0:
      return FanMode.OFF
    if value == 1:
      return FanMode.FAN
    return None

  def homekit_value(self) -> Optional[int]:
    """returns the equivalent homekit value for a given FanMode."""
    if self == FanMode.OFF:
      return 0
    if self == FanMode.FAN:
      return 1
    return None


class Oscillation(Enum):
  """fan oscillation state."""

  OSCILLATION_ON = 'ON'
  OSCILLATION_OFF = 'OFF'

  @staticmethod
  def from_homekit_value(value: int):
    """creates oscillation type from homekit value."""
    if value == 0:
      return Oscillation.OSCILLATION_OFF
    if value == 1:
      return Oscillation.OSCILLATION_ON
    return None

  def homekit_value(self):
    """returns the equivalent homekit value for a given oscillation."""
    if self == Oscillation.OSCILLATION_ON:
      return 1
    if self == Oscillation.OSCILLATION_OFF:
      return 0
    return None

class NightMode(Enum):
  """Night mode."""

  NIGHT_MODE_ON = 'ON'
  NIGHT_MODE_OFF = 'OFF'

class FanSpeed(Enum):
  """Fan Speed."""

  FAN_SPEED_1 = '0001'
  FAN_SPEED_2 = '0002'
  FAN_SPEED_3 = '0003'
  FAN_SPEED_4 = '0004'
  FAN_SPEED_5 = '0005'
  FAN_SPEED_6 = '0006'
  FAN_SPEED_7 = '0007'
  FAN_SPEED_8 = '0008'
  FAN_SPEED_9 = '0009'
  FAN_SPEED_10 = '0010'
  FAN_SPEED_AUTO = 'AUTO'

  @staticmethod
  def from_homekit_value(value: float):
    """creates a FanSpeed from a homekit value."""

    fan_speed = None
    tens_place = value // 10
    if tens_place in (0, 1):
      fan_speed = FanSpeed.FAN_SPEED_1
    if tens_place == 2:
      fan_speed = FanSpeed.FAN_SPEED_2
    if tens_place == 3:
      fan_speed = FanSpeed.FAN_SPEED_3
    if tens_place == 4:
      fan_speed = FanSpeed.FAN_SPEED_4
    if tens_place == 5:
      fan_speed = FanSpeed.FAN_SPEED_5
    if tens_place == 6:
      fan_speed = FanSpeed.FAN_SPEED_6
    if tens_place == 7:
      fan_speed = FanSpeed.FAN_SPEED_7
    if tens_place == 8:
      fan_speed = FanSpeed.FAN_SPEED_8
    if tens_place == 9:
      fan_speed = FanSpeed.FAN_SPEED_9
    if tens_place == 10:
      fan_speed = FanSpeed.FAN_SPEED_10
    return fan_speed

  def homekit_value(self):
    """returns the homekit equivalent value for this speed."""

    desired_speed: Optional[float] = None
    if self == FanSpeed.FAN_SPEED_1:
      desired_speed = 10.0
    if self == FanSpeed.FAN_SPEED_2:
      desired_speed = 20.0
    if self == FanSpeed.FAN_SPEED_3:
      desired_speed = 30.0
    if self == FanSpeed.FAN_SPEED_4:
      desired_speed = 40.0
    if self == FanSpeed.FAN_SPEED_5:
      desired_speed = 50.0
    if self == FanSpeed.FAN_SPEED_6:
      desired_speed = 60.0
    if self == FanSpeed.FAN_SPEED_7:
      desired_speed = 70.0
    if self == FanSpeed.FAN_SPEED_8:
      desired_speed = 80.0
    if self == FanSpeed.FAN_SPEED_9:
      desired_speed = 90.0
    if self == FanSpeed.FAN_SPEED_10:
      desired_speed = 100.0
    return desired_speed

class FanState(Enum):
  """Fan State."""

  FAN_OFF = "OFF"
  FAN_ON = "FAN"

  @staticmethod
  def from_homekit_value(value: int):
    """returns a FanState for an equivalent homekit value."""
    if value == 0:
      return FanState.FAN_OFF
    if value == 1:
      return FanState.FAN_ON
    return None

  def homekit_value(self):
    """returns homekit value for equivalent FanState."""
    if self == FanState.FAN_OFF:
      return 0
    if self == FanState.FAN_ON:
      return 1
    return None

class QualityTarget(Enum):
  """Quality Target for air."""

  QUALITY_NORMAL = "0004"
  QUALITY_HIGH = "0003"
  QUALITY_BETTER = "0001"

class StandbyMonitoring(Enum):
  """Monitor air quality when on standby."""

  STANDBY_MONITORING_ON = "ON"
  STANDBY_MONITORING_OFF = "OFF"

class DeviceState:
  """represents current state of fan."""

  fan_mode: FanMode
  fan_state: FanState
  night_mode: NightMode
  speed: FanSpeed
  oscillation: Oscillation
  quality_target: QualityTarget
  standby_monitoring: StandbyMonitoring

  def __init__(self,
               fan_mode: Optional[FanMode],
               fan_state: Optional[FanState],
               night_mode: Optional[NightMode],
               speed: Optional[FanSpeed],
               oscillation: Optional[Oscillation],
               quality_target: Optional[QualityTarget],
               standby_monitoring: Optional[StandbyMonitoring]) -> None:
    self.fan_mode = fan_mode
    self.fan_state = fan_state
    self.night_mode = night_mode
    self.speed = speed
    self.oscillation = oscillation
    self.quality_target = quality_target
    self.standby_monitoring = standby_monitoring

  def state_setting_values_to(self,
                              fan_mode: Optional[FanMode] = None,
                              fan_state: Optional[FanState] = None,
                              night_mode: Optional[NightMode] = None,
                              speed: Optional[FanSpeed] = None,
                              oscillation: Optional[Oscillation] = None,
                              quality_target: Optional[QualityTarget] = None,
                              standby_monitoring: Optional[StandbyMonitoring] = None):
    fan_mode = self.fan_mode if fan_mode is None else fan_mode
    fan_state = self.fan_state if fan_state is None else fan_state
    night_mode= self.night_mode if night_mode is None else night_mode
    speed = self.speed if speed is None else speed
    oscillation = self.oscillation if oscillation is None else oscillation
    quality_target = (self.quality_target if quality_target is None
                                          else quality_target)
    standby_monitoring = (self.standby_monitoring if standby_monitoring is None
                                                  else standby_monitoring)

    return DeviceState(fan_mode,
                       fan_state,
                       night_mode,
                       speed,
                       oscillation,
                       quality_target,
                       standby_monitoring)

    def __repr__(self):
      fields = [("fan_mode", self.fan_mode),
                ("fan_state", self.fan_state),
                ("night_mode", self.night_mode),
                ("speed", self.speed),
                ("oscillation", self.oscillation),
                ("quality_target", self.quality_target),
                ("standby_monitoring", self.standby_monitoring)]
      string_fields = map(lambda x: f"{x[0]}={x[1]}", fields)
      return 'DeviceState(' + ",".join(string_fields) + ')'
