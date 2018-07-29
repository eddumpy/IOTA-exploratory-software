"""
app.py

Run this script to print out a network summary

"""

from Deployment.client import Client
from prettytable import PrettyTable
import time


def main():

    while True:

        # Find online devices
        devices = client.mqtt.find_devices()

        # Creates table
        table = PrettyTable(['Type', 'Name', 'Tag', 'Status', 'Last Transaction', 'Last Reading', 'Total transactions'])

        # Retrieves timestamp of latest transaction
        for device in devices:
            device_tag = device[2]

            # Add status of device
            status = client.check_device_status(device_tag)

            # Number of transactions
            transactions = client.get_transactions([device_tag], most_recent=False)
            num_of_txs = len(transactions)

            # Latest Transaction
            latest_transaction = transactions[-1:]
            time_of_transaction = client.get_timestamps(latest_transaction)[0]
            last_transaction_data = client.get_transaction_data(latest_transaction[0])

            # Add to device details
            device.append(status)
            device.append(time_of_transaction)
            device.append(last_transaction_data)
            device.append(num_of_txs)

            # Add device to table
            table.add_row(device)

        # Print table to console
        print(table)

        # Wait 10 minutes for next network summary
        time.sleep(600)

        # Resets the search
        client.mqtt.reset()


client = Client(device_name='broker1',
                device_type='broker',
                seed=b'SEDUAWZ9CKBMVEOZ9FCFGFZLCHMIPROBURLEQTYLURFDHOKRCZDNKPNSQTRIBQFQLOAQGIZGYNZNIOOYI',
                route_pow=False)

if __name__ == '__main__':
    main()
