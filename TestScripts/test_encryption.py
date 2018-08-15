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
    for i in range(0, number_of_transactions):
        times = []
        for j in range(0, average_over):
            time = client.post_to_tangle(data='', encrypt=encrypt)
            times.append(time)
        avg = sum(times) / average_over
        results.append(avg)
    return results


final_results_encrypt = test_encryption(50, 10, encrypt=True)
final_results_no_encrypt = test_encryption(50, 10, encrypt=False)
