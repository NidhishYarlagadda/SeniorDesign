# This is the API for the AS5 Angle Sensor that uses CANOPEN to send and recieve
# messages from the angle sensor.

class AS5():

    # Summary:
    #       AS5 object default constructor.
    # Parameters:
    #
    # Returns:
    #       None
    def __init__(self):

        self.calibrationInit = False
        pass

    # Summary:
    #       Sends the doCal signal to the board to put the board in calibration mode.
    # Parameters:
    #
    # Returns:
    #
    def startCal(self):
        self.calibrationInit = True
        pass

    # Summary:
    #       Calibrates the sensor for a specific axis.
    # Parameters:
    #       axis: a str that represents which axis to calibrate.
    # Returns:
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

