"""
monitor.py

This script represents a device monitoring data from the sensing devices (sensor.py). It calculates an average
from the last 10 transactions made by the sensing devices, depending on this value it posts a number, either 0, 1 or 2,
to the tangle. If the the average is above 6 it suggests something may be wrong so posts with a 1 or 2, depending on
severity, anything less than 6 is considered normal so a 0 is posted.
"""

from Classes.client import Client
import time
import requests


def main(tags):

    try:
        while True:

            # Code used to query tangle
            transaction_hashes = client.get_transactions_hashes(tags)
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

            # Monitors every 3 minutes
            time.sleep(180)

            # Publishes tag to message stream again for recently connected devices
            client.mqtt.publish_data_stream(tag_string=client.tag_string)

    # Catches any connection errors when collecting data
    except requests.exceptions.ConnectionError:
        print("Connection error...restarting in 1 min")
        time.sleep(60)
        main(tags=tags)


# Create a client object with seed of device
client = Client(device_name="monitor1",
                seed=b'BTPPLUVESQQYZCFYCDZVD9RXHAHTSCIBTMRVQCONZTKQMVLDPGY9HAOTH9NBPFANAEOFLEZIRNTZZVKQY',
                subscribe_topic="sensor/data",
                publish_topic="monitor/data")

if __name__ == '__main__':
    client.mqtt.find_data_streams(number_of_streams=2)
    device_tags = client.convert_tag_strings(client.mqtt.tags_found)
    print("Monitoring sensor...")
    main(tags=device_tags)
