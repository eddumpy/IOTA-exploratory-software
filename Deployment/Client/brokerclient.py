from Deployment.MQTT.mqtt_broker import MqttBroker
from Deployment.Client.client import Client

from datetime import datetime
from prettytable import PrettyTable
import copy
import time


class BrokerClient(Client):

    def __init__(self, device_type, seed, device_name='', reuse_address=True,
                 mqtt_broker="localhost", route_pow=True,
                 iota_node='https://nodes.devnet.thetangle.org:443',
                 pow_node='http://localhost:14265'):

        super(BrokerClient, self).__init__(device_type, seed, device_name, reuse_address, mqtt_broker, route_pow,
                                           iota_node, pow_node)

        self.mqtt = MqttBroker(network_name=self.network_name, broker=mqtt_broker)

    def check_device_status(self, tag):
        """Checks

        :param tag: Tag of a device
        :return:
        """

        # Checks the data
        transactions = self.get_transactions(tags=[tag], count=5)
        tx_data = [self.get_transaction_data(transaction) for transaction in transactions]

        # Checks the timestamps
        timestamps = self.get_timestamps(transactions, as_int=True)

        if len(timestamps) <= 1:
            accumulate_diff = 0
        else:
            accumulate_diff = 0
            for i in range(len(timestamps) - 1, 0, -1):
                timestamp_diff = ((datetime.fromtimestamp(int(timestamps[i]))
                                   - datetime.fromtimestamp(int(timestamps[i - 1]))).total_seconds())
                accumulate_diff += timestamp_diff
            accumulate_diff /= 60

        current_time = round(time.time())
        time_since_last_transaction = ((datetime.fromtimestamp(current_time) -
                                       datetime.fromtimestamp(int(timestamps[len(timestamps) - 1])))
                                       .total_seconds()) / 60

        # Checks to see if device is online or offline
        if time_since_last_transaction > 30:
            device_status = 'Offline'
        else:
            # If online, check its data and transaction times
            if len(set(tx_data)) == 1:
                device_status = 'Data error'
            elif accumulate_diff > 10:
                device_status = 'Slow Txs'
            else:
                device_status = 'Online'
        return device_status

    def get_device_data(self, devices, tag=True, status=True,
                        last_tx=True, last_reading=True, total_txs=True):

        # Default attributes for table
        default_attributes = ['Type', 'Name']

        # Uses the arguments to create a list of attributes
        arguments = [tag, status, last_tx, last_reading, total_txs]
        extra_attributes = ['Tag', 'Status', 'Last Transaction', 'Last Reading', 'Total transactions']

        # Final attributes list
        attributes = default_attributes + [att for a, att in zip(arguments, extra_attributes) if a]

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
        return devices, attributes

    @staticmethod
    def query_device_data(devices, status=None):
        if status is not None:
            updated_devices = [device for device in devices if status in device]
            return updated_devices
        else:
            return devices

    @staticmethod
    def create_table(devices, attributes):
        # Creates table
        table = PrettyTable(attributes)
        for device in devices:
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
