"""
Test to see the difference in time it takes to send transactions with unattached and
already attached addresses
"""

from Deployment.Client.client import Client
import matplotlib.pyplot as plt
import numpy as np


def test_reuse(number_of_transactions, average_over, reuse):

    # Stores results
    results = []

    # Create a client object
    client = Client(device_type='test_device',
                    seed='',
                    device_name='test',
                    reuse_address=reuse,
                    iota_node="http://localhost:14700",
                    route_pow=False)

    # Get results
    for i in range(0, number_of_transactions):
        times = []
        for j in range(0, average_over):
            time = client.post_to_tangle(data='')
            times.append(time)
        avg = sum(times) / average_over
        results.append(avg)
    return results


result_reuse = test_reuse(10, 5, True)
result_no_reuse = test_reuse(10, 5, False)

x = np.arange(0, len(result_reuse))
plt.plot(x, result_reuse, color="blue", label="Reuse")
plt.plot(x, result_no_reuse, color="red", label="No reuse")
plt.title("Reusing addresses")
plt.xlabel('Transaction number')
plt.ylabel('Time (s)')
plt.legend()
plt.show()
