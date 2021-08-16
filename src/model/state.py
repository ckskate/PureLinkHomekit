from typing import Dict, Union, Any, Optional
from util.constants import *


class DeviceState:
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
        fan_mode = self.fan_mode if fan_mode == None else fan_mode
        fan_state = self.fan_state if fan_state == None else fan_state
        night_mode= self.night_mode if night_mode == None else night_mode
        speed = self.speed if speed == None else speed
        oscillation = self.oscillation if oscillation == None else oscillation
        quality_target = self.quality_target if quality_target == None else quality_target
        standby_monitoring = self.standby_monitoring if standby_monitoring == None else standby_monitoring

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


class EnvironmentState:
    humidity: int
    volatile_compounds: int
    temperature: float
    dust: int

    def __init__(self,
                 humidity: Optional[int],
                 volatile_compounds: Optional[int],
                 temperature: Optional[float],
                 dust: Optional[int]) -> None:
        self.humidity = humidity
        self.volatile_compounds = volatile_compounds
        self.temperature = temperature
        self.dust = dust


    def __repr__(self):
        fields = [("humidity", self.humidity),
                  ("volatile_compounds", self.volatile_compounds),
                  ("temperature", self.temperature),
                  ("dust", self.dust)]
        string_fields = map(lambda x: f"{x[0]}={x[1]}", fields)
        return 'EnvironmentState(' + ",".join(string_fields) + ')'

