"""
status.py

Device reads the data posted by monitor.py, and prints a service update about client-v1.
"""

from Deployment.client import Client
from Deployment.user_input import get_user_input
import time


def main(tags):

    while True:

        # Code used to query tangle
        transaction_hashes = client.get_transactions_hashes(tags)
        transactions = client.get_transactions(transaction_hashes, count=5)

        # Gets transaction data from list of transaction objects
        txs_data = [int(client.get_transaction_data(tx)) for tx in transactions]

        # Prints out a message to console based on client-v2 data
        if sum(txs_data) > 3:
            print("Red")
        elif 2 > sum(txs_data) > 1:
            print("Orange")
        else:
            print("Green")

        time.sleep(300)


# Get a device name from the user
device_name, device_list = get_user_input()

# Class used to query tangle data,
client = Client(device_name=device_name,
                seed=b'FDUDNNKTWT9OJXMSXIYX9HUTTLCRJTW99UODHCBHAPQKSEBIOPKNCKNEBQKSWG9QTARTRKJXWDWXCW9FG',
                subscribe_topic="monitor/data",
                known_devices=device_list)

if __name__ == '__main__':
    device_tags = client.find_devices()
    main(device_tags)
