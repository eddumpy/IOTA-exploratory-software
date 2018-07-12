
def get_user_input():

    # default device value
    devices = None

    # Get a device name from the user
    name = input("Please provide a name for the device: ")

    devices_question = input("Are there any known devices you wish to read from? (y/n): ")

    if devices_question == 'y':
        devices = [str(x) for x in input("Provide device name(s) with a space between:\n").split()]

    return name, devices
