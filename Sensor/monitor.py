"""monitor.py

This script represents a device monitoring data from the sensing device (client-v1). It calculates an average
from the last 10 transactions made by the sensing device, depending on this value it posts a number, either 0, 1 or 2,
to the tangle. If the the average is above 6 it suggests something may be wrong so posts with a 1 or 2, depending on
severity, anything less than 6 is considered normal so a 0 is posted.
"""

from iota import Tag
from Classes.node import Node
from Classes.client import Client
import time
import requests


def main():

    print("Device monitoring sensor...")

    try:
        while True:

            # Code used to query tangle
            transaction_hashes = client.get_transactions_hashes([sensor_tag])
            transactions = client.get_transactions(transaction_hashes)

            # Gets transaction data from list of transaction objects
            txs_data = [client.get_transaction_info(tx) for tx in transactions]

            # Sorts data, reads the last 10 transactions posted by client-v1
            sorted_data = client.sort_data(txs_data)

            monitor_data = []
            for d in sorted_data:
                monitor_data.append(int(d[1]))

            # Calculates an average from last 10 transactions from client-v1
            data_average = sum(monitor_data) / float(len(monitor_data))
            print("Device value: ", data_average)

            # If the data average is above a certain threshold, a number between 0-2 will be posted
            if data_average > 7:
                device_status = 2
                client.post_to_tangle(device_status)
            elif 7 > data_average > 6:
                device_status = 1
                client.post_to_tangle(device_status)
            else:
                device_status = 0
                client.post_to_tangle(device_status)

            # Monitors every 5 minutes
            time.sleep(300)

    # Catches any connection errors when collecting data
    except requests.exceptions.ConnectionError:
        print("Connection error...restarting in 1 min")
        time.sleep(60)
        main()


# Connect to node and create api instance
node = Node()
api = node.create_api()

# Tag of this device.
monitor_tag = Tag(b'MONITOR')

# Tag of the device that this device is monitoring i.e. the sensor
sensor_tag = Tag(b'SENSOR')

# Client library
client = Client(api, monitor_tag)

if __name__ == '__main__':
    main()
