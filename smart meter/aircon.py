"""aircon.py

Python script is used to post the state of a virtual air-conditioner to the tangle. The state changes depending on the
data posted by the temperature sensor in temp.py.
"""

from node import Node
from client import Client
from iota import Tag


def get_temperature():
    """Gets the temperature from the sensor.

    :return: Returns the latest temperature reading by the temperature sensor.
    """

    # Uses the temperature tag to find data posted by the temperature sensor
    temp_tag = [Tag(b"TEMPSENSOR999")]

    # Gets the transaction hashes from the temperature tag
    transaction_hashes = client.get_transactions_hashes(temp_tag)

    # If no transaction hashes are found, a default temperature of 20 is assumed, otherwise the temperature is
    # the reading from the tangle
    if not transaction_hashes:
        latest_temperature_reading = 20  # default temperature
    else:
        transaction_trytes = client.get_transaction_trytes(transaction_hashes)
        transactions = client.get_transactions(transaction_trytes)
        latest_temperature_reading = client.get_latest_transaction_info(transactions)

    print("latest Temperature reading: " + latest_temperature_reading + " Degrees")
    return int(latest_temperature_reading)


def main(state):

    """Constantly monitors any changes to temperature, so air conditioner can be turned on/off accordingly.

    :param state: Default state of air conditioner (is turned off to start)
    """

    while True:

        # Gets the current temperature
        temperature = get_temperature()

        # If temperature is 30 or above the air conditioner needs to be turned on,
        # it turns off when the temperature reaches 20, any change in state is
        # stored on the tangle
        if temperature >= 30:
            if state == 1:
                pass
            else:
                state = 1
                client.post_to_tangle(state)
        elif temperature <= 20:
            if state == 0:
                pass
            else:
                state = 0
                client.post_to_tangle(state)


# Device seed
device_seed = b"EPDTQBXLCSCXAADFDUXRSVSBZXRHUVJLDIDRKKHGTUKOACXAESDD9TYVJJUALPZOKJSWLPPHPWDDNTKSL"

# Device tag, used to post transactions to tangle
device_tag = Tag(b"AIRCON999")

# Connect to node and create an api
node = Node()
api = node.create_api(seed=device_seed)

# client object to query and post to tangle
client = Client(api, device_tag)

current_state = 0
if __name__ == '__main__':
    main(current_state)
