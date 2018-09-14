import sys


def get_user_input():
    """Gets user input for details of devices to look for

    :return: devices, streams
    """

    devices_question = input("Are there any known devices you wish to read from? (y/n): ")

    if devices_question == 'y' or devices_question == 'Y':
        devices = [str(x) for x in input("Provide device name(s) with a space between:\n").split()]
        streams = len(devices)

    elif devices_question == 'n' or devices_question == 'N':
        devices = []
        streams = input("How many devices would you like to read from: ")

        try:
            streams = int(streams)
        except ValueError:
            print("Integer not entered, please restart device.")
            sys.exit()

        if streams == 0:
            print("No streams chosen, default number of streams will be read (1)")
            streams = 1

    else:
        print("Invalid entry, please restart device and try again.")
        sys.exit()
    return devices, streams
