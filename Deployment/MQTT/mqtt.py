"""
mqtt.py


"""

import paho.mqtt.client as mqtt
import time
import copy


class MQTT(object):

    def __init__(self, name, network_name, broker):

        # MQTT broker, default broker is locally running
        self.broker = broker
        self.mqtt_port = 1883

        # MQTT client
        self.mqtt_client = mqtt.Client(name)

        # Name of network
        self.network_name = network_name
        self.network_topic = self.network_name + '/'

        # Saves found devices here
        self.found_devices = list()

        # Saves messages from MQTT
        self.messages = list()

    def get_device_tag(self, topic):
        """Gets the tag of a device

        :param topic: A topic with 'device_type/device_name/' format
        :return: Tag
        """

        found = False
        tag = None
        while not found:
            messages = self.get_message(topic)
            if messages:
                tag = messages[0]
                found = True
        return tag

    def find_device_types(self):
        """Find device types that are online in the network

        :return: A list of device types
        """

        device_types = set()
        messages = self.get_message(self.network_topic, seconds=60)
        if messages:
            for message in messages:
                device_types.add(message)
        return device_types

    def get_message(self, topic, seconds=5):
        """Gets messages from a MQTT stream

        :param topic: Topic to subscribe too
        :param seconds: How long to wait for message -> Int
        :return: List of messages from MQTT stream
        """
        self.mqtt_client.connect(self.broker, self.mqtt_port)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe(topic)
        self.mqtt_client.on_message = self.on_message
        time.sleep(seconds)
        self.mqtt_client.loop_stop()

        messages = copy.deepcopy(self.messages)
        self.messages = []
        return messages

    def on_message(self, client, userdata, message):
        """Callback function for MQTT

        """

        # Message from device
        device_message = str(message.payload.decode("utf-8"))
        self.messages.append(device_message)
