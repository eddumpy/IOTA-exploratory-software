"""
client.py

Contains the Client class, which is used as the core component for deployment. All deployment settings can be
passed through when creating a Client object, enabling flexibility.

Uses MQTT to communicate with other devices

"""

from iota import Transaction, ProposedTransaction, TryteString, Tag
from Deployment.node import Node
from Deployment.MQTT.device import Device
from Deployment.MQTT.broker import Broker
from Deployment.crypto import Crypto

import iota
import time
import random
import string
from datetime import datetime


class Client:

    def __init__(self,
                 # Device details
                 device_name,  # Device name -> String
                 device_type,  # Device type -> String
                 seed,  # IOTA Seed -> String
                 reuse_address=True,  # If you want to reuse addresses -> Bool

                 #  MQTT configuration
                 mqtt_broker="localhost",  # broker for MQTT communication -> String

                 # Iota node configuration
                 route_pow=True,  # If you wish to route the PoW to a node -> Bool
                 iota_node='https://nodes.devnet.thetangle.org:443',  # URI of IOTA node -> String
                 pow_node='http://localhost:14265'):  # Uri of PoW node -> String

        self.network_name = 'network'  # Name of network
        self.device_type = device_type  # Device type
        self.device_name = device_name  # Name of device

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

        # IOTA api, created through the Node class
        self.api = Node(seed, iota_node, route_pow, pow_node).api

        # MQTT client, devices and brokers
        if self.device_type == 'broker':
            self.mqtt = Broker(name=self.device_name, network_name=self.network_name, broker=mqtt_broker)
        else:
            self.mqtt = Device(name=self.device_name, network_name=self.network_name, broker=mqtt_broker)

        # Class used to encrypt and decrypt data
        self.crypto = Crypto()

    def __str__(self):
        return "Network name: " + self.network_name + "\nDevice type: " + self.device_type \
               + "\nDevice name: " + self.device_name + "\nTag: " + self.tag_string

    def generate_address(self):
        """Gets a new unused address for each transaction, with security level 2

        :return: Address of device
        """

        # Finds the next unused address
        print("Generating address...")
        addresses = self.api.get_new_addresses(count=None, security_level=1)['addresses']
        print("Found an address: ", addresses[0])
        return addresses[0]

    def post_to_tangle(self, data, verbose=False):
        """Posts data to the tangle to a randomly generated address

        :param data: Data to be stored on the tangle
        :param verbose: Prints out the transaction process if True
        """

        # Encrypt data before being posted to tangle
        encrypted_data = self.crypto.encrypt(data)

        # Monitor how long the transaction takes
        start = time.time()

        # Gets an appropriate address for sending transaction
        if self.reuse_address:
            if self.address is '':
                self.address = self.generate_address()  # Generates a new unused address
        else:
            self.address = self.generate_address()

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
                        message=TryteString.from_bytes(encrypted_data),
                    ),
                ],
            )

            if verbose:
                end = time.time()
                print("Transaction complete \nElapsed time: ", end - start, " seconds.")

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

    def get_transaction_data(self, transaction):
        """Gets the SignatureMessageFragment of a transaction

        :param transaction: Transaction object
        :return: Transaction data inside the transaction
        """

        # Get timestamp and message of Transaction
        message = transaction.signature_message_fragment.decode()

        # Decrypt data
        decrypted_data = self.crypto.decrypt(message)
        return decrypted_data

    def publish(self, minutes):
        for i in range(0, (30 * minutes)):
            self.mqtt.publish_device(self.device_details)

    def check_device_status(self, tag):

        # Checks the data
        transactions = self.get_transactions(tags=[tag], count=5)
        tx_data = [self.get_transaction_data(transaction) for transaction in transactions]

        # Checks the timestamps
        timestamps = self.get_timestamps(transactions[1:], as_int=True)

        timestamp_diff = ((datetime.fromtimestamp(round(int(timestamps[1]) / 1000))
                           - datetime.fromtimestamp(round(int(timestamps[0]) / 1000))).total_seconds() / 60)

        if len(set(tx_data)) != 1 and timestamp_diff < 5:
            device_status = 'Green'
        else:
            device_status = 'Red'
        return device_status

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

    @staticmethod
    def get_timestamps(transactions, as_int=False):

        timestamps = [tx.timestamp for tx in transactions]

        if not as_int:
            converted_timestamps = [datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                                    for timestamp in timestamps]
            return converted_timestamps
        else:
            return timestamps
