"""
monitor.py

This script represents a device monitoring data from the sensing devices (sensor.py). It calculates the mean from
the data found in the last 10 transactions made by the sensing device(s). It then stores this data to the tangle.
"""

from Deployment.Client.client import Client
from Deployment.user_input import get_user_input
import time
import requests
import sys


def main(tags):

    try:

        while True:

            # Code used to query tangle
            transactions = client.get_transactions(tags, count=len(tags) * 10)
            txs_data = [int(client.get_transaction_data(tx)) for tx in transactions]

            print("Decrypted data", txs_data[0])

            # Calculates the mean of found transactions
            data_average = sum(txs_data) / float(len(txs_data))

            print("Average: ", data_average)

            # Posts average of data
            client.post_to_tangle(data_average, verbose=True)

            # Wait for next data collection
            client.publish(minutes=1)

    # Catches any connection errors when collecting data and restarts
    except requests.exceptions.ConnectionError:
        print("Connection error...restarting in 1 min")
        time.sleep(60)
        main(tags=tags)

    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()


device_list, streams = get_user_input()

# Create a client object with seed of device
client = Client(device_type='monitor',
                seed=b'BTPPLUVESQQYZCFYCDZVD9RXHAHTSCIBTMRVQCONZTKQMVLDPGY9HAOTH9NBPFANAEOFLEZIRNTZZVKQY')

# Prints client details to console
print(client)

if __name__ == '__main__':
    device_tags = client.mqtt.find_device_tags(devices=device_list, num_of_streams=streams, read_from='sensor')
    main(device_tags)
