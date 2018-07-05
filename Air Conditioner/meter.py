from iota import Tag


class Meter:

    def __init__(self, client):
        self.temperature_tag = [Tag(b"TEMPSENSOR999")]  # list of tags from temperature sensors
        self.aircon_tag = [Tag(b"AIRCON999")]  # List of tags from Air conditioner units
        self.client = client  # Avoids creating another client object

    def get_temperature(self):
        """Gets the temperature from the sensor.

        :return: Returns the latest temperature reading by the temperature sensor.
        """

        # Gets the transaction hashes from the temperature tag
        transaction_hashes = self.client.get_transactions_hashes(self.temperature_tag)

        # If no transaction hashes are found, a default temperature of 20 is assumed, otherwise the temperature is
        # the reading from the tangle
        if not transaction_hashes:
            latest_temperature_reading = 20  # default temperature
        else:
            transactions = self.client.get_transactions(transaction_hashes)
            latest_temperature_reading = self.client.get_latest_transaction_info(transactions)

        print("latest Temperature reading: " + latest_temperature_reading + " Degrees")
        return int(latest_temperature_reading)

    def get_aircon_state(self):
        """Gets the air-conditioner state by looking on the tangle

        :return: State of the air-conditioner
        """

        # Get the transaction hashes of previous transactions by the air conditioner
        transaction_hashes = self.client.get_transactions_hashes(self.aircon_tag)

        # If no previous transactions, the air-conditioner is off
        if not transaction_hashes:
            is_on = False
        else:
            transactions = self.client.get_transactions(transaction_hashes)
            state = self.client.get_latest_transaction_info(transactions)

            if state == "1":
                is_on = True
            else:
                is_on = False
        return is_on







