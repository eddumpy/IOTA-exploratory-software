"""
sensor.py

This python script represents a sensing IoT device. Every 2 minutes, the device will store a
random number between 0-9 on to the tangle.
"""

from Classes.client import Client

import time
import random
import requests


def main():

    try:

        while True:

            # Generate random number as the data to store in the tangle and convert to Trytestring
            sensor_data = random.randint(0, 9)

            # Post data to tangle
            client.post_to_tangle(sensor_data)

            # Wait 1 minutes for next data collection
            time.sleep(60)

            # Publishes tag to message stream again for recently connected devices
            client.mqtt.publish_data_stream(tag_string=client.tag_string)

    # Catches any connection errors when collecting data
    except requests.exceptions.ConnectionError:
        print("Connection error...restarting in 1 min")
        time.sleep(60)
        main()


# Create a client object with device seed, use a seed generator to get a seed.
client = Client(device_name="Sensor1",
                publish_topic="sensor/data",
                seed=b'GYZHOINRXAPJOIUIPEZATMDDYNQQZITJQTWMFDAUPWWAQNAURLGXQOOVQMAJUICWXIEIWDIBPGUQPBRMY')

if __name__ == '__main__':
    print("Starting data stream, publishing tag to: ", client.publish_topic)
    client.mqtt.publish_data_stream(tag_string=client.tag_string)
    print("Device collecting data...")
    main()
