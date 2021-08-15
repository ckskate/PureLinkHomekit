import asyncio
from asyncio_mqtt import Client, MqttError
from contextlib import AsyncExitStack, asynccontextmanager

from util.hasher import hash_password
from util.constants import DEVICE_NUMBER
from model.state import DeviceState
from assembler.state_assembler import StateAssembler


class Fan:
    username: str
    password: str
    stack: AsyncExitStack
    mqttc: Client
    command_path: str

    @staticmethod
    async def _init(username: str,
                    password: str,
                    stack: AsyncExitStack):
        fan = Fan(username, password, stack)
        await fan.mqttc.connect()
        await fan.mqttc.subscribe(f"{DEVICE_NUMBER}/{username}/status/current")
        return fan

    # Only meant for internal usage, use _init(...) instead
    def __init__(self,
                 username: str,
                 password: str,
                 stack: AsyncExitStack):
        self.username = username
        self.password = hash_password(password)
        self.stack = stack
        self.command_path = f"{DEVICE_NUMBER}/{username}/command"
        self.mqttc = Client(f"{username}.local",
                            port=1883,
                            username=f"{username}",
                            password=f"{self.password}")

    async def read_state(self) -> None:
        messages = await self.stack.enter_async_context(
                             self.mqttc.unfiltered_messages()
                         )
        async for message in messages:
            dto = StateAssembler().state_from_message_json(message.payload)
            print(repr(dto))


if __name__ == "__main__":
    import configparser

    config = configparser.ConfigParser()
    config.read('user.ini')
    user = config['User']
    username = user['id']
    password = user['pass']

    async def main():
        async with AsyncExitStack() as stack:
            client = await Fan._init(username, password, stack)

            while True:
                try:
                    await client.read_state()
                except Exception:
                    break

    asyncio.run(main())

