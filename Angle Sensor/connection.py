# Script is to test that we can establish some sort of connection with the sensor
# TO DO: 


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
sdoclient = node.sdo
msg = 0x01000000 # msg
sdoclient.download(0x2003,0x04,msg,) # to send msg to board(A Docal msg)
cal_stat = (sdoclient[0x2003][0x04]).raw # gets the stats bit from status register(2003)

#cal_stat_bit = (0b11000000 & cal_stat) >> 6 #Bit mask for status bits
#This is to test that the msg is received. 
print("Status:{:06b}".format(cal_stat)) # Prints out status

angle = (sdoclient[0x2004][0x01].raw) / 10.0 # returns the decimal value of the angle stored in angle register(2004)


# In single angle mode, all angles are saved in Angle 1, 2, and 3.(subindexes of 2004)


print("Angle data:", angle)

# to send messages using the sdo


network.disconnect()

#if __name__ == "__main__":
