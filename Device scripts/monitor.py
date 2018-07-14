"""
monitor.py

This script represents a device monitoring data from the sensing devices (sensor.py). It calculates an average
from the last 10 transactions made by the sensing devices, depending on this value it posts a number, either 0, 1 or 2,
to the tangle. If the the average is above 6 it suggests something may be wrong so posts with a 1 or 2, depending on
severity, anything less than 6 is considered normal so a 0 is posted.
"""

from Deployment.client import Client
from Deployment.user_input import get_user_input
import time
import requests
import sys


def main(tags):

    try:

        while True:

            # Code used to query tangle
            transaction_hashes = client.get_transactions_hashes(tags)
            transactions = client.get_transactions(transaction_hashes, count=len(tags) * 10)

            # Gets transaction data from list of transaction objects
            txs_data = [int(client.get_transaction_data(tx)) for tx in transactions]

            # Calculates the mean of found transactions
            data_average = sum(txs_data) / float(len(txs_data))
            print("Average: ", data_average)

            # Posts average of data
            client.post_to_tangle(data_average)

            # Wait for next data collection
            client.wait_and_publish()

    # Catches any connection errors when collecting data and restarts
    except requests.exceptions.ConnectionError:
        print("Connection error...restarting in 1 min")
        time.sleep(60)
        main(tags=tags)

    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()


device_name, device_list, streams = get_user_input()

# Create a client object with seed of device
client = Client(device_name=device_name,
                device_type='monitor',
                read_from_device_type='sensor',
                seed=b'BTPPLUVESQQYZCFYCDZVD9RXHAHTSCIBTMRVQCONZTKQMVLDPGY9HAOTH9NBPFANAEOFLEZIRNTZZVKQY',
                known_devices=device_list,
                number_of_streams=streams)

if __name__ == '__main__':
    device_tags = client.search_for_devices()
    main(device_tags)
