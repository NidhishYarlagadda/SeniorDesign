# This is the API for the AS5 Angle Sensor that uses CANOPEN to send and recieve
# messages from the angle sensor.
import time
import canopen


class AS5():
###  AS5 object default constructor.
    
    def __init__(self, network): # initializes with network being passed
        self.Xaxisup = False
        self.Xaxisdown = False
        self.Yaxisdown = False
        self.Yaxisup  = False
        self.Zaxisdown = False
        self.Zaxisup = False
        self.network = network
        self.stat = 0

        # Initialize node in network with eds file.
        self.node = self.network.add_node(90,"as5-101.eds")
        self.sdoserver = self.node.sdo
        
        # need to check the status bits and set the calibrationdone and the statuses.
        self.stat = self.pullstat()

        if self.stat == 0b11111111:
            self.calibrationdone = True
            self.Xaxisup = True
            self.Xaxisdown = True
            self.Yaxisdown = True
            self.Yaxisup  = True
            self.Zaxisdown = True
            self.Zaxisup = True 
            self.newstatus = self.stat
            self.oldstatus = self.stat  
            print("***Sensor is calibrated as of initialization****")

        else:
##### if stat is not 0000 and there are some calibrations already done.
            self.calibrationdone = False
            self.newstatus = 0
            self.oldstatus = 0

    def pullstat(self):# pulls status bits from board.
            result = -1
            try:
                result = ((self.sdoserver[0x2003][0x04]).raw)
            except:
                print("Error: Status bit unable to be read")
            
            return result


################## Axis Booleans Calibrations #######################################
    def isXupcalibrated(self):
        return self.Xaxisup
    def isXdncalibrated(self):
        return self.Xaxisdown
    def isZupcalibrated(self):
        return self.Zaxisup
    def isZdncalibrated(self):
        return self.Zaxisdown
    def isYupcalibrated(self):
        return self.Yaxisup
    def isYdncalibrated(self):
        return self.Yaxisdown
    
    def getcalstatus(self):
        return self.stat
###################### DO CAL
    def DoCal(self):
    # Summary:
    #       Calibrates the sensor for a specific axis.
    # Operations:
    #   Send Docal message, to calibrate axis
    #   If SdoCommunication Error, send Docal message again.
    #   Bitmask check for which sides are calibrated, and update the side boolean.
    #   if statusbits == ff: then set calbrationdone to True

        if not self.calibrationdone: # If cal is already done
            msg_array = bytes([0x01]) # DoCal Message     
            print("In Docal")

############ PRE MSG : RETRIEVING THE OLD STATUS ################################
            self.oldstatus = self.pullstat()
            print("OLD STATUS: " + bin(self.oldstatus))

############ SENDING MSG ################################
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
            print("In Docal: Sent Message")
            # Check the status bits
            # Make the bit mask to check for which axis has just been calibrated 

############ POST MSG: RETRIEVING THE OLD STATUS ################################           
            self.newstatus = self.pullstat()
            self.stat = self.newstatus
            print("NEW STATUS: " + bin(self.newstatus))
############ 
            #  7     6     5     4     3     2     1     0
            #             Zdn   Zup   Ydn   Xdn   Yup   Xup
            #  1  |  1  |  0  |  0  |  0  |  0  |  0  |  0
            #     0b00000001 shift 0  Xup
            statusbits = self.newstatus >> 6 # isolates the bits 7 and 6 -
            check_axis = (self.newstatus ^ self.oldstatus) & 0b00111111  # Xor to isolate the modified axis(eliminated the status bits)
            

            if statusbits == 0b11: # if successful cal
                #  5     4     3     2     1     0    
                #  Zdn   Zup   Ydn   Xdn   Yup   Xup
                #  0  |  0  |  0  |  0  |  0  |  0
                    
                    if check_axis == 0:# Same side twice
                        print("You have calibrated this side already")
                    
                    
                    elif check_axis == 2**5: # 100000 -> Zdn
                        self.Zaxisdown = True
                        print("Z vector down calibrated ")  
                    
                    elif check_axis == 2**4: # 010000 -> Zup 16
                        self.Zaxisup = True
                        print("Z vector up calibrated ")       
                    
                    elif check_axis == 2**3: # 001000 -> Ydn
                        self.Yaxisdown = True
                        print("Y vector down calibrated ")   
                    
                    elif check_axis == 2**2: # 000100 -> Xdn
                        self.Xaxisdown = True
                        print("X vector down calibrated ")   
                    
                    elif check_axis == 2: # 000010 -> Yup
                        self.Yaxisup = True
                        print("Y vector up calibrated ")  
                    
                    elif check_axis == 1: # 000001 -> Xup 
                        self.Xaxisup = True
                        print("X vector up calibrated ")  

                    if self.newstatus == 0b11111111:
                        self.calibrationdone = True
                        print("**Sensor has now been fully calibrated**")
            elif statusbits == 0b01: # undefined
                print("ERROR: UNDEFINED")
            elif statusbits == 0b10: # Failed
                print("ERROR: CALIBRATION FAILED")

        else:
            print("CALIBRATION ALREADY COMPLETE")
            #raise Exception("CALIBRATION ALREADY COMPLETE")



######## GETTING ANGLE    
    def getAngle(self,axis):
        # Summary:
    #       Obtains the axis specific angle data.
    # Parameters:
    #       axis: an that represents which axis to look at. 0 = x, 1 = y, 2 = z
    # Returns:
    #       double: the angle measurment.
        if self.calibrationdone:
            subIndexes = [0x01,0x02,0x03]
            try:
                angle = (self.sdoserver[0x2004][subIndexes[axis]].raw) / 10.0
                return angle
            except: 
                raise Exception("Error Reading Angle from Sensor")
        else:
            raise Exception("Did not calibrate. Calibrate first")
        
        

