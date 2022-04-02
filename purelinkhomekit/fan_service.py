"""handles MQTT communication with the fan."""

import asyncio
import logging
from contextlib import AsyncExitStack
from typing import Optional

from asyncio_mqtt import Client, MqttError

from purelinkhomekit import util
from purelinkhomekit import model
from purelinkhomekit import assembler

logger = logging.getLogger(__name__)

class FanService:
  """class responsible for communicating with the fan."""

  username: str
  password: str
  mqttc: Client
  command_topic: str

  most_recent_state: Optional[model.DeviceState]
  task: Optional[asyncio.Task]

  def __init__(self,
               name: str,
               psk: str):
    self.username = name
    self.password = util.hash_password(psk)
    self.command_topic = f"{model.DEVICE_NUMBER}/{name}/command"
    self.most_recent_state = None
    self.most_recent_environment_state = None
    self.task = None

  async def start_main_run_loop(self):
    """starts the update loop for the fan."""
    self.task = (asyncio.get_running_loop()
                       .create_task(self.__run_main_loop()))

  async def request_states(self) -> None:
    """requests a state update from the fan."""
    await self.write_command(model.Command(model.CommandType.REQUEST_STATE))

  async def write_command(self, command: model.Command) -> None:
    """sends the given command to the fan."""
    command_json = assembler.command_assembler.command_to_json(command)
    logger.info(command_json)
    await self.mqttc.publish(self.command_topic, command_json, qos=1)

  async def disconnect(self) -> None:
    """stops the main device update loop and disconnects."""
    if self.task is not None:
      await self.__stop_main_loop()
      self.task = None

  async def __run_main_loop(self):
    while True:
      try:
        await self.__read_states()
      except MqttError as error:
        logger.info('error: "%s". reconnecting in 3 seconds.', error)
      finally:
        await asyncio.sleep(3)
        logger.info('reconnecting!')

  async def __read_states(self) -> None:
    async with AsyncExitStack() as stack:
      # refresh the client details (necessary on re-connection)
      self.mqttc = Client(f"{self.username}.local",
                          port=1883,
                          username=f"{self.username}",
                          password=f"{self.password}")

      # connect
      await stack.enter_async_context(self.mqttc)

      # subscribe
      await self.mqttc.subscribe(f"{model.DEVICE_NUMBER}/"
                                 f"{self.username}/status/current")

      # the messages
      messages = await stack.enter_async_context(self.mqttc
                                                     .unfiltered_messages())
      async for message in messages:
        state = (assembler.state_assembler
                          .state_from_message_json(message.payload))
        if isinstance(state, model.DeviceState):
          self.most_recent_state = state

  async def __stop_main_loop(self):
    if self.task is None or self.task.done():
      return
    try:
      self.task.cancel()
      await self.task
    except asyncio.CancelledError:
      pass
