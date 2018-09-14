from Deployment.Client.client import Client
import matplotlib.pyplot as plt
import numpy as np


def test_address_level(number_of_transactions):

    # Stores results
    results = []

    # Create a client object
    client = Client(device_type='test_device',
                    seed='',
                    device_name='test',
                    reuse_address=False,
                    iota_node="http://localhost:14700",
                    route_pow=False)

    # Get results
    for j in range(1, 4):
        times = []
        for tx in range(0, number_of_transactions):
            time = client.post_to_tangle(data='', address_level=j)
            times.append(time)
        avg = sum(times) / number_of_transactions
        results.append(avg)
    return results


final_results = []
for i in range(10, 60, 10):
    scores = test_address_level(i)
    final_results.append(scores)
    
levels = []
for i in range(0, 3):
    level = []
    for results in final_results:
        level.append(results[i])
    levels.append(level)
print(levels)

n = 5
fig, ax = plt.subplots()

ind = np.arange(n)
width = 0.2

p1 = ax.bar(ind, levels[0], width, color='r', bottom=0)
p2 = ax.bar(ind + width, levels[1], width, color='y', bottom=0)
p3 = ax.bar(ind + width*2, levels[2], width, color='b', bottom=0)

ax.set_xticks(ind + width)
ax.set_xticklabels(('10', '20', '30', '40', '50'))

ax.set_ylabel('Time (s)')
ax.set_xlabel('Number of Transactions')

ax.legend((p1[0], p2[0], p3[0]), ('1', '2', '3'))
ax.autoscale_view()
plt.show()
