"""
light.py

Depending on the state value posted by state.py, this script will print out either, 'Red', 'Orange' and 'Green' to
imitate a light

"""

from Deployment.Client.client import Client
from Deployment.user_input import get_user_input
import requests
import time
import sys


def main(tags):

    while True:

        try:
            # Code used to query tangle
            transactions = client.get_transactions(tags, count=1)

            # Gets transaction data from list of transaction objects
            txs_data = [float(client.get_transaction_data(tx)) for tx in transactions]

            if txs_data[0] is 2:
                light_state = "Red"
            elif txs_data[0] is 1:
                light_state = "Orange"
            else:
                light_state = "Green"

            print(light_state)

            # Post state of device to tangle
            client.post_to_tangle(light_state)

            # Wait period
            client.publish(minutes=1)

        # Catches any connection errors when collecting data and restarts
        except requests.exceptions.ConnectionError:
            print("Connection error...restarting in 1 min")
            time.sleep(60)
            main(tags=tags)

        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()


# Get a device name from the user
device_name, device_list, streams = get_user_input()

# Class used to query tangle data,
client = Client(device_name=device_name,
                device_type='light',
                seed=b'UKFZVYF99PJTYMOXFIBPQVLB9EGEC9VWVOOZTPAOWVZSURREHLKORIGFVBMQYJGGNC9GBNHZKDIDPBXAS')

# Prints client details to console
print(client)

if __name__ == '__main__':
    device_tags = client.mqtt.find_device_tags(devices=device_list, num_of_streams=streams, read_from='state')
    main(device_tags)
