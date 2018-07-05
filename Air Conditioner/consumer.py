from Classes.node import Node
from iota import Address


# Function found on someone else's code, checks balance of client address.
def check_balance():
    print("Checking balance...")
    gb_result = api.get_balances(address)
    balance = gb_result['balances']
    print(balance)
    return balance[0]


consumer_seed = b"OKTLI9KRLBVAAFVKRSOZRKRLLWROWVNELHREIQVQOISCOUVROGJGZGFB9RGDKDZQOCUEAPCNEPEGBDMEG"

address = [Address(b"HTESEKSVYBQX9XH9IREBNRWWCJQJUMALCGVGOBFZOOYCRSLFQQCXFMZWWQXZKZLOTABJCSNNWANRWJZZZ")]

node = Node()
api = node.create_api(consumer_seed)
check_balance()



