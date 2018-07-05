from Classes.node import Node

"""Client-v4

Script will watch the balance of an IOTA address and then will turn on a light, depending on
much IOTA was sent.
"""


# Seed of the device
device_seed = b"MQRADQDKIZDRBVNRKMVDQHNNAXLNOFA9WK9ISKYOLIUNXMQUZGZBIYVRATBDHTQZBHTAPLG9R9KJCHUXW"

node = Node()
api = node.create_api(seed=device_seed)

result = api.get_new_addresses(count=1, security_level=2)
addresses = result['addresses']
address = addresses[0]

balance = api.get_balances(addresses)
print(balance)
