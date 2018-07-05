"""status.py

Device reads the data posted by client-v2, and prints a service update about client-v1.
"""

from iota import Tag
from Classes.node import Node
from Classes.client import Client


def main():
    # Code used to query tangle
    transaction_hashes = client.get_transactions_hashes(monitor_tag)
    transactions = client.get_transactions(transaction_hashes)

    # Gets transaction data from list of transaction objects
    txs_data = []
    for tx in transactions:
        data = client.get_transaction_info(tx)
        txs_data.append(data)

    # Sorts data, reads the last 5 transactions posted by client-v2
    sorted_data = client.sort_data(txs_data, count=5)

    # Gets the data posted by client-v2
    status_list = []
    for i in range(0, len(sorted_data)):
        info = sorted_data[i]
        status_list.append(float(info[1]))

    # Prints out a message to console based on client-v2 data
    if sum(status_list) > 3:
        print("URGENT, Device needs servicing ASAP...")
    elif 2 > sum(status_list) > 1:
        print("Device needs servicing, may not be working properly...")
    else:
        print("Device is working as normal.")


# Connect to node and create api instance
node = Node()
api = node.create_api()

# Tag of this device.
monitor_tag = [Tag(b'MONITOR')]

# Class used to query tangle data,
client = Client(api, monitor_tag)

if __name__ == '__main__':
    main()
