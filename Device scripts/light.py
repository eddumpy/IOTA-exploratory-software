"""
state.py

Device reads the data posted by monitor.py, and prints a service update about client-v1.
"""

from Deployment.client import Client
from Deployment.user_input import get_user_input
import requests
import time
import sys


def main(tags):

    while True:

        try:
            # Code used to query tangle
            transaction_hashes = client.get_transactions_hashes(tags)
            transactions = client.get_transactions(transaction_hashes, count=1)

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
            client.wait_and_publish(minutes=1)

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
                read_from_device_type='state',
                seed=b'UKFZVYF99PJTYMOXFIBPQVLB9EGEC9VWVOOZTPAOWVZSURREHLKORIGFVBMQYJGGNC9GBNHZKDIDPBXAS',
                known_devices=device_list,
                number_of_streams=streams)

if __name__ == '__main__':
    device_tags = client.search_for_devices()
    main(device_tags)
