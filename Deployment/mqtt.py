"""
mqtt.py

Provides a class that uses the MQTT protocol to communicate with devices and is used by client.py.
Tags are published to topics, which devices, if subscribed to, can read the tags to access their data streams
"""

import paho.mqtt.client as mqtt
import time


class MQTT:

    def __init__(self, device_name, broker, subscribe_topic, publish_topic, known_devices,
                 number_of_streams):

        # MQTT broker, default broker is locally running
        self.broker = broker
        self.mqtt_port = 1883

        # MQTT client
        self.mqtt_client = mqtt.Client(device_name)

        # MQTT topics
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic

        # Finds known devices
        if known_devices is None:
            self.known_devices = []
            self.number_of_streams = number_of_streams
        else:
            self.known_devices = known_devices
            self.number_of_streams = len(known_devices)

        # Stores found tags and devices here, uses a set in case of multiple data streams
        self.tags_found = list()
        self.devices_found = list()

    def publish_data_stream(self, message):
        """Publishes messages to the objects publish_topic

        :param message: Message string
        """

        self.mqtt_client.connect("localhost", self.mqtt_port)
        self.mqtt_client.loop_start()
        self.mqtt_client.publish(self.publish_topic, message)
        time.sleep(4)
        self.mqtt_client.loop_stop()

    def find_data_streams(self):
        """Finds data streams for devices to read

        """

        self.mqtt_client.connect("localhost", self.mqtt_port)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe(self.subscribe_topic)
        self.mqtt_client.on_message = self.on_message
        time.sleep(4)
        self.mqtt_client.loop_stop()

        if len(self.tags_found) == self.number_of_streams:
            print("Reading from found data streams, from:\n", "\n".join(self.devices_found))
        else:
            if self.known_devices:
                print("Searching for", " ".join([device for device in self.known_devices if device not in self.devices_found]))
            else:
                print("Searching for data streams, ", len(self.tags_found), " found")
            self.find_data_streams()

    def on_message(self, client, userdata, message):

        # Message from device
        device_message = str(message.payload.decode("utf-8"))

        # Index of '/' to use to split string
        i = device_message.find('/')
        device_name, device_tag = device_message[:i], device_message[(i + 1):]

        # If no name was given, default unknown device is given
        if len(device_name) == 0:
            device_name = "Unknown device"

        if self.known_devices:
            if device_name in self.known_devices:
                self.tags_found.append(device_tag)
                self.devices_found.append(device_name)
        else:
            if len(self.tags_found) < self.number_of_streams:
                self.tags_found.append(device_tag)
                self.devices_found.append(device_name)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully to broker!")
        else:
            print("Connected with result code " + str(rc))
