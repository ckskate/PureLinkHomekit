import sys
import asyncio
from typing import Dict, Union, Any, Optional
from contextlib import AsyncExitStack, asynccontextmanager

from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_FAN

from model.state import DeviceState, EnvironmentState
from model.command import Command
from fan_test import FanService
from util.constants import *


class HomekitFan(Accessory):

    category = CATEGORY_FAN

    fan_service: FanService

    def __init__(self,
                 username: str,
                 password: str,
                 driver: AccessoryDriver):
        super().__init__(driver, display_name="Dyson PureLink")

        self.fan_service = FanService(username, password)

        self.set_info_service(firmware_revision="0.1",
                              manufacturer="Saul T. Dong, BBC",
                              model="Dyson Pure Cool Link",
                              serial_number="69")

        fan = self.add_preload_service("Fanv2", chars=["Active", "RotationSpeed", "SwingMode"])
        self.active_char = fan.get_characteristic("Active")
        self.speed_char = fan.get_characteristic("RotationSpeed")
        self.rotation_char = fan.get_characteristic("SwingMode")

        fan.setter_callback = self.update_state

    async def run(self):
        await self.fan_service.start_reading()
        await self.update_device()

    @Accessory.run_at_interval(3)
    async def update_device(self):
        try:
            await self.fan_service.request_states()
        except Exception:
            return

        current_state = self.fan_service.most_recent_state

        if current_state == None:
            return

        self.active_char.set_value(current_state.fan_state.homekit_value())
        self.speed_char.set_value(current_state.speed.homekit_value())
        self.rotation_char.set_value(current_state.oscillation.homekit_value())

    async def stop(self):
        try:
            await self.fan_service.disconnect()
        except Exception:
            return

    def update_state(self, char_values: Dict[str, Any]) -> None:
        is_active = (FanMode.from_homekit_value(char_values['Active'])
                        if 'Active' in char_values else None)
        if 'RotationSpeed' in char_values and char_values['RotationSpeed'] == 0.0:
            is_active = FanState.FAN_OFF
        rotation_speed = (FanSpeed.from_homekit_value(char_values['RotationSpeed'])
                            if 'RotationSpeed' in char_values else None)
        oscillation = (Oscillation.from_homekit_value(char_values['SwingMode'])
                        if 'SwingMode' in char_values else None)

        desired_state = self.fan_service.most_recent_state.state_setting_values_to(fan_mode=is_active,
                                                                                   speed=rotation_speed,
                                                                                   oscillation=oscillation)
        state_command = Command(CommandType.SET_STATE, desired_state)
        self.driver.add_job(self.fan_service.write_command(state_command))

