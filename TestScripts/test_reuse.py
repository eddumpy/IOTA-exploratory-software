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


#result_reuse = test_reuse(10, 5, True)
#result_no_reuse = test_reuse(10, 5, False)

result_reuse = [20.431574487686156, 28.76900773048401, 16.073536586761474, 17.513502645492554, 38.35531964302063, 25.098815536499025, 18.038471460342407, 16.520094776153563, 29.765741539001464, 19.796921014785767]
result_no_reuse = [24.472752141952515, 31.45073547363281, 32.13733620643616, 27.993191242218018, 43.77975959777832, 36.96368618011475, 42.38713183403015, 46.8346243383656, 35.16887526512146, 48.273162603378296]

x = np.arange(0, len(result_reuse))
plt.plot(x, result_reuse, color="blue", label="Reuse")
plt.plot(x, result_no_reuse, color="red", label="No reuse")
plt.title("Reusing addresses")
plt.xlabel('Transaction number')
plt.ylabel('Time (s)')
plt.legend()
plt.show()
