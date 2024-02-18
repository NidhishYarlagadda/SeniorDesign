# Script is to test that we can establish some sort of connection with the sensor
# connecting to the network, finding the specific node, and opening a stream to and fro
# GOAL : Sending a message and receiving one back.
import canopen
import time

network = canopen.Network()

# Hardcoding which channel to use
network.connect(bustype='pcan', channel= 'PCAN_USBBUS1', bitrate= 1251000)

network.scanner.search()

time.sleep(0.05)

for node_id in network.scanner.nodes:
    print("Found node %d!" % node_id)

# Create board object
nodeId = 90
board = network[nodeId]

#print object dictionary
for obj in board.object_dictionary.values():
    print('0x%X: %s' % (obj.index, obj.name))
    if isinstance(obj, canopen.objectdictionary.ODRecord):
        for subobj in obj.values():
            print('  %d: %s' % (subobj.subindex, subobj.name))
network.disconnect()

#if __name__ == "__main__":
