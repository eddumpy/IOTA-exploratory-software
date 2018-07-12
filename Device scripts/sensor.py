"""
sensor.py

This python script represents a sensing IoT device. Every minute, the device will store a
random number between 0-9 on to the tangle.
"""

from Deployment.client import Client
import time
import random
import requests
import sys


def main():

    try:

        while True:

            # Generate random number as the data to store in the tangle and convert to Trytestring
            sensor_data = random.randint(0, 100)
            print(sensor_data)

            # Posts encrypted data to tangle
            client.post_to_tangle(sensor_data)

            # Wait 1 minutes for next data collection
            time.sleep(60)

            # Publishes tag to message stream again for recently connected devices
            client.mqtt.publish_data_stream(message=client.device_name + '/' + client.tag_string)

    # Catches any connection errors when collecting data
    except requests.exceptions.ConnectionError:
        print("Connection error...restarting data collection in 1 min")
        time.sleep(60)
        main()

    except KeyboardInterrupt:
        print("Ending data stream....")
        client.mqtt.publish_data_stream(message=client.device_name + '/' + 'stream_ended')
        sys.exit()


# Get a device name from the user
name = input("Please provide a name for the device: ")

# Create a client object with device seed, use a seed generator to get a seed.
client = Client(device_name=name,
                publish_topic="sensor/data",
                seed=b'GYZHOINRXAPJOIUIPEZATMDDYNQQZITJQTWMFDAUPWWAQNAURLGXQOOVQMAJUICWXIEIWDIBPGUQPBRMY')

if __name__ == '__main__':
    print("Starting stream, publishing ", client.message, " to ", client.publish_topic)
    client.mqtt.publish_data_stream(message=client.message)
    print("Data collection initiated...")
    main()
