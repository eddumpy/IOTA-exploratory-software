"""
mqtt.py

Provides a class that uses the MQTT protocol to communicate with devices and is used by client.py.
Tags are published to topics, which devices, if subscribed to, can read the tags to access their data streams
"""

import paho.mqtt.client as mqtt
import time


class MQTT:

    def __init__(self, device_name, device_tag, device_type, read_from, broker, subscribe_topics, publish_topics, known_devices,
                 number_of_streams):

        # Name of device and its tag
        self.device_name = device_name
        self.device_tag = device_tag
        self.device_type = device_type

        # MQTT broker, default broker is locally running
        self.broker = broker
        self.mqtt_port = 1883

        # MQTT client
        self.mqtt_client = mqtt.Client(self.device_name)

        # Creates the subscribe topics, depends on if devices are known
        if read_from is None:
            self.subscribe_topics = []
        else:
            if not known_devices:
                self.subscribe_topics = [read_from + '/']
            else:
                self.subscribe_topics = [read_from + '/' + device for device in known_devices]

        # The publish topics
        self.publish_topics = [self.device_type + '/', self.device_type + '/' + self.device_name + '/']

        # MQTT topics
        self.subscribe_topics = subscribe_topics
        self.publish_topics = publish_topics

        # Devices to connect to
        self.known_devices = known_devices

        # How many streams to look for
        if not known_devices:
            self.number_of_streams = number_of_streams
        else:
            self.number_of_streams = len(known_devices)

        # Stores found tags and devices here, uses a set in case of multiple data streams
        self.tags_found = list()
        self.devices_found = list()

    def publish_data_stream(self):
        """Publishes messages to the devices publish_topics

        """

        self.mqtt_client.connect(self.broker, self.mqtt_port)
        self.mqtt_client.loop_start()
        self.mqtt_client.publish(self.publish_topics[0], self.device_name)
        self.mqtt_client.publish(self.publish_topics[1], self.device_tag)
        time.sleep(10)
        self.mqtt_client.loop_stop()

    def find_devices(self):

        # Describes state of found devices
        all_devices_found = False

        while not all_devices_found:
            self.mqtt_client.connect(self.broker, self.mqtt_port)
            self.mqtt_client.loop_start()
            self.mqtt_client.subscribe(self.subscribe_topics[0])
            self.mqtt_client.on_message = self.on_message
            time.sleep(2)
            self.mqtt_client.loop_stop()

            if len(self.known_devices) >= self.number_of_streams:
                all_devices_found = True

    def find_data_streams(self):
        """Finds data streams from known devices

        """

        # Finds devices for
        if not self.known_devices:
            self.find_devices()
            self.subscribe_topics = [self.subscribe_topics[0] + device_name + '/' for device_name in self.known_devices]

        # Variable to show how many tags have been found
        number_of_tags_found = 0

        for topic in self.subscribe_topics:

            self.number_of_streams_found()

            stream_found = False

            while not stream_found:
                self.mqtt_client.connect(self.broker, self.mqtt_port)
                self.mqtt_client.loop_start()
                self.mqtt_client.subscribe(topic)
                self.mqtt_client.on_message = self.on_message
                time.sleep(2)
                self.mqtt_client.loop_stop()

                if len(self.tags_found) > number_of_tags_found:
                    number_of_tags_found = len(self.tags_found)
                    stream_found = True

        if len(self.tags_found) == self.number_of_streams:
            print("Reading data streams from these devices: ", " ".join(self.devices_found))

    def number_of_streams_found(self):
        print("Searching for device tags for devices: ",
              " ".join([device for device in self.known_devices if device not in self.devices_found]))

    def on_message(self, client, userdata, message):

        # Message from device
        device_message = str(message.payload.decode("utf-8"))

        if len(device_message) == 27:
            if device_message not in self.tags_found:
                self.tags_found.append(device_message)
        else:
            if device_message not in self.known_devices:
                print("Added ", device_message, " to known devices")
                self.known_devices.append(device_message)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully to broker!")
        else:
            print("Connected with result code " + str(rc))
