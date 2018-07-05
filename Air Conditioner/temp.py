"""temp.py

Python script is used to monitor temperature.
New temperature readings are posted to the tangle with the device tag.
"""
from Classes.node import Node
from Classes.client import Client
from meter import Meter
from iota import Tag
import time


def main():
    """Monitors temperature, takes a new reading every minute

    """

    # Default starting temperature
    temp = 20

    # Start up message
    print("Temperature sensor initialised, recording temperature... ")

    while True:

        # Check to see if air-conditioner is on
        air_con = meter.get_aircon_state()

        # If the air-conditioner is on the temperature decreases by one, if off, the temperature increases by one
        if air_con is True:
            temp -= 1
            client.post_to_tangle(temp)
            status = "ON"
        else:
            temp += 1
            client.post_to_tangle(temp)
            status = "OFF"

        # Prints out the current temperature and air conditioner status
        print("Current Temperature: ", temp, " Degrees")
        print("Air conditioner is turned ", status)

        # Takes a new temperature reading every minute
        time.sleep(60)


# Device seed
device_seed = b"WGPUZIIOHZSGSG99LKDOV9P9YRJCNZDPZASKUQRPAXOBWTCSDLYHJGDVGOOMKAZXZXMGUWIZLLMHPAKDS"

# Device tag
device_tag = Tag(b"TEMPSENSOR999")

# Connect to node and create an api
node = Node()
api = node.create_api(seed=device_seed)

# client object to query and post to tangle
client = Client(api, device_tag)

# Creates meter object
meter = Meter(client)

if __name__ == '__main__':
    main()
