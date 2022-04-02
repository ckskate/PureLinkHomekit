"""homekit accessory for the fan."""

from typing import Dict, Any

from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_FAN
from asyncio_mqtt import MqttError

from src import model
from src import fan_service


class HomekitFan(Accessory):
  """HAP fan accessory for the dyson fan."""

  category = CATEGORY_FAN

  service: fan_service.FanService

  def __init__(self,
               username: str,
               password: str,
               driver: AccessoryDriver):
    super().__init__(driver, display_name="Dyson PureLink")

    self.service = fan_service.FanService(username, password)
    fan = self.add_preload_service("Fanv2",
                                   chars=["Active",
                                          "RotationSpeed",
                                          "SwingMode"])
    fan.setter_callback = self.__update_state

    self.active_char = fan.get_characteristic("Active")
    self.speed_char = fan.get_characteristic("RotationSpeed")
    self.rotation_char = fan.get_characteristic("SwingMode")
    self.set_info_service(firmware_revision="1.0",
                          manufacturer="Hot Wind Labs",
                          model="Dyson Pure Cool Link",
                          serial_number="69")


  async def run(self):
    await self.service.start_main_run_loop()
    await self._update_device()

  @Accessory.run_at_interval(3)
  async def _update_device(self):
    """updates the homekit device state to match the state read from fan."""

    try:
      await self.service.request_states()
    except MqttError:
      return

    current_state = self.service.most_recent_state
    if current_state is None:
      return
    self.active_char.set_value(current_state.fan_state.homekit_value())
    self.speed_char.set_value(current_state.speed.homekit_value())
    self.rotation_char.set_value(current_state.oscillation.homekit_value())

  async def stop(self):
    try:
      await self.service.disconnect()
    except MqttError:
      return

  def __update_state(self, char_values: Dict[str, Any]) -> None:
    is_active = None
    modified_state = None
    rotation_speed = None
    oscillation = None
    if 'Active' in char_values:
      is_active = model.FanMode.from_homekit_value(char_values['Active'])
    if 'SwingMode' in char_values:
      oscillation = (model.Oscillation
                          .from_homekit_value(char_values['SwingMode']))
    if ('RotationSpeed' in char_values
        and char_values['RotationSpeed'] == 0.0):
      is_active = model.FanState.FAN_OFF
    if 'RotationSpeed' in char_values:
      rotation_speed = (model.FanSpeed
                          .from_homekit_value(char_values['RotationSpeed']))
    modified_state = (self.service
                         .most_recent_state
                         .state_setting_values_to(fan_mode=is_active,
                                                  speed=rotation_speed,
                                                  oscillation=oscillation))
    state_command = model.Command(model.CommandType.SET_STATE,
                                  modified_state)
    self.driver.add_job(self.service.write_command(state_command))
