from Deployment.Client.client import Client


def test_address_level():

    results = []

    client = Client(device_type='test_device',
                    seed='',
                    device_name='test',
                    reuse_address=False,
                    iota_node="http://localhost:14700",
                    route_pow=False)

    for j in range(1, 4):
        times = []
        for i in range(0, 20):
            # Send a zero value transaction to attach address to tangle with address level
            time = client.post_to_tangle(data='', address_level=j)
            times.append(time)
        avg = sum(times) / 50
        results.append(avg)
    return results


scores = test_address_level()
print(scores)
