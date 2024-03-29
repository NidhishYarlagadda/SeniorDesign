from as5 import AS5
import canopen

network = canopen.Network()
# Hardcoding which channel to use
network.connect(bustype='pcan', channel= 'PCAN_USBBUS1', bitrate= 125000)

myDevice = AS5(network)
myDevice.DoCal()

while(1):
   print(myDevice.getAngle(0))


#myDevice.DoCal()





network.disconnect()


