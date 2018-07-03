from iota import Tag
from node import Node
from client import Client
import time
import random
import requests


"""Client-v1

This python script represents a sensing IoT device. Every 2 minutes, the device will store a 
random number between 0-9 on to the tangle.
"""


def main():

    print("Device collecting data...")

    try:
        while True:
            # Generate random number as the data to store in the tangle and convert to Trytestring
            sensor_data = random.randint(0, 9)

            # Post data to tangle
            client.post_to_tangle(sensor_data)

            # Wait 2 minutes for next data collection
            time.sleep(120)

    # Catches any connection errors when collecting data
    except requests.exceptions.ConnectionError:
        print("Connection error...restarting in 1 min")
        time.sleep(60)
        main()


# Connect to node and create api instance
node = Node()
api = node.create_api()
node.test_node(api)

# Tag of this device
sensor_tag = Tag(b'SENSOR')

# Create a client object, and pass in api and tag of device
client = Client(api, sensor_tag)

if __name__ == '__main__':
    main()
