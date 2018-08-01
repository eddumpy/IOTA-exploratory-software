"""
app.py

Run this script to print out a network summary

"""

from Deployment.Client.brokerclient import BrokerClient
import time
from iota import Tag


def main():

    while True:

        # Used for testing
        de_devices = [['sensor', 'sensor1', Tag(b'KSUOJULM9TWGSKLWQDQS9DUGOPS')],
                   ['sensor', 'sensor2', Tag(b'DSSSXPQCTPYAIUCOU9UJKRNZTPU')]]

        # Use MQTT to find devices
        devices = client.mqtt.find_devices() + de_devices

        devices_data, attributes = client.get_device_data(devices, last_tx=False, last_reading=False, total_txs=False)

        final_devices = client.query_device_data(devices_data)

        table = client.create_table(final_devices, attributes)

        # Print table to console
        print(table)

        # Wait 10 minutes for next network summary
        time.sleep(600)

        # Resets the search
        client.mqtt.reset()


client = BrokerClient(device_type='broker',
                      seed=b'SEDUAWZ9CKBMVEOZ9FCFGFZLCHMIPROBURLEQTYLURFDHOKRCZDNKPNSQTRIBQFQLOAQGIZGYNZNIOOYI',
                      route_pow=False)

if __name__ == '__main__':
    main()
