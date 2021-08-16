import asyncio
from asyncio_mqtt import Client, MqttError
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Dict, Union, Any, Optional

from util.hasher import hash_password
from util.constants import *
from model.state import DeviceState, EnvironmentState
from model.command import Command
from assembler.state_assembler import StateAssembler
from assembler.command_assembler import CommandAssembler


class FanService:
    username: str
    password: str
    stack: AsyncExitStack
    mqttc: Client
    command_topic: str
    most_recent_state: Optional[DeviceState]
    most_recent_environment_state: Optional[EnvironmentState]

    @staticmethod
    async def _init(username: str,
                    password: str,
                    stack: AsyncExitStack):
        fan_service = FanService(username, password, stack)
        await fan_service.mqttc.connect()
        await fan_service.mqttc.subscribe(f"{DEVICE_NUMBER}/{username}/status/current")
        # start reading the states
        asyncio.get_event_loop().create_task(fan_service.read_states())
        return fan_service

    # Only meant for internal usage, use _init(...) instead
    def __init__(self,
                 username: str,
                 password: str,
                 stack: AsyncExitStack):
        self.username = username
        self.password = hash_password(password)
        self.stack = stack
        self.command_topic = f"{DEVICE_NUMBER}/{username}/command"
        self.mqttc = Client(f"{username}.local",
                            port=1883,
                            username=f"{username}",
                            password=f"{self.password}")
        self.most_recent_state = None
        self.most_recent_environment_state = None

    async def read_states(self) -> None:
        print("running read states")
        messages = await self.stack.enter_async_context(
                             self.mqttc.unfiltered_messages()
                         )
        async for message in messages:
            state = StateAssembler().state_from_message_json(message.payload)
            if isinstance(state, DeviceState):
                self.most_recent_state = state
            elif isinstance(state, EnvironmentState):
                self.most_recent_environment_state = state

    async def request_states(self) -> None:
        #await asyncio.gather(self.write_command(Command(CommandType.REQUEST_STATE)),
        #                     self.write_command(Command(CommandType.REQUEST_ENVIRONMENT_STATE)))
        await self.write_command(Command(CommandType.REQUEST_STATE))

    async def write_command(self, command: Command) -> None:
        command_json = CommandAssembler().json_from_command(command)
        print(command_json)
        await self.mqttc.publish(self.command_topic, command_json, qos=1)

    async def disconnect(self) -> None:
        await self.mqttc.disconnect()


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

