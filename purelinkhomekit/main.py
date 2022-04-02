"""main script to run the fan. call with `python3 main.py`."""

import asyncio
import signal
import pathlib
import logging
import configparser

from pyhap.accessory_driver import AccessoryDriver

from purelinkhomekit.homekit_fan import HomekitFan


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  CONFIG_FILEPATH = str(pathlib.PurePath(__file__).parent) + "/user.ini"
  PERSIST_FILEPATH = (str(pathlib.PurePath(__file__).parent.parent)
                      + "/fan_device.state")

  # read fan config file
  config = configparser.ConfigParser()
  config.read(CONFIG_FILEPATH)
  user = config['User']
  username = user['id']
  password = user['pass']

  loop = asyncio.get_event_loop()

  driver = AccessoryDriver(persist_file=PERSIST_FILEPATH,
                           loop=loop)

  fan = HomekitFan(username, password, driver)
  driver.add_accessory(accessory=fan)

  def signal_handler(_sig, _frame):
    """custom signal handler with time to shut down the fan connection."""
    driver.stop()
    # kill the run loop later with some time for
    # things to shut down
    loop.call_later(4, loop.stop)

  signal.signal(signal.SIGINT, signal_handler)
  driver.start()
