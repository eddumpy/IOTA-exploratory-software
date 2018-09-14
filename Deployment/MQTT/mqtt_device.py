"""mqtt_device.py

Sub-class of MQTT class for device scripts
"""

from Deployment.MQTT.mqtt import MQTT
from iota import Tag
import time


class MqttDevice(MQTT):

    def __init__(self, network_name, broker):

        super(MqttDevice, self).__init__(network_name, broker)

        # Initialises a list for publish and subscribe topics
        self.publish_topics = list()
        self.subscribe_topics = list()

        # Saves found tags here
        self.tags_found = list()

    def publish_device(self, device_details):
        """Publishes messages to the devices publish_topics

        :param device_details: List of details of the device
        """

        # Creates publish topics
        if not self.publish_topics:
            self.publish_topics = [device_details[0] + '/',
                                   device_details[0] + '/' + device_details[1] + '/',
                                   device_details[0] + '/' + device_details[1] + '/' + device_details[2] + '/']

        # Connects to broker and publishes details to topics
        self.mqtt_client.connect(self.broker, self.mqtt_port)
        self.mqtt_client.loop_start()
        for x in range(1, 4):
            self.mqtt_client.publish(self.publish_topics[x - 1], device_details[x])
        time.sleep(2)
        self.mqtt_client.loop_stop()

    def find_devices(self, topics, num_of_streams):
        """Finds online devices

        :param topics: Topics to subscribe too
        :param num_of_streams: How many streams to read
        :return: a list of the found devices
        """

        # Describes state of found devices
        all_devices_found = False

        # Find devices
        while not all_devices_found:
            for topic in topics:
                messages = self.get_message(topic)
                for message in messages:
                    if message not in self.found_devices:
                        print("Found: ", message)
                        self.found_devices.append(message)
                        if len(self.found_devices) == num_of_streams:
                            all_devices_found = True
                            break
        return self.found_devices

    def find_device_tags(self, devices, num_of_streams, read_from):
        """Finds data streams by finding tags of devices in the network

        :param devices: Names of devices
        :param num_of_streams: How many streams to find
        :param read_from: What device to read from
        :return: List of found tags
        """

        if not devices:
            topics = [self.network_name + '/' + read_from + '/']
            self.find_devices(topics, num_of_streams)
            self.subscribe_topics = [topics[0] + device_name + '/' for device_name in self.found_devices]
            devices = self.found_devices
        else:
            self.subscribe_topics = [self.network_name + '/' + read_from + '/' + device + '/'
                                     for device in devices]

        for topic in self.subscribe_topics:

            # Prints an update on how many streams are needed to be found still
            print("Searching for tags of devices: ",
                  " ".join(devices))

            tag_found = False

            while not tag_found:
                tag = self.get_single_message(topic)
                if tag not in self.tags_found:
                    print('Found tag: ', tag)
                    self.tags_found.append(tag)
                    tag_found = True

        # Prints which devices are being read
        print("Reading data streams from these devices: ", " ".join(devices))
        tags = [Tag(tag) for tag in self.tags_found]
        return tags
