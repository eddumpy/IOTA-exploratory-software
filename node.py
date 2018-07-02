from iota import Iota
from iota.adapter.wrappers import RoutingWrapper
import requests


class Node:

    def __init__(self, iota_node='https://nodes.devnet.thetangle.org:443', pow_node='http://localhost:14265'):
        self.iota_node = iota_node  # Public node
        self.pow_node = pow_node  # Local node to perform PoW

    def create_api(self, seed='', route_pow=True) -> Iota:
        if route_pow is True:
            api = \
                Iota(
                    RoutingWrapper(self.iota_node)
                        .add_route('attachToTangle', self.pow_node)
                        .add_route('interruptAttachingToTangle', self.pow_node),
                    seed=seed
                )
        else:
            api = Iota(self.iota_node, seed)

        return api

    @staticmethod
    def test_node(api):
        try:
            status = api.get_node_info()
            print("Successfully connected to IOTA Node!")
            if abs(status['latestMilestoneIndex'] - status['latestSolidSubtangleMilestoneIndex']) > 3:
                print("\rIota node is not synced!")
            else:
                print("\rIota node is synced!")
        except requests.exceptions.ConnectionError:
            print("Connection refused")