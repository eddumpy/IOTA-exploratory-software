"""
sensor.py

This python script represents a sensing IoT device. Every minute, the device will store a
random number between 0-9 on to the tangle.
"""

from Deployment.Client.client import Client
import time
import random
import requests
import sys


def main():

    try:
        # Provide status update
        print("Data collection initiated...")

        while True:

            # Generate random number as the data to store in the tangle and convert to Trytestring
            sensor_data = random.randint(0, 100)
            print("Data reading: ", sensor_data)

            # Posts encrypted data to tangle
            client.post_to_tangle(sensor_data, verbose=True)

            # Wait approx 1 minute for next data collection
            client.publish(minutes=1)

    # Catches any connection errors when collecting data
    except requests.exceptions.ConnectionError:
        print("Connection error...restarting data collection in 1 min")
        time.sleep(60)
        main()

    except KeyboardInterrupt:
        print("Ending data stream....")
        sys.exit()


# Create a client object with device seed, use a seed generator to get a seed.
client = Client(device_type='sensor',
                seed=b'GYZHOINRXAPJOIUIPEZATMDDYNQQZITJQTWMFDAUPWWAQNAURLGXQOOVQMAJUICWXIEIWDIBPGUQPBRMY')

# Prints client details to console
print(client)

if __name__ == '__main__':
    main()
