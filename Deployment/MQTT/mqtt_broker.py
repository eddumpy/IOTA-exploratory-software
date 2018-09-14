"""
mqtt_broker.py

Sub-class of the MQTT class for brokerscript
"""

from Deployment.MQTT.mqtt import MQTT
from iota import Tag


class MqttBroker(MQTT):

    def __init__(self, network_name, broker):

        # MQTT broker parameters
        super(MqttBroker, self).__init__(network_name, broker)

        # Default name for broker
        self.device_name = 'broker'

        # Saves devices to this list
        self.devices = list()

    def find_devices(self, types=None, names=None):
        """Find devices currently online

        :param types: Types of devices
        :param names: Names of devices
        :return: Device details -> [[type, name, tag]]
        """

        # Finds device types in network, if names is None
        if names is None:
            if types is None:
                types = self.find_messages(self.network_topic)
            if not types:
                print("No devices online...")
                return self.devices
            else:

                # Find device names from found device types
                for device_type in types:
                    topic = self.network_topic + device_type + '/'
                    names = self.find_messages(topic)

                    # Finds the tag of found devices
                    for name in names:
                        self.found_devices.append(name)
                        tag = Tag(self.get_single_message(topic=(topic + name + '/')))
                        self.devices.append([device_type, name, tag])
        else:
            # If name is not None, get device tags
            for name in names:
                topic = self.network_topic + '+' + '/' + name + '/'
                tag = self.get_single_message(topic=topic)
                self.devices.append(['unknown type', name, tag])
        return self.devices

    def reset(self):
        """Method to reset search
        """

        self.found_devices = []
        self.devices = []
