from iota import Tag
from node import Node
from client import Client
import time
import random
import requests


def main():
    print("Device collecting data...")

    try:
        while True:
            # Generate random number as the data to store in the tangle and convert to Trytestring
            sensor_data = random.randint(0, 9)

            # Post data to tangle
            client.post_to_tangle(sensor_data, sensor_tag)

            # Wait 2 minutes for next data collection
            time.sleep(120)

    except requests.exceptions.ConnectionError:
        print("Connection error...restarting in 1 min")
        time.sleep(60)
        main()


# Connect to node and create api instance
node = Node()
api = node.create_api()
node.test_node(api)

# Tag of this device.
sensor_tag = Tag(b'SENSOR')

# Client library.
client = Client(api, sensor_tag)

if __name__ == '__main__':
    main()
