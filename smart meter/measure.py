"""measure.py

Measures the length of time the air-conditioner has been on and then calculates energy consumption
"""

from Classes.node import Node
from Classes.client import Client
from meter import Meter


def main():
    pass


# Device seed
device_seed = b"SHORHFAI9XLAGESQKYNDCAUCHHQOZMQPLCHKU9HFSYSUU9ERJBNOGCA9G9BNUAOGTF9LYKNMRSSRBR9DM"

# Device tag, used to post transactions to tangle
device_tag = Tag(b"AIRCON999MEASURE")

# Connect to node and create an api
node = Node()
api = node.create_api(seed=device_seed)

# client object to query and post to tangle
client = Client(api, device_tag)

# Meter object to get meter readings
meter = Meter(client)

if __name__ == '__main__':
    main()
