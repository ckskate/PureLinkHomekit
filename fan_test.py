import json
import paho.mqtt.client as mqtt

import hasher
from constants import DEVICE_NUMBER
from state import DeviceState
from state_assembler import StateAssembler

assembler = StateAssembler()

class Fan:
    username: str
    password: str
    mqttc: mqtt.Client

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = hasher.hash_password(password)

        self.mqttc = mqtt.Client()

        self.mqttc.on_connect = self._subscribe_to_topics
        self.mqttc.on_message = self.testRead
        self.mqttc.username_pw_set(self.username,
                                   password=self.password)
        self.mqttc.connect("{0}.local".format(username),
                           port=1883)
        self.mqttc.loop_forever()

    def _subscribe_to_topics(self, client, userdata, flags, rc) -> None:
        client.subscribe("{0}/{1}/status/current".format(DEVICE_NUMBER,
                                                         self.username))

    def testRead(self, client, userdata, message) -> None:
        dto = json.loads(message.payload)
        dto = assembler.state_from_command_json(dto)
        print(repr(dto))


if __name__ == "__main__":
    import configparser

    config = configparser.ConfigParser()
    config.read('user.ini')
    user = config['User']
    username = user['id']
    password = user['pass']

    client = Fan(username, password)

