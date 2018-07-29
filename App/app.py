"""
app.py

Run this script to print out a network summary

"""

from Deployment.Client.brokerclient import BrokerClient
import time
from iota import Tag


def main():

    while True:

        # Find online devices
        #devices = client.mqtt.find_devices()

        # Used for testing
        devices = [['sensor', 'sensor1', Tag(b'KSUOJULM9TWGSKLWQDQS9DUGOPS')]]

        table = client.create_table(devices, tag=False)

        # Print table to console
        print(table)

        # Wait 10 minutes for next network summary
        time.sleep(600)

        # Resets the search
        client.mqtt.reset()


client = BrokerClient(device_name='broker1',
                      device_type='broker',
                      seed=b'SEDUAWZ9CKBMVEOZ9FCFGFZLCHMIPROBURLEQTYLURFDHOKRCZDNKPNSQTRIBQFQLOAQGIZGYNZNIOOYI',
                      route_pow=False)

if __name__ == '__main__':
    main()
