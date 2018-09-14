from Deployment.Client.client import Client
import matplotlib.pyplot as plt


def test_setup(number_of_devices):

    # Variable to store total time
    total_time = 0

    for _ in range(0, number_of_devices):
        # Setting up a client device
        client = Client(device_type='test_device',
                        seed='',
                        device_name='test',
                        iota_node="http://localhost:14700",
                        route_pow=False)

        # Send a zero value transaction to attach address to tangle
        time = client.post_to_tangle(data='')

        # Add found time to total time
        total_time += time
    return total_time


results = []
for i in range(10, 60, 10):
    time_of_setup = test_setup(number_of_devices=i)
    results.append(time_of_setup)

x = [10, 20, 30, 40, 50]
width = 5
plt.bar(x, results, width)
plt.title("Cost of set up")
plt.ylabel("Time (s)")
plt.xlabel("Number of devices")
plt.gca()
plt.show()

