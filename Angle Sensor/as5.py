# This is the API for the AS5 Angle Sensor that uses CANOPEN to send and recieve
# messages from the angle sensor.

class AS5():

    # Summary:
    #       AS5 object default constructor.
    # Parameters:
    #
    # Returns:
    #       None
    def __init__(self, network): # initializes with network being passed

        self.calibrationdone= False
        self.Xaxisup = False
        self.Xaxisdown = False
        self.Yaxisdown = False
        self.Yaxisup  = False
        self.Zaxisdown = False
        self.Zaxisup = False
        self.network = network
        self.statusbits = 0
        pass

    # Summary:
    #       Sends the doCal signal to the board to put the board in calibration mode.
    # Parameters:
    #
    # Returns:
    #
    def DoCal(self):
        #self.calibrationInit = True
        pass

    # Summary:
    #       Calibrates the sensor for a specific axis.
    # Operations:
    # Send DOcal message,
    # If SdoCommunication Error, send Docal message again.
    
    # Bitmask check for which sides are calibrated, and update the side boolean.
    
    # if statusbits == ff: then set calbrationdone to True

    #Return:

    


     
    #
    def calibrate(self,axis):
        if not self.calibrationInit:
            raise Exception("Intiaialize calibration first")

    # Summary:
    #       Obtains the axis specific angle data.
    # Parameters:
    #       axis: a str that represents which axis to look at.
    # Returns:
    #       double: the angle measurment.
    def getAngle(self,axis):
        pass

