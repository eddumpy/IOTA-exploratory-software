from Deployment.Client.client import Client
import matplotlib.pyplot as plt
import numpy as np


def test_mwm(number_of_transactions, mwm):

    # Create a client object
    client = Client(device_type='test_device',
                    seed='',
                    device_name='test',
                    reuse_address=False,
                    iota_node="http://localhost:14700",
                    route_pow=False)

    results = []
    for _ in range(0, number_of_transactions):
        tx_time = client.post_to_tangle(data='', mwm=mwm)
        results.append(tx_time)
    average = sum(results) / number_of_transactions
    return average


all_times = []
for i in range(3, 21, 3):
    time = test_mwm(number_of_transactions=10, mwm=i)
    all_times.append(time)

n = len(all_times)
fig, ax = plt.subplots()

ind = np.arange(n)
width = 0.5

p1 = ax.bar(ind, all_times, width, color='r', bottom=0)

ax.set_xticks(ind)
ax.set_xticklabels(('3', '6', '9', '12', '15', '18'))

ax.set_ylabel('Time (s)')
ax.set_xlabel('Minimum weight magnitude')

rects = ax.patches

labels = [str(int(time)) for time in all_times]

for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label,
            ha='center', va='bottom')

ax.autoscale_view()
plt.show()



