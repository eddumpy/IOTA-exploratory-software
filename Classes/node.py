import urllib3
from iota import Iota
from iota.adapter.wrappers import RoutingWrapper
import requests

"""Node class:

Used to create an API instance to interact with the tangle
Default URIs are provided, but can be changed if needed.

Current set up connects to a public Iota devnet node and 
uses a local running node with no neighbours to provide the
proof of work.
"""


class Node:

    def __init__(self, iota_node='https://nodes.devnet.thetangle.org:443', pow_node='http://localhost:14265'):
        self.iota_node = iota_node  # Public node
        self.pow_node = pow_node  # Local node to perform PoW

        self.api = None  # Once the create api method is called, an API will be saved so it can be tested immediately

    def create_api(self, seed='', route_pow=True) -> Iota:
        """Creates an Iota object to interact with the tangle

        :param seed: The seed of the device, currently uses a random seed.
        :param route_pow: Boolean to provide whether you want to provide PoW assistance from a local node.
        :return: An Iota object
        """
        try:

            if route_pow is True:
                self.api = \
                    Iota(
                        RoutingWrapper(self.iota_node)
                            .add_route('attachToTangle', self.pow_node)
                            .add_route('interruptAttachingToTangle', self.pow_node),
                        seed=seed
                    )
            else:
                self.api = Iota(self.iota_node, seed)
                print("Made it before test")
                self.test_node()

        except ConnectionRefusedError as e:
            print(e)
            print("Ensure all nodes are working correctly before connecting")
        except urllib3.exceptions.NewConnectionError as e:
            print(e)
            print("Ensure all nodes are working correctly before connecting")
        except urllib3.exceptions.MaxRetryError as e:
            print(e)
            print("Ensure all nodes are working correctly before connecting")
        except requests.exceptions.ConnectionError as e:
            print(e)
            print("Ensure all nodes are working correctly before connecting")

        return self.api

    def test_node(self):
        """Tests the connection to the node and if it is synced
        """
        try:
            status = self.api.get_node_info()
            print("Successfully connected to IOTA Node!")
            if abs(status['latestMilestoneIndex'] - status['latestSolidSubtangleMilestoneIndex']) > 3:
                print("\rIota node is not synced!")
            else:
                print("\rIota node is synced!")
        except requests.exceptions.ConnectionError:
            print("Connection refused")
