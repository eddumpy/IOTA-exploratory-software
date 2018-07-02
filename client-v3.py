from iota import Tag
from node import Node
from client import Client


def main():
    transaction_hashes = client.get_transactions_hashes(monitor_tag)
    transaction_trytes = client.get_transaction_trytes(transaction_hashes)
    transactions = client.get_transactions(transaction_trytes)

    txs_data = []
    for tx in transactions:
        data = client.get_transaction_info(tx)
        txs_data.append(data)

    sorted_data = client.sort_data(txs_data)

    status_list = []
    for i in range(0, len(sorted_data)):
        info = sorted_data[i]
        status_list.append(float(info[1]))

    if sum(status_list) > 5:
        print("Device needs service...")
    elif 5 > sum(status_list) > 3:
        print("Device may not be working...")
    else:
        print("Device working as normal.")

# Connect to node and create api instance
node = Node()
api = node.create_api()
node.test_node(api)

# Tag of this device.
monitor_tag = [Tag(b'MONITOR')]

# Class used to query tangle data,
client = Client(api, monitor_tag)

if __name__ == '__main__':
    main()