"""
broker.py

MQTT class for broker devices
"""

from Deployment.MQTT.mqtt import MQTT


class Broker(MQTT):

    def __init__(self, name, network_name, broker):

        # MQTT broker parameters
        super(Broker, self).__init__(name, network_name, broker)

        # Subscribe topic
        self.subscribe_topics = list()

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
                types = self.find_device_types()
            if not types:
                print("No devices online...")
            else:
                for device_type in types:
                    topic = self.network_topic + device_type + '/'
                    messages = self.get_message(topic, seconds=60)
                    for name in messages:
                        if name not in self.found_devices:
                            self.found_devices.append(name)
                            tag = self.get_device_tag(topic=(topic + name + '/'))
                            status = self.get_status(topic=topic + name + '/' + 'status/')
                            self.devices.append([device_type, name, tag, status])
        else:
            for name in names:
                topic = self.network_topic + '+' + '/' + name + '/'
                tag = self.get_device_tag(topic=topic)
                status = self.get_status(topic=topic + 'status/')
                self.devices.append(['unknown type', name, tag, status])
        return self.devices

    def reset(self):
        """Resets search

        """
        self.found_devices = []
        self.subscribe_topics = []
        self.devices = []
