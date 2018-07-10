"""
mqtt class

Uses the MQTT protocol to communicate with devices. Tags are sent published to topics,
which devices, if subscribed to, can read the tags so they can access the data stream
"""

import paho.mqtt.client as mqtt
import time


class MQTT:

    def __init__(self,
                 device_name,
                 broker="localhost",
                 subscribe_topic='',
                 publish_topic=''):

        # MQTT broker, default broker is locally running
        self.broker = broker
        self.mqtt_port = 1883

        # MQTT client
        self.mqtt_client = mqtt.Client(device_name)

        # MQTT topics
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic

        # Stores found tags here, uses a list in case of multiple data streams
        self.tags_found = set()

    def publish_data_stream(self, tag_string):
        """Publishes messages to the objects publish_topic

        :param tag_string: The string of a given tag
        """
        self.mqtt_client.connect("localhost")
        self.mqtt_client.loop_start()
        print("Publishing tag: ", tag_string, " to ", self.publish_topic)
        self.mqtt_client.publish(self.publish_topic, tag_string)
        time.sleep(5)
        self.mqtt_client.loop_stop()

    def find_data_streams(self, number_of_streams=1):
        """Finds data streams for devices to read

        :param number_of_streams: Number of data streams wanting to analyse -> Int
        """

        self.mqtt_client = mqtt.Client("monitor1")
        self.mqtt_client.connect("localhost")
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe(self.subscribe_topic)
        self.mqtt_client.on_message = self.on_message
        time.sleep(10)
        self.mqtt_client.loop_stop()

        if len(self.tags_found) == number_of_streams:
            print("Reading from found data streams...")
        else:
            print(len(self.tags_found), " number of data streams found...")
            self.find_data_streams(number_of_streams)

    def on_message(self, client, userdata, message):
        device_tag = str(message.payload.decode("utf-8"))
        print("Tag found ", device_tag, " in topic ", message.topic)
        self.tags_found.add(device_tag)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully to broker!")
        else:
            print("Connected with result code " + str(rc))