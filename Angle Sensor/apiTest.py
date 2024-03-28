from as5 import AS5
import canopen

network = canopen.Network()
# Hardcoding which channel to use
network.connect(bustype='pcan', channel= 'PCAN_USBBUS1', bitrate= 125000)

myDevice = AS5(network)


myDevice.DoCal()

#bin(myDevice.getcalstatus())

#print(myDevice.getAngle(0))


network.disconnect()


