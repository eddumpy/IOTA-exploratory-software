"""
state.py

Device reads the data posted by monitor.py, and gives a state value
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
            transactions = client.get_transactions(tags, count=(len(tags) * 5))

            # Gets transaction data from list of transaction objects
            txs_data = [float(client.get_transaction_data(tx)) for tx in transactions]

            # All transaction data summed
            total = sum(txs_data)

            # Performs a check on the summed data and gives device a state
            if total >= 600:
                system_state = 2
            elif 600 > total > 500:
                system_state = 1
            else:
                system_state = 0

            print("State: ", system_state)

            # Post state of device to tangle
            client.post_to_tangle(system_state, verbose=True)

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
device_list, streams = get_user_input()

# Class used to query tangle data,
client = Client(device_type='state',
                seed=b'FDUDNNKTWT9OJXMSXIYX9HUTTLCRJTW99UODHCBHAPQKSEBIOPKNCKNEBQKSWG9QTARTRKJXWDWXCW9FG')

# Prints client details to console
print(client)

if __name__ == '__main__':
    device_tags = client.mqtt.find_device_tags(devices=device_list, num_of_streams=streams, read_from='monitor')
    main(device_tags)
