from Deployment.Client.client import Client
import time
import random
import string


def utf8len(s):
    return len(s.encode('utf-8'))


def propagate_message(tag):

        client = Client(device_type='test_device',
                        device_name='test',
                        reuse_address=False,
                        iota_node="http://localhost:14700",
                        route_pow=False)

        transactions = client.get_transactions(tags=[tag], count=1)
        data = client.get_transaction_data(transactions[0])
        client.post_to_tangle(data=data, address_level=1)
        return client.tag, data


def test_latency(number_of_devices, message_size):

    client = Client(device_type='test_device',
                    device_name='test',
                    reuse_address=False,
                    iota_node="http://localhost:14700",
                    route_pow=False)

    data = ''.join(random.choice(string.ascii_uppercase + '9') for _ in range(message_size))
    print(data)
    start = time.time()

    client.post_to_tangle(data=data, address_level=1)

    tag = client.tag

    for i in range(0, number_of_devices):
        tag, data = propagate_message(tag)
        print(data)

    end = time.time()
    elapsed_time = end - start
    return elapsed_time


times = test_latency(0, 2000)
print(times)
