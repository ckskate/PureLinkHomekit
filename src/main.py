import asyncio
import json
import signal, pathlib
import configparser

from contextlib import AsyncExitStack, asynccontextmanager
from asyncio_mqtt import Client, MqttError
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader

from homekit_fan import HomekitFan


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('user.ini')
    user = config['User']
    username = user['id']
    password = user['pass']

    persist_filepath = str(pathlib.PurePath(__file__).parent.parent) + "/fan_device.state"
    async def main():
        async with AsyncExitStack() as stack:
            driver = AccessoryDriver(persist_file=persist_filepath,
                                     pincode="000-00-000".encode("ascii"))

            fan = await HomekitFan._init(username, password, driver, stack)
            driver.add_accessory(accessory=fan)

            signal.signal(signal.SIGTERM, driver.signal_handler)
            return driver

    driver = asyncio.run(main())
    driver.start()

