import asyncio
import json
import signal, pathlib, logging
import configparser

from contextlib import AsyncExitStack, asynccontextmanager
from asyncio_mqtt import Client, MqttError
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader

from homekit_fan import HomekitFan


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = configparser.ConfigParser()
    config.read('user.ini')
    user = config['User']
    username = user['id']
    password = user['pass']

    loop = asyncio.get_event_loop()

    persist_filepath = str(pathlib.PurePath(__file__).parent.parent) + "/fan_device.state"
    driver = AccessoryDriver(persist_file=persist_filepath, loop=loop)

    fan = HomekitFan(username, password, driver)
    driver.add_accessory(accessory=fan)

    def signal_handler(_sig, _frame):
        driver.stop()
        # kill the run loop later with some time for
        # things to shut down
        loop.call_later(4, loop.stop)

    signal.signal(signal.SIGINT, signal_handler)
    driver.start()

