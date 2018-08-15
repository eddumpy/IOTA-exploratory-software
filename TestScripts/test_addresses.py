from Deployment.Client.client import Client


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

print(final_results)

