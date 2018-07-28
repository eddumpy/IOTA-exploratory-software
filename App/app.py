"""
app.py

Run this script to print out a network summary

"""
import datetime

from Deployment.client import Client
from prettytable import PrettyTable
import time


def main():

    while True:

        # Find online devices
        devices = client.mqtt.find_devices(names=['sss'])

        # Creates table
        table = PrettyTable(['Type', 'Name', 'Tag', 'Last Transaction'])

        # Retrieves timestamp of latest transaction
        for device in devices:
            latest_transaction_timestamp = client.get_transactions([device[2]], count=1)[0].timestamp
            t = datetime.datetime.fromtimestamp(latest_transaction_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            device.append(t)
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
                broker=True)

if __name__ == '__main__':
    main()
