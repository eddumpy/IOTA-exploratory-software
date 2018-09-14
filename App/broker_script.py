"""
broker_script.py

Run this script to print out a network summary

"""

from Deployment.Client.brokerclient import BrokerClient
import time


def main():

    while True:

        # Message to console to indicate its working
        print("Gathering network state...")

        # Use MQTT to find devices
        devices = client.mqtt.find_devices()

        # Get device data
        devices_data, attributes = client.get_device_data(devices)
        table = client.create_table(devices_data, attributes)

        # Print table to console
        print(table)

        # Wait 10 minutes for next network summary
        time.sleep(600)

        # Uncomment if you want to reset search after each wait
        client.mqtt.reset()


client = BrokerClient(device_type='broker', device_name='broker', route_pow=False)
print(client)

if __name__ == '__main__':
    main()
