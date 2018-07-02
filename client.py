from iota import Transaction, ProposedTransaction, TryteString, Tag
import time
import datetime


class Client:

    def __init__(self, api, tag):
        self.api = api
        self.tag = tag

    def get_transactions_hashes(self, tag):
        """Returns transaction hashes"""
        transactions_hashes = self.api.find_transactions(tags=tag)
        txs_hashes = transactions_hashes['hashes']
        return txs_hashes

    def get_transaction_trytes(self, txs_hashes):
        """Returns the raw transaction trytes from the transaction hashes"""
        tx_trytes = self.api.get_trytes(txs_hashes)
        txs = tx_trytes['trytes']
        return txs

    def get_transactions(self, tx_trytes):
        """Given a list of transaction trytes returns a list of Transaction objects"""
        transactions = []
        for tryte in tx_trytes:
            tx = Transaction.from_tryte_string(tryte)
            transactions.append(tx)
        return transactions

    def post_to_tangle(self, data, tag):
        """"Post data to the tangle, data must be of type Trytestring"""
        # Get address to send data
        result = self.api.get_new_addresses(count=1, security_level=2)
        addresses = result['addresses']
        address = addresses[0]

        start = time.time()
        print("Transaction Initialised...")
        print("Sending to: ", address)

        self.api.send_transfer(
            depth=8,
            transfers=[
                ProposedTransaction(
                    address=address,
                    value=0,
                    tag=self.tag,
                    message=TryteString.from_string(str(data)),
                ),
            ],
        )

        end = time.time()
        print("Transaction complete, elapsed time: ", end - start, " seconds.")

    def read_data(self, transactions_data):
        """Given a list of tuples (timestamp, data), method will print out transaction information"""
        for tx_data in transactions_data:
            # Convert unix timestamp int to readable format
            value = datetime.datetime.fromtimestamp(tx_data[0])
            time_of_transaction = value.strftime('%d/%m/%Y% %H:%M:%S')
            print(time_of_transaction, "Data: ", tx_data[1])

    def sort_data(self, data, most_recent=True, count=10):
        """Sorts transaction information by timestamps"""
        # Sort transactions by timestamps
        data.sort(key=lambda tup: tup[0])

        if most_recent is True:
            return data[-count:]
        else:
            return data

    def get_transaction_info(self, transaction):
        """The default data format for this application is a tuple of (timestamp, data)"""
        # Get timestamp and message of Transaction
        timestamp = transaction.timestamp
        message = transaction.signature_message_fragment

        # Decoding message tryte string
        sensor_data = message.decode()

        # Create data tuple
        transaction_data = (timestamp, sensor_data)
        return transaction_data

