"""
client.py

Contains the Client class, which is used as the core component for deployment. All deployment settings can be
passed through when creating a Client object, enabling flexibility.

Uses MQTT to communicate with other devices

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

    def __init__(self,
                 # Device details
                 device_type,  # Device type -> String
                 seed='',  # IOTA Seed -> String
                 device_name='',
                 reuse_address=True,  # If you want to reuse addresses -> Bool

                 #  MQTT configuration
                 mqtt_broker="localhost",  # broker for MQTT communication -> String

                 # Iota node configuration
                 route_pow=True,  # If you wish to route the PoW to a node -> Bool
                 iota_node='https://nodes.devnet.thetangle.org:443',  # URI of IOTA node -> String
                 pow_node='http://localhost:14265'):  # Uri of PoW node -> String

        # IOTA api, created through the Node class
        self.api = Node(seed, iota_node, route_pow, pow_node).api

        self.network_name = 'network'  # Name of network

        # MQTT client
        self.mqtt = MqttDevice(network_name=self.network_name, broker=mqtt_broker)

        self.device_type = device_type  # Device type

        if device_name == '':
            self.device_name = self.create_name(check_network=False)  # Name of device
        elif device_name == 'broker':
            self.device_name = device_name
        else:
            self.device_name = device_name

        # Creates a random Tag to classify current data stream
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

    def __str__(self):
        return "Network name: " + self.network_name + "\nDevice type: " + self.device_type \
               + "\nDevice name: " + self.device_name + "\nTag: " + self.tag_string

    def create_name(self, check_network=False):
        """Creates a name for the device

        :return: name of device
        """
        name = input("Please provide a name for the device: ")

        if check_network:
            names_in_network = self.mqtt.find_messages(topic=self.network_name + '/' + self.device_type + '/')
            if name in names_in_network:
                print("Name already used, please provide a different name.")
                self.create_name()
        return name

    def generate_address(self, level):
        """Gets a new unused address for each transaction, with security level 2

        :return: Address of device
        """
        try:
            # Finds the next unused address
            print("Generating address...")
            addresses = self.api.get_new_addresses(count=None, security_level=level)['addresses']
            print("Found an address: ", addresses[0])
            return addresses[0]
        except iota.BadApiResponse:
            print("Address generation error...")
            return None

    def post_to_tangle(self, data, address_level=1, encrypt=True, verbose=False):
        """Posts data to the tangle to a randomly generated address

        :param data: Data to be stored on the tangle
        :param address_level: Security level of address, 1-3
        :param encrypt: Option to encrypt Encrypt data
        :param verbose: Prints out the transaction process if True
        :return elapsed time: Time of the transaction
        """

        # Encrypt data before being posted to tangle
        if encrypt:
            data = self.crypto.encrypt(data)
            tryte_string = TryteString.from_bytes(data)
        else:
            tryte_string = TryteString.from_string(str(data))

        # Monitor how long the transaction takes
        start = time.time()

        # Gets an appropriate address for sending transaction
        if self.reuse_address:
            if self.address is '':
                self.address = self.generate_address(address_level)  # Generates a new unused address
        else:
            self.address = self.generate_address(address_level)

        # Checks address to ensure there was no problem
        if self.address is None:
            self.post_to_tangle(data)

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
            )

            # Times of transaction
            end = time.time()
            elapsed_time = end - start

            if verbose:
                print("Transaction complete \nElapsed time: ", elapsed_time, " seconds.")

            return elapsed_time

        except iota.BadApiResponse:
            print("Transaction failed, retrying...")
            self.post_to_tangle(data)

    def get_transactions(self, tags, most_recent=True, count=10) -> [Transaction]:
        """Creates Transaction objects from the transaction trytes

        :param tags: List of tags
        :param most_recent: whether you want most recent transactions or not
        :param count: Specifies how many transactions you want given you want most recent transactions
        :return: List of Transaction objects
        """

        transactions_hashes = self.api.find_transactions(tags=tags)['hashes']

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

    def get_transaction_data(self, transaction, decrypt=True):
        """Gets the SignatureMessageFragment of a transaction

        :param transaction: Transaction object
        :param decrypt: decrypt data
        :return: Transaction data inside the transaction
        """

        # Get timestamp and message of Transaction
        message = transaction.signature_message_fragment.decode()

        # Decrypt data
        if decrypt:
            message = self.crypto.decrypt(message)
        return message

    def publish(self, minutes):
        for i in range(0, (30 * minutes)):
            self.mqtt.publish_device(self.device_details)

    @staticmethod
    def sort_data(transactions, most_recent, count):
        """Sorts data by the oldest to the newest transactions

        :param transactions: List of transactions
        :param most_recent: Boolean, True if you want the most recent transactions, False if not.
        :param count: If most recent is True, value of count (Int) provides that many transactions.
        :return: returns the data
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
