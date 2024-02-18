# Script is to test that we can establish some sort of connection with the sensor
# connecting to the network, finding the specific node, and opening a stream to and fro
# GOAL : Sending a message and receiving one back.
import canopen
import time

network = canopen.Network()

network.connect(bustype='pcan', channel= 'PCAN_USBBUS1', bitrate= 125000)

network.scanner.search()

time.sleep(0.05)

for node_id in network.scanner.nodes:
    print("Found node %d!" % node_id)


network.disconnect()

#if __name__ == "__main__":
