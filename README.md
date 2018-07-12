# IOTA-application

IoT applications using IOTA for University research project.

To run any of the scripts, ensure this git repository is downloaded or cloned into a directory on to your machine.

To clone this repository using the command line, navigate to the appropriate directory and use the command:

``git clone https://github.com/eddumpy/IOTA-application.git``

## Dependencies 

To run any of the scripts the Python IOTA API library, PYOTA, needs to be installed. Go to the directory where you cloned this repository and install PYOTA.

``pip install pyota``

To find further installation instructions, they can be found at:

https://github.com/iotaledger/iota.lib.py

## IOTA Nodes

To edit the node configuration the ``node.py`` needs to be edited. To do this, edit the default parameters in  ``client.py``, as this is where the Node object is created. You can also change the configuration when creating the client object in the device scripts.

The current configuration connects to the IOTA devnet using one of the public IOTA devnet nodes. This can be changed to connect to the mainnet (not recommended), by entering the node you wish to connect to. Nodes can be found in the IOTA discord chat room. 

The configuration also has an option to route the proof of work to a local running node, this is recommended for the devnet as a lot of the public nodes do not offer proof of work. The parameters are shown below:

``route_pow=True``
``iota_node='https://nodes.devnet.thetangle.org:443'``
``pow_node='http://localhost:14265'``

Setting up a locally running node can be done by following the instructions found at:

https://github.com/iotaledger/iri

There is no need to set it up with neighbours as we only want to use it to provide the proof of work. Once, everything is installed, open up the terminal on your machine and use the command:

`` java -jar iri-1.5.0.jar -p 14265 --testnet --remote``

## Running the scripts




