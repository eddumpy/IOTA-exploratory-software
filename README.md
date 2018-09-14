# IOTA-exploratory-software

Exploratory software is developed to review the DLT IOTA. It is built for my end of year research project at the University of Bath for a Msc in Computer science. 

## Overview

* The software stores real-time data from any device on IOTA's tangle

* Device data is categorised using MQTT topics

* MQTT is also used for devices to discover data streams by sharing tags

* Support flexible node configurations

## Dependencies 

To run any of the scripts the Python IOTA API library, PyOTA, needs to be installed. To install PyOTA, 
run the command below in the command line:

``pip install pyota``

To find further installation instructions, they can be found at:

https://github.com/iotaledger/iota.lib.py

## Deployment

The deployment works so that all you have to do is pass in the relevant configuration settings in to the Client class 
parameters (found in ``client.py``).

### Client class

To create a device script, a client object is needed, it has 10 parameters: When running any of the device scripts you will be asked to name the device, the input given will be passed in the 
parameter  of the client class. This is so devices can identify who is posting data. 

1. ``device_type``: State the type of the device, e.g. sensor, monitor etc.\

2. ``network_name``: Name your network

3. ``seed``: An Iota seed (details of how to obtain one are below)

4. ``device_name``: Name of the device. This is required, so if a name is not given, user input will be requested

5. ``encrypt``: Whether you want to encrypt data on the tangle or not

6. ``reuse_address``: Option to re-use addresses, not recommened but improves performance


To create a seed use a command, found below, in a terminal window:

Mac OS: 

``$ cat /dev/urandom |LC_ALL=C tr -dc 'A-Z9'| fold -w 81 | head -n 1``
  
Linux:

``$ cat /dev/urandom |tr -dc A-Z9|head -c${1:-81}``

##### MQTT

MQTT is used as the communication protocol for devices. Devices will publish their type, name and Tag to MQTT topics. 
Any device set up with the same ``network_name`` can find devices on that network. 


<span>7.</span> ``mqtt_broker``: To use MQTT, you must be connected to a broker. The broker is in charge of handling messages 
and ensuring clients can subscribe and publish to topics. Public brokers can be found online or you can run your 
own broker from your machine. This software used eclipse mosquitto for the message broker.

Once a client object has been created, accessing the MQTT client from the client object you gain access to the ``find_device_tags`` method.
 The ``user_input.py`` provides a way to request the ``number_of_streams`` and ``known_devices`` as user input before the method is called.

* ``read_from``: State which device type you wish to read from

* ``number_of_streams``: Number of streams you want to read from, default is 1 device

* ``known_devices``: List of devices you want to read from

##### IOTA Node

To interact with the tangle, you need to connect to a synced IOTA node. The parameters that concern the IOTA node are:

<span>8.</span>``iota_node``: The IOTA node you wish to connect to, you will need the URI of the node

<span>9.</span>``route_pow`` **[Optional]**: Determines if you wish to dedicate the proof of work to another node

<span>10.</span>``pow_node`` **[Optional]**: If you wish to route your proof of work, state the relevant IOTA node


The current configuration connects to the IOTA devnet using one of the public IOTA devnet nodes. This can be changed to
connect to the mainnet (not recommended) by entering the URI of an IOTA node in ``iota_node``. If you do not want to 
run your own node you can find public nodes in the IOTA discord chat room. Proof of work is also routed because a lot of 
public IOTA devnet nodes do not offer the proof of work, instead a locally running node with no neighbours is used for 
proof of work. Setting up a locally running node can be done by following the instructions found at:

https://github.com/iotaledger/iri

Once you have the iri installed correctly, open up the terminal on your machine navigate to the directory 
with ``iri-1.5.0.jar`` and run the command:

``java -jar iri-1.5.0.jar -p 14265 --testnet --remote``

_Note: The version of the IRI may have changed so ensure you run the command with the right version_



## Running the device scripts

To run the device scripts, ensure this git repository is downloaded or cloned into a directory on your machine which has access to the PyOTA library.

To clone this repository using the command line, navigate to the appropriate directory and use the command:

``git clone https://github.com/eddumpy/IOTA-application.git``

The device scripts directory contains python files that imitate programs run on IoT devices. You can create your own device scripts and then make use of the client class to store data in the tangle or set up your own network of devices. 
