from Deployment.Client.client import Client
import matplotlib.pyplot as plt
import time
import numpy as np


def transaction_test(number_of_txs, wait):

    # List to store times
    times = []

    for _ in range(0, number_of_txs):

        client = Client(device_type='test_device',
                        seed='',
                        device_name='test',
                        iota_node="http://localhost:14700",
                        route_pow=False)

        # Send a zero value transaction to attach address to tangle
        t = client.post_to_tangle(data='')

        # Add found time to total time
        times.append(t)

        # Wait time
        time.sleep(wait)

    return times


results = []
for i in range(0, 90, 30):
    result = transaction_test(number_of_txs=50, wait=i)
    results.append(result)

x = np.arange(1, len(results[0]) + 1)
plt.plot(x, results[0], color="blue", label="No wait time")
plt.plot(x, results[1], color="red", label="30 seconds")
plt.plot(x, results[2], color="green", label="60 seconds")
plt.xticks(np.arange(min(x) + 4, max(x) + 5, 5))
plt.xlabel('Transaction number')
plt.ylabel('Time (s)')
plt.legend()
plt.show()
