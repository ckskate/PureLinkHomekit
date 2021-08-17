from enum import Enum

DEVICE_NUMBER = "475"

class CommandType(Enum):
    """Types of commands you can send the fan."""

    REQUEST_ENVIRONMENT_STATE = 'REQUEST-PRODUCT-ENVIRONMENT-CURRENT-SENSOR-DATA'
    REQUEST_STATE = 'REQUEST-CURRENT-STATE'
    SET_STATE = 'STATE-SET'


class StateType(Enum):
    """State type from received message."""

    CURRENT_STATE = 'CURRENT-STATE'
    STATE_CHANGE = 'STATE-CHANGE'
    ENVIRONMENTAL_DATA = 'ENVIRONMENTAL-CURRENT-SENSOR-DATA'


class FanMode(Enum):
    """Fan mode."""

    OFF = 'OFF'
    FAN = 'FAN'
    AUTO = 'AUTO'

    @staticmethod
    def from_homekit_value(value: int):
        if value == 0:
            return FanMode.OFF
        elif value == 1:
            return FanMode.FAN
        else:
            return None

    def homekit_value(self):
        if self == FanMode.OFF:
            return 0
        elif self == FanMode.FAN:
            return 1
        else:
            return None


class Oscillation(Enum):
    """Oscillation."""

    OSCILLATION_ON = 'ON'
    OSCILLATION_OFF = 'OFF'

    @staticmethod
    def from_homekit_value(value: int):
        if value == 0:
            return Oscillation.OSCILLATION_OFF
        elif value == 1:
            return Oscillation.OSCILLATION_ON
        else:
            return None

    def homekit_value(self):
        if self == Oscillation.OSCILLATION_ON:
            return 1
        elif self == Oscillation.OSCILLATION_OFF:
            return 0
        else:
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
        tens_place = value // 10
        if tens_place == 0 or tens_place == 1:
            return FanSpeed.FAN_SPEED_1
        elif tens_place == 2:
            return FanSpeed.FAN_SPEED_2
        elif tens_place == 3:
            return FanSpeed.FAN_SPEED_3
        elif tens_place == 4:
            return FanSpeed.FAN_SPEED_4
        elif tens_place == 5:
            return FanSpeed.FAN_SPEED_5
        elif tens_place == 6:
            return FanSpeed.FAN_SPEED_6
        elif tens_place == 7:
            return FanSpeed.FAN_SPEED_7
        elif tens_place == 8:
            return FanSpeed.FAN_SPEED_8
        elif tens_place == 9:
            return FanSpeed.FAN_SPEED_9
        elif tens_place == 10:
            return FanSpeed.FAN_SPEED_10
        else:
            return None

    def homekit_value(self):
        if self == FanSpeed.FAN_SPEED_1:
            return 10.0
        elif self == FanSpeed.FAN_SPEED_2:
            return 20.0
        elif self == FanSpeed.FAN_SPEED_3:
            return 30.0
        elif self == FanSpeed.FAN_SPEED_4:
            return 40.0
        elif self == FanSpeed.FAN_SPEED_5:
            return 50.0
        elif self == FanSpeed.FAN_SPEED_6:
            return 60.0
        elif self == FanSpeed.FAN_SPEED_7:
            return 70.0
        elif self == FanSpeed.FAN_SPEED_8:
            return 80.0
        elif self == FanSpeed.FAN_SPEED_9:
            return 90.0
        elif self == FanSpeed.FAN_SPEED_10:
            return 100.0
        else:
            return None


class FanState(Enum):
    """Fan State."""

    FAN_OFF = "OFF"
    FAN_ON = "FAN"

    @staticmethod
    def from_homekit_value(value: int):
        if value == 0:
            return FanState.FAN_OFF
        elif value == 1:
            return FanState.FAN_ON
        else:
            return None

    def homekit_value(self):
        if self == FanState.FAN_OFF:
            return 0
        elif self == FanState.FAN_ON:
            return 1
        else:
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

