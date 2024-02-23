# Script is to test that we can establish some sort of connection with the sensor
# connecting to the network, finding the specific node, and opening a stream to and fro
# GOAL : Sending a message and receiving one back.
import canopen
import time

network = canopen.Network()

# Hardcoding which channel to use
network.connect(bustype='pcan', channel= 'PCAN_USBBUS1', bitrate= 125000)

network.scanner.search()

time.sleep(0.05)

for node_id in network.scanner.nodes:
    print("Found node %d!" % node_id)

#board = network.add_node(90)# needs an eds file to add node
#msg = bytearray(0x003200401000000)
#network.send_message(90,[0x01,0x02,0x03]) # dummy message seems to successful because no error so..
#time.sleep(0.1)
#messages = network.receive(timeout=1.0) # receive doesn't work
#for message in messages:
 #   print('Received message:',message)
    
pathofeds = "as5-101.eds"
node = network.add_node(90,pathofeds)

#print object dictionary(Currently can't load anything as the object is empty)
#for obj in node.object_dictionary.values():
    #print(obj)
 #   print('0x%X: %s' % (obj.index, obj.name))
 #   if isinstance(obj, canopen.objectdictionary.ODRecord):
 #      for subobj in obj.values():
 #          print('  %d: %s' % (subobj.subindex, subobj.name))
cal_stat = (node.sdo[0x2003][0x04]).raw

cal_stat_bit = (0b11000000 & cal_stat) >> 6 #Bit mask for status bits

print("Status:{:02b}".format(cal_stat_bit)) # Prints out status


# to send messages using the sdo


network.disconnect()

#if __name__ == "__main__":
