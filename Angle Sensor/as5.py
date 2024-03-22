# This is the API for the AS5 Angle Sensor that uses CANOPEN to send and recieve
# messages from the angle sensor.
import time
import canopen
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

        # Initialize node in network with eds file.
        self.node = self.network.add_node(90,"as5-101.eds")
        self.sdoserver = self.node.sdo
        

    # Summary:
    #       Sends the doCal signal to the board to put the board in calibration mode.
    # Parameters:
    #
    # Returns:
    #
    def DoCal(self):
    # Summary:
    #       Calibrates the sensor for a specific axis.
    # Operations:
    # Send DOcal message,
    # If SdoCommunication Error, send Docal message again.
    # Bitmask check for which sides are calibrated, and update the side boolean.
    # if statusbits == ff: then set calbrationdone to True

        if self.calibrationdone: # If cal is already done
            msg_array = bytes([0x01]) # DoCal Message

            # Send the Docal Message
            while(1): # While loop to compensate for the inconsistency of it working
                try:
                    self.sdoserver.download(0x2003,0x04,msg_array) # to send msg to board
                    break
                except Exception as e:
                    # Note: Multiple errors possible. Sdocommunication error causes inconsistency
                    # if it doesn't work try again till no error.
                    print("This error occured while sending: ",e)
                    print("**TRYING AGAIN**")

            time.sleep(4)

            # Check the status bits
            # Make the bit mask to check for which axis has just been calibrated 
            try:
                self.statusbits = ((self.sdoserver[0x2003][0x04]).raw)
            except:
                raise Exception("Error: Status bit unable to be read")
                
            #  0     1     2     3     4     5     6     7
            #             Zdn   Zup   Ydn   Xdn   Yup   Xup
            #  1  |  1  |  0  |  0  |  0  |  0  |  0  |  0
            #     0b00000001 shift 0  Xup
            if   (0b00000001 & self.statusbits) == 1:
                self.Xaxisup = True
                print("X vector up calibrated ")
            #      0b00000010 shift 1  Yup
            elif ((0b00000010 & self.statusbits)>>1) == 1:
                self.Yaxisup = True
                print("Y vector up calibrated ")
            #      0b00000100 shift 2  Xdn
            elif ((0b00000100 & self.statusbits)>>2) == 1:
                self.Xaxisdown = True
                print("X vector down calibrated ")
            #      0b00001000 shift 3  Ydn
            elif ((0b00001000 & self.statusbits)>>3) == 1:
                self.Yaxisdown = True
                print("Y vector down calibrated ")
            #      0b00010000 shift 4  Zup
            elif ((0b00010000 & self.statusbits)>>4) == 1:
                self.Zaxisup = True
                print("Z vector up calibrated ")
            #      0b00100000 shift 5  Zdn
            elif ((0b00100000 & self.statusbits)>>5) == 1:
                self.Zaxisdown = True
                print("Z vector down calibrated ")
            else:
                if self.statusbits == 0b11111111: 
                    self.calibrationdone = True
                # or somehow no calibrations have been made (0b00000000)
            
        else:
            raise Exception("CALIBRATION ALREADY COMPLETE")
    #Return: potential could just return results string?

    


     
    #
    def calibrate(self,axis):
        if not self.calibrationInit:
            raise Exception("Intiaialize calibration first")

    # Summary:
    #       Obtains the axis specific angle data.
    # Parameters:
    #       axis: an that represents which axis to look at. 0 = x, 1 = y, 2 = z
    # Returns:
    #       double: the angle measurment.
    def getAngle(self,axis):
        subIndexes = [0x01,0x02,0x03]
        try:
            angle = (self.sdoserver[0x2004][subIndexes[axis]].raw) / 10.0
            return angle
        except: 
            raise Exception("Error Reading Angle from Sensor")

        
        

