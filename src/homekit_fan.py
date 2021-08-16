import asyncio
from typing import Dict, Union, Any, Optional
from contextlib import AsyncExitStack, asynccontextmanager

from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_FAN

from model.state import DeviceState, EnvironmentState
from fan_test import FanService


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

    async def start(self):
        await self.fan_service.start_reading()

    @Accessory.run_at_interval(3)
    async def run(self):
        try:
            await self.fan_service.request_states()
        except Exception:
            return

        current_state = self.fan_service.most_recent_state

        if current_state == None:
            print("current state was none")
            return

        self.active_char.set_value(current_state.fan_state.homekit_value())
        self.speed_char.set_value(current_state.speed.homekit_value())
        self.rotation_char.set_value(current_state.oscillation.homekit_value())

    async def stop(self):
        await self.fan_service.disconnect()

    def update_state(self, char_values: Dict[str, Any]) -> None:
        is_active = (FanState.from_homekit_value(char_values['Active'])
                        if 'Active' in char_values else None)
        rotation_speed = (FanSpeed.from_homekit_value(char_values['RotationSpeed'])
                            if 'RotationSpeed' in char_values else None)
        oscillation = (Oscillation.from_homekit_value(char_values['SwingMode'])
                        if 'SwingMode' in char_values else None)

        desired_state = self.fan_service.most_recent_state.state_setting_values_to(fan_state=is_active,
                                                                                   speed=rotation_speed,
                                                                                   oscillation=oscillation)
        state_command = Command(CommandType.SET_STATE, desired_state)
        self.driver.add_job(self.fan_service.write_command(state_command))

