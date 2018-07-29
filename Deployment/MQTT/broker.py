"""
broker.py

MQTT class for broker devices
"""

from Deployment.MQTT.mqtt import MQTT
from iota import Tag


class MqttBroker(MQTT):

    def __init__(self, name, network_name, broker):

        # MQTT broker parameters
        super(MqttBroker, self).__init__(name, network_name, broker)

        # Saves devices
        self.devices = list()

    def find_devices(self, types=None, names=None):
        """Find devices currently online

        :param types: Types of devices
        :param names: Names of devices
        :return: Device details -> [[type, name, tag]]
        """

        if names is None:
            if types is None:
                types = self.find_messages(self.network_topic)
            if not types:
                print("No devices online...")
            else:
                for device_type in types:
                    topic = self.network_topic + device_type + '/'
                    names = self.find_messages(topic)
                    for name in names:
                        self.found_devices.append(name)
                        tag = Tag(self.get_single_message(topic=(topic + name + '/')))
                        self.devices.append([device_type, name, tag])
        else:
            for name in names:
                topic = self.network_topic + '+' + '/' + name + '/'
                tag = self.get_single_message(topic=topic)
                self.devices.append(['unknown type', name, tag])
        return self.devices

    def reset(self):
        """Resets search

        """
        self.found_devices = []
        self.devices = []
