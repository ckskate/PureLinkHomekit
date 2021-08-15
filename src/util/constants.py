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


class Oscillation(Enum):
    """Oscillation."""

    OSCILLATION_ON = 'ON'
    OSCILLATION_OFF = 'OFF'


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


class FanState(Enum):
    """Fan State."""

    FAN_OFF = "OFF"
    FAN_ON = "FAN"


class QualityTarget(Enum):
    """Quality Target for air."""

    QUALITY_NORMAL = "0004"
    QUALITY_HIGH = "0003"
    QUALITY_BETTER = "0001"


class StandbyMonitoring(Enum):
    """Monitor air quality when on standby."""

    STANDBY_MONITORING_ON = "ON"
    STANDBY_MONITORING_OFF = "OFF"

