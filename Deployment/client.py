"""
client.py

Contains the Client class, which is used as the core component for deployment. All deployment settings can be
passed through when creating a Client object, enabling flexibility.

Uses MQTT to communicate with other devices

"""

import iota
from iota import Transaction, ProposedTransaction, TryteString, Tag
from Deployment.node import Node
from Deployment.mqtt import MQTT
from Deployment.crypto import Crypto

import time
import random
import string


class Client:

    def __init__(self,
                 # Device details
                 device_name,  # Device name -> String
                 device_type,  # Device type -> String
                 seed,  # IOTA Seed -> String
                 known_devices,  # Specifies if you want to read from any known devices -> [String]
                 reuse_address=True,  # If you want to reuse addresses

                 #  MQTT configuration
                 read_from_device_type=None,  # Specifies which devices you wish to read from
                 number_of_streams=1,  # Specifies how many streams you wish to read from -> Int
                 mqtt_broker="localhost",  # broker for MQTT communication -> String

                 # Iota node configuration
                 route_pow=True,  # If you wish to route the PoW to a node -> Bool
                 iota_node='https://nodes.devnet.thetangle.org:443',  # URI of IOTA node to connect to -> String
                 pow_node='http://localhost:14265'):  # Uri of PoW node -> String

        # Name of device, if empty will be seen as 'unknown device'
        self.device_name = device_name
        self.device_type = device_type

        # Device address info
        self.reuse_address = reuse_address
        self.address = ''

        # IOTA api, created through the Node class
        self.api = Node(seed, iota_node, route_pow, pow_node).api

        # Creates a random Tag to classify current data stream
        self.tag_string = ''.join(random.choice(string.ascii_uppercase + '9') for _ in range(27))
        self.tag = Tag(self.tag_string)

        # MQTT client to use with the Iota client
        self.mqtt = MQTT(device_name=self.device_name,
                         device_tag=self.tag_string,
                         device_type=self.device_type,
                         read_from=read_from_device_type,
                         broker=mqtt_broker,
                         known_devices=known_devices,
                         number_of_streams=number_of_streams)

        # Class used to encrypt and decrypt data
        self.crypto = Crypto()

        # Stores the most recent transaction timestamp
        self.most_recent_transaction = None

    def generate_address(self):
        """Gets a new unused address for each transaction, with security level of 2

        :return: Address of device
        """
        addresses = self.api.get_new_addresses(count=None, security_level=2)['addresses']
        address = addresses[0]
        self.address = address
        return address

    def get_transactions_hashes(self, tags: [Tag]) -> [TryteString]:
        """Gets transaction hashes of a given tag

        :param tags: Tag used by the device when sending transactions
        :return: List of Transaction hashes
        """

        transactions_hashes = self.api.find_transactions(tags=tags)
        txs_hashes = transactions_hashes['hashes']

        if not txs_hashes:
            print("No Transactions found, waiting for transactions...")
            time.sleep(60)
            self.get_transactions_hashes(tags)
        else:
            return txs_hashes

    def get_transactions(self, tx_hashes, most_recent=True, count=10) -> [Transaction]:
        """Creates Transaction objects from the transaction trytes


        :param tx_hashes: List of Transaction hashes
        :param most_recent: whether you want most recent transactions or not
        :param count: Specifies how many transactions you want given you want most recent transactions
        :return: List of Transaction objects
        """

        # The hashes are used to get the raw transaction trytes, which can then be converted to
        # Transaction objects.
        result = self.api.get_trytes(tx_hashes)
        tx_trytes = result['trytes']

        # Stores the Transaction objects in a list
        transactions = [Transaction.from_tryte_string(tryte) for tryte in tx_trytes]

        # Sorts the transactions into order
        ordered_transactions = self.sort_data(transactions, most_recent, count)

        return ordered_transactions

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

        except iota.adapter.BadApiResponse:
            print("Transaction failed, retrying...")
            self.post_to_tangle(data)

    def search_for_devices(self):
        """Finds devices to read data streams

        :return: The tags used to post data from found devices-> [Tags]
        """

        self.mqtt.find_data_streams()
        tags = [Tag(tag) for tag in self.mqtt.tags_found]
        for device in self.mqtt.devices_found:
            print("Reading from ", device)
        return tags

    def sort_data(self, transactions, most_recent, count):
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

        # Store the most recent transaction
        self.most_recent_transaction = ordered_transactions[len(ordered_transactions) - 1]

        # Return the most recent transactions or all transactions
        if most_recent is True:
            return ordered_transactions[-count:]
        else:
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

    def wait_and_publish(self, minutes):
        for i in range(0, (6 * minutes)):
            self.mqtt.publish_data_stream()
