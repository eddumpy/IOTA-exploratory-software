from iota import Transaction, ProposedTransaction, TryteString, Tag
import time
import datetime

"""Client class:

Methods in this class provide ways to:
  -  Store data on the tangle
  -  Query data on the tangle
  -  Read data on the tangle
  -  Sort data from the tangle
  -  Manipulate data from the tangle
"""


class Client:

    def __init__(self, api, tag):
        self.api = api
        self.tag = tag

    def get_transactions_hashes(self, tag: [Tag]) -> [TryteString]:
        """Gets transaction hashes of a given tag

        :param tag: Tag used by the device when sending transactions
        :return: List of Transaction hashes
        """

        transactions_hashes = self.api.find_transactions(tags=tag)
        txs_hashes = transactions_hashes['hashes']
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

        # Get an address to send data
        result = self.api.get_new_addresses(count=1, security_level=2)
        addresses = result['addresses']
        address = addresses[0]

        # Monitor how long the transaction takes
        start = time.time()

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
                    message=TryteString.from_string(str(data)),
                ),
            ],
        )

        if verbose:
            end = time.time()
            print("Transaction complete, elapsed time: ", end - start, " seconds.")

    def read_data(self, transaction_data):
        """Prints transaction data to the console

        :param transaction_data: List of transaction data -> [(timestamp, message)]
        """
        """Given a list of tuples (timestamp, data), method will print out transaction information"""
        for tx_data in transaction_data:
            # Convert unix timestamp int to readable format
            value = datetime.datetime.fromtimestamp(tx_data[0])
            time_of_transaction = value.strftime('%d/%m/%Y% %H:%M:%S')
            print(time_of_transaction, "Data: ", tx_data[1])

    def sort_data(self, data, most_recent=True, count=10):
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

    def get_transaction_info(self, transaction):
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


