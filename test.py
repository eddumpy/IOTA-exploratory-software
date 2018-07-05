from iota import Tag
from Classes.node import Node

device_seed = b"WGPUZIIOHZSGSG99LKDOV9P9YRJCNZDPZASKUQRPAXOBWTCSDLYHJGDVGOOMKAZXZXMGUWIZLLMHPAKDS"

node = Node()
api = node.create_api(seed=device_seed)
node.test_node(api)

# Tag of this device.
monitor_tag = Tag(b'MONITOR')

value = api.get_account_data(10, inclusion_states=False)
print(value)

