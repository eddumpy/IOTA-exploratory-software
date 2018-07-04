"""temp.py

Python script is used to monitor temperature.
New temperature readings are posted to the tangle with the device tag.
"""

from node import Node
from client import Client
from iota import Tag
import time


def get_aircon_state():
    """Gets the air-conditioner state by looking on the tangle

    :return: State of the air-conditioner
    """

    # Tag used to query air-conditioner state
    aircon_tag = [Tag(b"AIRCON999")]

    # Get the transaction hashes of previous transactions by the air conditioner
    transaction_hashes = client.get_transactions_hashes(aircon_tag)

    # If no previous transactions, the air-conditioner is off
    if not transaction_hashes:
        is_on = False
    else:
        transaction_trytes = client.get_transaction_trytes(transaction_hashes)
        transactions = client.get_transactions(transaction_trytes)
        state = client.get_latest_transaction_info(transactions)

        if state == "1":
            is_on = True
        else:
            is_on = False
    return is_on


def main(temp):
    """Monitors temperature, takes a new reading every minute

    :param temp: Default temperature value
    """

    while True:

        # Check to see if air-conditioner is on
        air_con = get_aircon_state()

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
node.test_node(api)

# client object to query and post to tangle
client = Client(api, device_tag)

# Default starting temperature
starting_temp = 20

if __name__ == '__main__':
    main(starting_temp)
