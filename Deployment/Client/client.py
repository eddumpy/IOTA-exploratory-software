"""
client.py

Contains the Client class, which is used as the core component for deployment. All deployment settings can be
passed through when creating a Client object.
"""

from iota import Transaction, ProposedTransaction, TryteString, Tag
from Deployment.node import Node
from Deployment.MQTT.mqtt_device import MqttDevice
from Deployment.crypto import Crypto

import iota
import time
import random
import string


class Client:

    def __init__(self, device_type, network_name="network", seed='', device_name='', encrypt=True, reuse_address=True,
                 mqtt_broker="localhost", route_pow=True, iota_node='https://nodes.devnet.thetangle.org:443',
                 pow_node='http://localhost:14265'):

        # IOTA api, created through the Node class
        self.api = Node(seed, iota_node, route_pow, pow_node).api

        # Name of network
        self.network_name = network_name

        # MQTT client
        self.mqtt = MqttDevice(network_name=self.network_name, broker=mqtt_broker)

        # Device type
        self.device_type = device_type

        # Name of device
        if device_name == '':
            self.device_name = self.create_name(check_network=False)
        elif device_name == 'broker':
            self.device_name = device_name
        else:
            self.device_name = device_name

        # Creates a random Tag to classify current data stream, as a string and as an IOTA tag
        self.tag_string = ''.join(random.choice(string.ascii_uppercase + '9') for _ in range(27))
        self.tag = Tag(self.tag_string)

        # Stores device details in a list, used for MQTT publishing
        self.device_details = [self.network_name,
                               self.device_type,
                               self.device_name,
                               self.tag_string]

        # Device address info
        self.reuse_address = reuse_address
        self.address = ''

        # Class used to encrypt and decrypt data
        self.crypto = Crypto()
        self.encrypt = encrypt

    def __str__(self):
        return "Network name: " + self.network_name + "\nDevice type: " + self.device_type \
               + "\nDevice name: " + self.device_name + "\nTag: " + self.tag_string

    def create_name(self, check_network=False):
        """Creates a name for the device

        :param: check networks for duplicate names if True
        :return: name of device
        """

        name = input("Please provide a name for the device: ")

        if name == '':
            name = 'unknown ' + self.device_type

        if check_network:
            names_in_network = self.mqtt.find_messages(topic=self.network_name + '/' + self.device_type + '/')
            if name in names_in_network:
                print("Name already used, please provide a different name.")
                name = self.create_name()
        return name

    def generate_address(self, level):
        """Gets a new unused address when called

        :param: Address level
        :return: Newly generated unused address
        """
        try:
            # Finds the next unused address
            # print("Generating address...")
            addresses = self.api.get_new_addresses(count=None, security_level=level)['addresses']
            print("Found an address: ", addresses[0])
            return addresses[0]
        except iota.BadApiResponse:
            print("Address generation error...")
            return None

    def post_to_tangle(self, data, mwm=14, address_level=1, verbose=False):
        """Posts data to the tangle to a randomly generated address

        :param data: Data to be stored on the tangle
        :param mwm: minimum weight magnitude for iota node, check default mwm of network
        :param address_level: Security level of address, 1-3
        :param verbose: Prints out the transaction process if True
        :return elapsed time: Time of the transaction
        """

        # Encrypt data before being posted to tangle
        if self.encrypt:
            data = self.crypto.encrypt(data)
            tryte_string = TryteString.from_bytes(data)
        else:
            tryte_string = TryteString.from_string(str(data))

        # Tracks how long the transaction takes
        start = time.time()

        # Gets an appropriate address for sending transaction
        if self.reuse_address:
            if self.address is '':
                # Generates a new unused address
                self.address = self.generate_address(address_level)
        else:
            self.address = self.generate_address(address_level)

        # Checks address to ensure there was no problem
        if self.address is None:
            self.post_to_tangle(data, mwm, address_level, verbose)

        if verbose:
            print("Transaction Initialised...")
            print("Sending to: ", self.address)

        try:
            # Posts data to the tangle
            self.api.send_transfer(
                depth=3,
                transfers=[
                    ProposedTransaction(
                        address=self.address,
                        value=0,
                        tag=self.tag,
                        message=tryte_string,
                    ),
                ],
                min_weight_magnitude=mwm,
            )

            # Time of transaction
            end = time.time()
            elapsed_time = end - start

            if verbose:
                print("Transaction complete \nElapsed time: ", elapsed_time, " seconds.")

            return elapsed_time

        except iota.BadApiResponse:
            print("Transaction failed, retrying...")
            self.post_to_tangle(data, mwm, address_level, verbose)

    def get_transactions(self, tags, most_recent=True, count=10):
        """Creates Transaction objects from the transaction trytes

        :param tags: List of tags
        :param most_recent: Whether you want returned the most recent transactions
        :param count: Specifies how many transactions you want, 'most_recent' must be true, default is 10
        :return: List of Transaction objects
        """

        # Get transaction hashes from tags
        transactions_hashes = self.api.find_transactions(tags=tags)['hashes']

        # Checks list of transaction hashes is not empty
        if not transactions_hashes:
            print("No Transactions found, waiting for transactions...")
            time.sleep(60)
            self.get_transactions(tags)
        else:

            # The hashes are used to get the raw transaction trytes, which can then be converted to
            # Transaction objects.
            result = self.api.get_trytes(transactions_hashes)
            transaction_trytes = result['trytes']

            # Stores the Transaction objects in a list
            transactions = [Transaction.from_tryte_string(tryte) for tryte in transaction_trytes]

            # Sorts the transactions into order
            ordered_transactions = self.sort_data(transactions, most_recent, count)

            return ordered_transactions

    def get_transaction_data(self, transaction):
        """Gets the SignatureMessageFragment of a transaction

        :param transaction: Transaction object
        :return: Transaction data inside the transaction
        """

        # Get timestamp and message of Transaction
        message = transaction.signature_message_fragment.decode()

        # Decrypt data
        if self.encrypt:
            message = self.crypto.decrypt(message)

        return message

    def publish(self, minutes):
        for i in range(0, (30 * minutes)):
            self.mqtt.publish_device(self.device_details)

    @staticmethod
    def sort_data(transactions, most_recent, count):
        """Sorts data by the oldest to the newest transactions

        :param transactions: List of transactions
        :param most_recent: Boolean, True if you want the most recent transactions
        :param count: If most recent is True, value of count returns that many transactions.
        :return: Returns ordered list of transactions
        """

        # Stores a list of timestamps and transaction objects in tuples
        timestamps = [(tx.timestamp, tx) for tx in transactions]

        # Sort transactions by timestamps
        timestamps.sort(key=lambda tup: tup[0])

        # List of ordered transactions
        ordered_transactions = [tx for (_, tx) in timestamps]

        # Return the most recent transactions or all transactions
        if most_recent is True:
            return ordered_transactions[-count:]
        else:
            return ordered_transactions
