"""Client class:

Methods in this class provide ways to:
  -  Store data on the tangle
  -  Query data on the tangle
  -  Read data on the tangle
  -  Sort data from the tangle
  -  Manipulate data from the tangle
"""

import random
import string

from iota import Transaction, ProposedTransaction, TryteString, Tag
from Classes.node import Node
from Classes.mqtt import MQTT
import time
import datetime


class Client:

    def __init__(self,
                 device_name='',
                 seed='',
                 subscribe_topic='',
                 publish_topic='',
                 route_pow=True,
                 iota_node='https://nodes.devnet.thetangle.org:443',
                 pow_node='http://localhost:14265'):

        # Describes the device function
        self.device_name = device_name

        # IOTA api, created through the Node class
        self.api = Node(seed, iota_node, route_pow, pow_node).api

        # Gets an Address for device
        self.address = self.generate_address()

        # Tag to classify current data stream
        self.tag_string = self.generate_tag()
        self.tag = Tag(self.tag_string)

        # Defines the topics the device has subscribed or can publish too
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic

        # MQTT client to use with the Iota client
        self.mqtt = MQTT(device_name=self.device_name,
                         subscribe_topic=self.subscribe_topic,
                         publish_topic=self.publish_topic)

    def generate_tag(self, size=27, chars=string.ascii_uppercase + '9'):
        """Generates a tag for a client

        :param size: Max number of trytes
        :param chars: Uppercase letters and the number 9
        :return: A tag for a client to use
        """

        tag_string = ''.join(random.choice(chars) for _ in range(size))
        return tag_string

    def generate_address(self):
        """Gets an address for the device

        :return: Address of device
        """
        result = self.api.get_new_addresses(count=1, security_level=2)
        addresses = result['addresses']
        address = addresses[0]
        return address

    def get_transactions_hashes(self, tag: [Tag]) -> [TryteString]:
        """Gets transaction hashes of a given tag

        :param tag: Tag used by the device when sending transactions
        :return: List of Transaction hashes
        """

        transactions_hashes = self.api.find_transactions(tags=tag)
        txs_hashes = transactions_hashes['hashes']

        if not txs_hashes:
            print("No Transactions found, waiting for transactions...")
            time.sleep(60)
            self.get_transactions_hashes(tag)
        else:
            return txs_hashes

    def get_transactions(self, tx_hashes: [TryteString]) -> [Transaction]:
        """Creates Transaction objects from the transaction trytes

        :param tx_hashes: List of Transaction hashes
        :return: List of Transaction objects
        """

        # The hashes are used to get the raw transaction trytes, which can then be converted to
        # Transaction objects.
        result = self.api.get_trytes(tx_hashes)
        tx_trytes = result['trytes']

        # Stores the Transaction objects in a list
        transactions = [Transaction.from_tryte_string(tryte) for tryte in tx_trytes]
        return transactions

    def post_to_tangle(self, data, verbose=False, tag=None):
        """Posts data to the tangle to a randomly generated address

        :param tag: Uses default tag of device if none is given
        :param data: Data to be stored on the tangle
        :param verbose: Prints out transaction process if True
        """

        # Uses the devices tag if none is given
        if tag is None:
            tag = self.tag

        # Monitor how long the transaction takes
        start = time.time()

        if verbose:
            print("Transaction Initialised...")
            print("Sending to: ", self.address)

        # Posts data to the tangle
        self.api.send_transfer(
            depth=3,
            transfers=[
                ProposedTransaction(
                    address=self.address,
                    value=0,
                    tag=tag,
                    message=TryteString.from_string(str(data)),
                ),
            ],
        )

        if verbose:
            end = time.time()
            print("Transaction complete \nElapsed time: ", end - start, " seconds.")

    @staticmethod
    def read_data(transaction_data):
        """Prints transaction data to the console

        :param transaction_data: List of transaction data -> [(timestamp, message)]
        """
        """Given a list of tuples (timestamp, data), method will print out transaction information"""
        for tx_data in transaction_data:
            # Convert unix timestamp int to readable format
            value = datetime.datetime.fromtimestamp(tx_data[0])
            time_of_transaction = value.strftime('%d/%m/%Y% %H:%M:%S')
            print(time_of_transaction, "Data: ", tx_data[1])

    @staticmethod
    def sort_data(data, most_recent=True, count=10):
        """Sorts data by the oldest to the newest transactions

        :param data: list of data -> [(timestamp, message)]
        :param most_recent: Boolean, True if you want the most recent transactions, False if not.
        :param count: If most recent is True, value of count (Int) provides that many transactions.
        :return: returns the data
        """
        # Sort transactions by timestamps
        data.sort(key=lambda tup: tup[0])

        if most_recent is True:
            return data[-count:]
        else:
            return data

    @staticmethod
    def get_transaction_info(transaction):
        """Gets the timestamp and message of a transaction

        :param transaction: Transaction object
        :return: Transaction data -> (timestamp, message)
        """

        # Get timestamp and message of Transaction
        timestamp = transaction.timestamp
        message = transaction.signature_message_fragment

        # Decoding message tryte string
        sensor_data = message.decode()

        # Create data tuple
        transaction_data = (timestamp, sensor_data)
        return transaction_data

    def get_latest_transaction_info(self, transactions):
        """Gets the most recent data from the list of transactions

        :param transactions: List of transaction objects
        :return: The most recent transaction data from the list of transactions
        """

        tx_timestamps = []
        tx_data = []
        for tx in transactions:
            info = self.get_transaction_info(tx)
            tx_timestamps.append(info[0])
            tx_data.append(info[1])

        latest_reading = max(tx_timestamps)
        data = tx_data[tx_timestamps.index(latest_reading)]
        return data

    def convert_tag_strings(self, tags_found):
        tags = []
        for tag in tags_found:
            tags.append(Tag(tag))
        return tags
