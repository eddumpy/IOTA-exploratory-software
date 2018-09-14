"""
mqtt.py

MQTT object provides methods to get messages from mqtt topics
"""

import paho.mqtt.client as mqtt
import time
import copy


class MQTT(object):

    def __init__(self, network_name, broker):

        # MQTT broker, default broker is locally running
        self.broker = broker
        self.mqtt_port = 1883

        # MQTT client
        self.mqtt_client = mqtt.Client()

        # Name of network
        self.network_name = network_name
        self.network_topic = self.network_name + '/'

        # Saves found devices here
        self.found_devices = list()

        # Saves messages from MQTT
        self.messages = list()

    def get_single_message(self, topic, wait_seconds=5):
        """Returns a message from a topic where only 1 message will be posted.
        (For example, finding a device tag as only the tag is getting posted here.)

        :param topic: A topic with 'network_name/device_type/device_name/' format
        :param wait_seconds: Time given to check MQTT topic
        :return: The message found on the given topic
        """

        while True:
            messages = self.get_message(topic, seconds=wait_seconds)
            if messages:
                m = messages[0]
                return m

    def find_messages(self, topic, wait_seconds=60):
        """Retrieves a list of messages from a topic, where different messages will be posted
        (For example, at the network level there are several device types that are posted here)

        :param topic: Topic with either 'network_name/device_type/' or 'network_name/' format
        :param wait_seconds: Time to check MQTT messages
        :return: A list of messages
        """

        m = set()
        messages = self.get_message(topic, seconds=wait_seconds)
        if messages:
            for message in messages:
                m.add(message)
        return m

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

        # Copy messages
        messages = copy.deepcopy(self.messages)

        # Resets variable to empty
        self.messages = []
        return messages

    def on_message(self, client, userdata, message):
        """Callback function for MQTT, used to retrieve messages from MQTT topics
        """

        # Message from device
        device_message = str(message.payload.decode("utf-8"))

        # Save to object variable
        self.messages.append(device_message)
