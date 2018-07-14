# IOTA-application

IoT applications using IOTA for University research project.

To run any of the scripts, ensure this git repository is downloaded or cloned into a directory on your machine.

To clone this repository using the command line, navigate to the appropriate directory and use the command:

``git clone https://github.com/eddumpy/IOTA-application.git``

## Dependencies 

To run any of the scripts the Python IOTA API library, PYOTA, needs to be installed. To install PYOTA, 
run the command below in the command line:

``pip install pyota``

To find further installation instructions, they can be found at:

https://github.com/iotaledger/iota.lib.py

## Deployment

The deployment works so that all you have to do is pass in the relevant configuration settings in to the Client objects 
parameters (found in ``client.py``). Below explains what these parameters are.

### Device Identity

When running any of the device scripts you will be asked to name the device, the input you give will be passed in the 
parameter ``device_name``. This is so devices can identify who is posting data.

### IOTA Node

To interact with the tangle, you need to connect to a synced IOTA node. The parameters that concern the IOTA node are:

``iota_node``: The IOTA node you wish to connect to, you will need the URI of the node

``route_pow`` **[Optional]**: Determines if you wish to dedicate the proof of work to another node

``pow_node`` **[Optional]**: If you wish to route your proof of work, state the relevant IOTA node


The current configuration connects to the IOTA devnet using one of the public IOTA devnet nodes. This can be changed to
connect to the mainnet (not recommended) by entering the URI of an IOTA node in ``iota_node``. If you do not want to 
run your own node you can find public nodes in the IOTA discord chat room. Proof of work is also routed because a lot of 
public IOTA devnet nodes do not offer the proof of work, instead locally running node with no neighbours was used for 
proof of work. Setting up a locally running node can be done by following the instructions found at:

https://github.com/iotaledger/iri

Once you have the iri installed correctly, open up the terminal on your machine navigate to the directory 
with ``iri-1.5.0.jar`` and run the command:

`` java -jar iri-1.5.0.jar -p 14265 --testnet --remote``

### MQTT

MQTT is used as the communication protocol for devices. Devices will publish their name and Tag they are using 
to post data to a topic. Any device subscribed to the that topic can see which devices are publishing there tags,
and can read all transactions associated with that tag. Below are the parameters needed to set up MQTT.

``mqtt_broker``: To use MQTT, you must be connected to a broker. The broker is in charge of handling messages 
and ensuring clients can subscribe and publish to topics. Public brokers can be found online or you can run your 
own broker from your machine.

``subscribe_topic``: The topic you wish to subscribe to

``publish_topic``: The topic you wish to read from

``number_of_streams`` **[Optional]**: Number of streams you want to read from, default is 1 device

``known_devices`` **[Optional]**: List of devices you want to read from



## Running the scripts

More to come...