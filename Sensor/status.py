"""
status.py

Device reads the data posted by monitor.py, and prints a service update about client-v1.
"""

from Classes.client import Client


def main(tags):
    # Code used to query tangle
    transaction_hashes = client.get_transactions_hashes(tags)
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


# Class used to query tangle data,
client = Client(device_name="status1",
                seed=b'FDUDNNKTWT9OJXMSXIYX9HUTTLCRJTW99UODHCBHAPQKSEBIOPKNCKNEBQKSWG9QTARTRKJXWDWXCW9FG',
                subscribe_topic="monitor/data")

if __name__ == '__main__':
    client.mqtt.find_data_streams()
    device_tags = client.convert_tag_strings(client.mqtt.tags_found)
    main(device_tags)
