"""
client.py

Contains the Client class, which is used as the core component for deployment. All deployment settings can be
passed through when creating a Client object, enabling flexibility.

Uses MQTT to communicate with other devices

Methods in this class provide ways to:
  -  Store data on the tangle
  -  Query data on the tangle
  -  Read data on the tangle
  -  Sort data from the tangle
  -  Manipulate data from the tangle
"""


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
                 device_name='',  # Device name-> String
                 seed='',  # Seed of device, if empty random seed will be used -> String

                 #  MQTT configuration
                 subscribe_topic='',  # Subscribe topic for mqtt -> String
                 publish_topic='',  # Publish topic for mqtt -> String
                 known_devices=None,  # Specifies if you want to read from any known devices -> [String]
                 number_of_streams=1,  # Specifies how many streams you wish to read from -> Int
                 mqtt_broker="localhost",  # broker for MQTT communication -> String

                 # Iota node configuration
                 route_pow=True,  # If you wish to route the PoW to a node -> Bool
                 iota_node='https://nodes.devnet.thetangle.org:443',  # IOTA node to connect to -> String
                 pow_node='http://localhost:14265'):  # PoW node -> String

        # Name of device, if empty will be seen as 'unknown device'
        self.device_name = device_name

        # IOTA api, created through the Node class
        self.api = Node(seed, iota_node, route_pow, pow_node).api

        # Creates a random Tag to classify current data stream
        self.tag_string = ''.join(random.choice(string.ascii_uppercase + '9') for _ in range(27))
        self.tag = Tag(self.tag_string)

        # Defines the topics the device has subscribed or can publish too
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic

        # MQTT client to use with the Iota client
        self.mqtt = MQTT(device_name=self.device_name,
                         broker=mqtt_broker,
                         subscribe_topic=self.subscribe_topic,
                         publish_topic=self.publish_topic,
                         known_devices=known_devices,
                         number_of_streams=number_of_streams)

        # Message to be posted to topic
        self.message = self.device_name + '/' + self.tag_string

        # Stores the most recent transaction timestamp
        self.most_recent_transaction = None

        # Exit message used for mqtt communication if device goes offline
        self.exit_message = "Exit"

        # Class used to encrypt and decrypt data
        self.crypto = Crypto()

    def generate_address(self):
        """Gets a new unused address for each transaction

        :return: Address of device
        """
        result = self.api.get_new_addresses(count=None, security_level=2)
        addresses = result['addresses']
        address = addresses[0]
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

    def post_to_tangle(self, data, verbose=False, tag=None):
        """Posts data to the tangle to a randomly generated address

        :param tag: Uses default tag of device if none is given
        :param data: Data to be stored on the tangle
        :param verbose: Prints out transaction process if True
        """

        # Encrypt data before being posted to tangle
        encrypted_data = self.crypto.encrypt(plaintext=str(data).encode('utf-8'))

        # Uses the devices tag if none is given
        if tag is None:
            tag = self.tag

        # Monitor how long the transaction takes
        start = time.time()

        # Generates a new unused address
        address = self.generate_address()

        if verbose:
            print("Transaction Initialised...")
            print("Sending to: ", address)

        # Posts data to the tangle
        self.api.send_transfer(
            depth=3,
            transfers=[
                ProposedTransaction(
                    address=address,
                    value=0,
                    tag=tag,
                    message=TryteString.from_bytes(encrypted_data),
                ),
            ],
        )

        if verbose:
            end = time.time()
            print("Transaction complete \nElapsed time: ", end - start, " seconds.")

    def find_devices(self):
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
        message = transaction.signature_message_fragment

        # Decoding message tryte string
        decoded_data = message.decode()

        # Decrypt data
        decrypted_data = self.crypto.decrypt(decoded_data)
        raw_data = str(decrypted_data.decode())

        return raw_data
