from Deployment.Client.client import Client


def test_reuse(number_of_transactions, average_over, reuse):

    # Stores results
    results = []

    # Create a client object
    client = Client(device_type='test_device',
                    seed='',
                    device_name='test',
                    reuse_address=reuse,
                    iota_node="http://localhost:14700")

    # Get results
    for i in range(0, average_over):
        times = []
        for j in range(0, number_of_transactions):
            time = client.post_to_tangle(data='')
            times.append(time)
        avg = sum(times) / number_of_transactions
        results.append(avg)
    return results


result_reuse = test_reuse(10, 5, True)
result_no_reuse = test_reuse(10, 5, False)

print(result_reuse)
print(result_no_reuse)
