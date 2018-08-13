from Deployment.Client.client import Client


def test_encryption(number_of_transactions, average_over, encrypt):

    # Stores results
    results = []

    # Create a client object
    client = Client(device_type='test_device',
                    seed='',
                    device_name='test',
                    reuse_address=False,
                    iota_node="http://localhost:14700")

    # Get results
    for i in range(0, average_over):
        times = []
        for j in range(0, number_of_transactions):
            time = client.post_to_tangle(data='', encrypt=encrypt)
            times.append(time)
        avg = sum(times) / number_of_transactions
        results.append(avg)
    return results