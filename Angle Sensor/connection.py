# Script is to test that we can establish some sort of connection with the sensor
# TO DO: 


import canopen
import time

network = canopen.Network()

# Hardcoding which channel to use
network.connect(bustype='pcan', channel= 'PCAN_USBBUS1', bitrate= 125000)

network.scanner.search()

time.sleep(0.05)

for node_id in network.scanner.nodes: # scans for ids
    print("Found node %d!" % node_id)

#msg = bytearray(0x003200401000000)
#network.send_message(90,[0x01,0x02,0x03]) # dummy message seems to successful because no error so..
#time.sleep(0.1)
#messages = network.receive(timeout=1.0) # receive doesn't work
#for message in messages:
 #   print('Received message:',message)
    
pathofeds = "as5-101.eds" # path to the eds file(manual containing the sensor's registers and stuff)
node = network.add_node(90,pathofeds) # adds the sensor id to the network
sdoserver = node.sdo

# TEST DOCAL
# At this point it should be all 0, as nothing is calibrated at this point
cal_stat = (sdoserver[0x2003][0x04]).raw # gets the stats bit from status register(2003)
print("OLD Status:{:08b}".format(cal_stat)) # Prints out status

msg = "2f03200401000000" # DoCalmsg
msg_hex_array = [0x2f, 0x03, 0x20,0x04,0x01,0x00,0x00, 0x00]
print(msg_hex_array)
msg_array = bytearray(msg_hex_array)
#print(bytearray(8))
print(bytes(msg_array))
#msg_array[0:4]=([0x2f], [0x03], [0x20], [0x04],[0x01])



sdoserver.download(0x2003,0x04,bytes(msg_array),False) # to send msg to board(A Docal msg)

# At least one Bit should have changed, if the calibration was successful
cal_stat = (sdoserver[0x2003][0x04]).raw # gets the stats bit from status register(2003)
print("New Status:{:08b}".format(cal_stat)) # Prints out status

#response = sdoserver.upload(0x2003,0x04)
#print(response)

#cal_stat_bit = (0b11000000 & cal_stat) >> 6 #Bit mask for status bits(the first two bits to see if it is fully calibrated)
#This is to test that the msg is received. 
angle = (sdoserver[0x2004][0x01].raw) / 10.0 # returns the decimal value of the angle stored in angle register(2004)


# In single angle mode, all angles are saved in Angle 1, 2, and 3.(subindexes of 2004)


print("Angle data:", angle)

# to send messages using the sdo


network.disconnect()

#if __name__ == "__main__":
