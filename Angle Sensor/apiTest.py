from as5 import AS5
import canopen

network = canopen.Network()

myDevice = AS5(network)

myDevice.DoCal()

print(myDevice.getAngle(0))


network.disconnect()


