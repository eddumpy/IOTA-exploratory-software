
def get_user_input():

    devices_question = input("Are there any known devices you wish to read from? (y/n): ")

    if devices_question == 'y':
        devices = [str(x) for x in input("Provide device name(s) with a space between:\n").split()]
        streams = len(devices)
    else:
        devices = []
        streams = int(input("How many devices would you like to read from: "))

    return devices, streams
