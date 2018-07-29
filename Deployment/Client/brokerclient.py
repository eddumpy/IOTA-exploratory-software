
from Deployment.MQTT.broker import MqttBroker
from Deployment.Client.client import Client

from datetime import datetime
from prettytable import PrettyTable
import copy


class BrokerClient(Client):

    def __init__(self, device_name, device_type, seed, reuse_address=True,
                 mqtt_broker="localhost", route_pow=True,
                 iota_node='https://nodes.devnet.thetangle.org:443',
                 pow_node='http://localhost:14265'):

        super(BrokerClient, self).__init__(device_name, device_type, seed, reuse_address, mqtt_broker, route_pow,
                                           iota_node, pow_node)

        self.mqtt = MqttBroker(name=self.device_name, network_name=self.network_name, broker=mqtt_broker)

    def check_device_status(self, tag):

        # Checks the data
        transactions = self.get_transactions(tags=[tag], count=5)
        tx_data = [self.get_transaction_data(transaction) for transaction in transactions]

        # Checks the timestamps
        timestamps = self.get_timestamps(transactions[1:], as_int=True)

        timestamp_diff = ((datetime.fromtimestamp(round(int(timestamps[1]) / 1000))
                           - datetime.fromtimestamp(round(int(timestamps[0]) / 1000))).total_seconds() / 60)

        if timestamp_diff > 10:
            device_status = 'Offline'
        elif len(set(tx_data)) == 1:
            device_status = 'Broken'
        else:
            device_status = 'Online'
        return device_status

    def create_table(self, devices, tag=True, status=True,
                     last_tx=True, last_reading=True, total_txs=True):

        """Creates a table with information about devices

        """

        # Default attributes for table
        default_attributes = ['Type', 'Name']

        # Uses the arguments to create a list of attributes
        arguments = [tag, status, last_tx, last_reading, total_txs]
        extra_attributes = ['Tag', 'Status', 'Last Transaction', 'Last Reading', 'Total transactions']

        # Final attributes list
        attributes = default_attributes + [att for a, att in zip(arguments, extra_attributes) if a]

        # Creates table
        table = PrettyTable(attributes)

        for device in devices:

            device_tag = copy.copy(device[2])
            transactions = self.get_transactions([device_tag], most_recent=False)
            latest_transaction = transactions[-1:]

            if not tag:
                device = copy.copy(device[:2])

            if status:
                status = self.check_device_status(device_tag)
                device.append(status)

            if last_tx:
                time_of_transaction = self.get_timestamps(latest_transaction)[0]
                device.append(time_of_transaction)

            if last_reading:
                last_transaction_data = self.get_transaction_data(latest_transaction[0])
                device.append(last_transaction_data)

            if total_txs:
                num_of_txs = len(transactions)
                device.append(num_of_txs)

            table.add_row(device)

        return table

    @staticmethod
    def get_timestamps(transactions, as_int=False):

        timestamps = [tx.timestamp for tx in transactions]

        if not as_int:
            converted_timestamps = [datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                                    for timestamp in timestamps]
            return converted_timestamps
        else:
            return timestamps
