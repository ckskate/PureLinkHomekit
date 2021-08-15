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

    current_fan_state: Optional[DeviceState]
    current_environment_state: Optional[EnvironmentState]
    fan_service: FanService
    exit_stack: AsyncExitStack

    @staticmethod
    async def _init(username: str,
                    password: str,
                    driver: AccessoryDriver,
                    exit_stack: AsyncExitStack):
        fan_service = await FanService._init(username, password, stack)
        fan = HomekitFan(username, password, driver, fan_service, exit_stack)
        return fan

    # Only meant for internal usage, use _init(...) instead
    def __init__(self,
                 username: str,
                 password: str,
                 driver: AccessoryDriver,
                 fan_service: FanService,
                 exit_stack: AsyncExitStack):
        super().__init__(driver, display_name="Dyson PureLink")

        self.fan_service = fan_service
        self.current_fan_state = None
        self.current_environment_state = None
        self.exit_stack = exit_stack

        self.set_info_service(firmware_revision="0.1",
                              manufacturer="Saul T. Dong, BBC",
                              model="Dyson Pure Cool Link",
                              serial_number="69")

        homekit_fan = self.add_preload_service("")

