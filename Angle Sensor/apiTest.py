from as5 import AS5
import canopen
import time

network = canopen.Network()
# Hardcoding which channel to use
network.connect(bustype='pcan', channel= 'PCAN_USBBUS1', bitrate= 125000)

myDevice = AS5(network)
myDevice.DoCal()

while(1):
   print(myDevice.getAngle(0))
   time.sleep(0.003)


#myDevice.DoCal()





network.disconnect()


