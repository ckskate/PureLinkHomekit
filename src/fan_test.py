import asyncio
import logging
from asyncio_mqtt import Client, MqttError
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Dict, Union, Any, Optional

from util.hasher import hash_password
from util.constants import *
from model.state import DeviceState, EnvironmentState
from model.command import Command
from assembler.state_assembler import StateAssembler
from assembler.command_assembler import CommandAssembler


logger = logging.getLogger(__name__)

class FanService:
    username: str
    password: str
    mqttc: Client
    command_topic: str

    most_recent_state: Optional[DeviceState]
    most_recent_environment_state: Optional[EnvironmentState]
    task: Optional[asyncio.Task]

    def __init__(self,
                 username: str,
                 password: str):
        self.username = username
        self.password = hash_password(password)
        self.command_topic = f"{DEVICE_NUMBER}/{username}/command"
        self.mqttc = Client(f"{username}.local",
                            port=1883,
                            username=f"{username}",
                            password=f"{self.password}")
        self.most_recent_state = None
        self.most_recent_environment_state = None
        self.task = None

    async def start_reading(self):
        # start reading the states
        self.task = asyncio.get_running_loop().create_task(self._read_loop())

    async def _read_loop(self):
        while True:
            try:
                await self._read_states()
            except MqttError as error:
                logger.info(f'error: "{error}". reconnecting in 3 seconds.')
            finally:
                await asyncio.sleep(3)

    async def _read_states(self) -> None:
        async with AsyncExitStack() as stack:
            self.read_operation_stack = stack
            assembler = StateAssembler()

            # connect
            await stack.enter_async_context(self.mqttc)

            # subscribe
            await self.mqttc.subscribe(f"{DEVICE_NUMBER}/{self.username}/status/current")

            # the messages
            messages = await stack.enter_async_context(
                                 self.mqttc.unfiltered_messages())
            async for message in messages:
                state = assembler.state_from_message_json(message.payload)
                if isinstance(state, DeviceState):
                    self.most_recent_state = state
                elif isinstance(state, EnvironmentState):
                    self.most_recent_environment_state = state

    async def cancel_task(self):
        if self.task == None or self.task.done():
            return
        try:
            self.task.cancel()
            await self.task
        except asyncio.CancelledError:
            pass

    async def request_states(self) -> None:
        #await asyncio.gather(self.write_command(Command(CommandType.REQUEST_STATE)),
        #                     self.write_command(Command(CommandType.REQUEST_ENVIRONMENT_STATE)))
        await self.write_command(Command(CommandType.REQUEST_STATE))

    async def write_command(self, command: Command) -> None:
        command_json = CommandAssembler().json_from_command(command)
        logger.info(command_json)
        await self.mqttc.publish(self.command_topic, command_json, qos=1)

    async def disconnect(self) -> None:
        if self.task != None:
            await self.cancel_task()
            self.task = None


if __name__ == "__main__":
    import configparser

    config = configparser.ConfigParser()
    config.read('user.ini')
    user = config['User']
    username = user['id']
    password = user['pass']

    async def main():
        async with AsyncExitStack() as stack:
            client = await FanService._init(username, password, stack)

            while True:
                try:
                    device_state = client.most_recent_state
                    print(repr(device_state))
                    await asyncio.sleep(2)

                    await client.request_states()
                    print("here")
                except Exception:
                    break

    asyncio.run(main())

