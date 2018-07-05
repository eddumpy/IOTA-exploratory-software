"""aircon.py

Python script is used to post the state of a virtual air-conditioner to the tangle. The state changes depending on the
data posted by the temperature sensor in temp.py.
"""

from Classes.node import Node
from Classes.client import Client
from iota import Tag
from meter import Meter


def main(state):

    """Constantly monitors any changes to temperature, so air conditioner can be turned on/off accordingly.

    :param state: Default state of air conditioner (is turned off to start)
    """

    while True:

        # Gets the current temperature
        temperature = meter.get_temperature()


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

meter = Meter(client)

current_state = 1
if __name__ == '__main__':
    main(current_state)
