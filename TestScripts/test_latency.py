"""
Tests the latency of varying message sizes through a given number of devices
"""

from Deployment.Client.client import Client
import random
import string
import numpy as np
import matplotlib.pyplot as plt


def propagate_message(tag):

        client = Client(device_type='test_device',
                        device_name='test',
                        encrypt=False,
                        reuse_address=False,
                        iota_node="http://localhost:14700",
                        route_pow=False)

        transactions = client.get_transactions(tags=[tag], count=1)
        data = client.get_transaction_data(transactions[0])
        time = client.post_to_tangle(data=data, address_level=1)
        return client.tag, data, time


def test_latency(number_of_devices, message_size, mwm):

    total_time = 0

    client = Client(device_type='test_device',
                    device_name='test',
                    encrypt=False,
                    reuse_address=False,
                    iota_node="http://localhost:14700",
                    route_pow=False)

    data = ''.join(random.choice(string.ascii_uppercase) for _ in range(message_size))

    t = client.post_to_tangle(data=data, address_level=1, verbose=True, mwm=mwm)

    tag = client.tag

    for _ in range(0, number_of_devices):
        total_time += t
        tag, data, t = propagate_message(tag)
    return total_time


magnitudes = []
for i in range(0, 1100, 250):
    all_times = []
    for j in range(3, 18, 3):
        print(i)
        times = test_latency(number_of_devices=10, message_size=i, mwm=j)
        all_times.append(times)
    magnitudes.append(all_times)

x = [3, 6, 9, 12, 15]
plt.plot(x, magnitudes[0], color="blue", label="0")
plt.plot(x, magnitudes[1], color="red", label="250")
plt.plot(x, magnitudes[2], color="green", label="500")
plt.plot(x, magnitudes[3], color="yellow", label="750")
plt.plot(x, magnitudes[4], color="purple", label="1000")
plt.xticks(np.arange(min(x), max(x) + 1, 3.0))
plt.xlabel('MWM')
plt.ylabel('Time (s)')
plt.legend()
plt.show()
