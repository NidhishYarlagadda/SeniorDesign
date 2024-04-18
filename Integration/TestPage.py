import tkinter as tk
import subprocess
import main_test
import csv
import os
from datetime import datetime

# TO DO: 
# IT SAVES AS A PLAIN DOCUMENT NOT A CSV.
# 
#/home/tech/Downloads/SeniorDesign/XArm/xarmAPI/xArm-Python-SDK/example/wrapper/xarm6/TestPage.py

# imports
from main_test import RobotMain, get_arm

RESULTS_DIRPATH = os.path.join(os.getcwd(), "results/")

class TestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Test Page", font=('bm jua', 35), justify='center', bg="DeepSkyBlue")
        label.pack(side="top", fill='x')

        logo = tk.Label(self, text = "OEM Controls", font=('bm jua', 20), justify = "left", bg="DeepSkyBlue" ,fg="White")
        logo.place(x=0, y=10)

        back_button = tk.Button(self, text='Back', bg='White', command=lambda: controller.show_home_page())
        back_button.pack(anchor='ne', padx=10, pady=0)
       
        Emergency_Stop_button = tk.Button(self, text="STOP", bd = 3, font=('bm jua', 20), relief="groove", bg="Red", activebackground="Darkred", fg="white")
        Emergency_Stop_button.place(relx = 0.1, rely = 0.2, anchor = "center")
        
        buttons = ["Start", "Reset"]
        i = 1
        w = 0.25
        for t in buttons:
            if t == "Start":
                # bt = tk.Button(self, text=t, bd = 4, font=('bm jua', 20), relief="groove", bg="Silver", activebackground = "DarkGray",command = self.run_main_test)
                bt = tk.Button(self, text=t, bd = 4, font=('bm jua', 20), relief="groove", bg="Silver", activebackground = "DarkGray",command = self.run_testfunction)

            else:

                bt = tk.Button(self, text=t, bd = 4, font=('bm jua', 20), relief="groove", bg="Silver", activebackground = "DarkGray")
            bt.place(relx = i*1.3*w, width = 120, height= 80, rely = 0.25, anchor='center')
            i+=1


        LogF = tk.Frame(self, bg='White', height = 350, width = 600)
        LogF.place(relx = 0.4, rely = 0.7, anchor = "center")

        i = 1
        labels = ["X: __", "Y: __", "Z: __"]
        for t in labels:
            lb = tk.Label(LogF, text = t, font=('bm jua', 15), justify= "left", bg = "White")
            lb.place(relx = 0.2, rely = i*w, anchor="center" )
            Error = tk.Label(LogF, text = "Error: __", font=('bm jua', 20), justify= "left", bg = "White")
            Error.place(relx = 0.7, rely = i*w, anchor="center")
            i+=1
    def run_main_test(self):
        subprocess.run (["python3","main_test.py"])


   # def send_stop_signal(self):
        #with open("stop_signal.txt","w") as file:
            #file.write("stop")
       # print("Stopping")

    

# This function runs a test function in main_test.py that moves the robot arm up and down
    def run_testfunction(self):
        # get the xarm object from main_test.py
        #arm = get_arm()
        # initialize a RobotMain object (this class has all the functions we need)
        #robot_main = RobotMain(arm)
        # test_frontend is a dummy function just for testing connection with the GUI
        #robot_main.test_frontend()
        # after function is done, we reset and disconnect from the robot arm
        #arm.reset(wait=True)
        #arm.disconnect()
        # CURRENTLY: the angle sensor controls the robot live. and returns values
        # TO DO: Do the opposite(for lonop 5 degree increment)
        # Emergency stop: arm.set_state(state=4) - check to see if it emergency stops.
        arm = self.controller.robot_arm
        if not arm.as5.calibrationdone:
            print("Arm instance: ", arm)
            print("Z Down boolean:",arm.calibrate_zDN())
            print("Z Up boolean:",arm.calibrate_zUP())
            print("X Down boolean:",arm.calibrate_xDN())
            print("Y Up boolean:",arm.calibrate_yUP())
            print("X Up boolean:",arm.calibrate_xUP())
            print("Y Down boolean:",arm.calibrate_yDN())
        else:
            #while(1):
             #   print("AS5 ANGLE: ", arm.as5.getAngle(0))
              #  print("XARM ANGLE: ", arm.get_angle())

                #angle += 5
              #  angle = arm.as5.getAngle(0)
              #  move  = arm.move_to_angle(angle)
            arm.move_to_angle(0)
            result_list = []
            for angle in range(-90, 95, 5):
                arm.move_to_angle(angle)
                print("Ref Angle: ", angle)
                test_angle = arm.as5.getAngle(0)
                print("Test Angle:",test_angle)
                difference = abs(angle - test_angle)
                result =  difference <= 0.4
                result_list.append([angle,test_angle,difference,result])
                
                if not result: 
                    print("Test Failed: Sensor not Correct")
                    print("Result List:",result_list)
                    break
            fields = ['Angle', 'Test Angle', 'Difference', 'Results']
            self.createFile(fields, result_list)
            arm.move_to_angle(0)

    def createFile(self, fields, results):
        if not os.path.isdir(RESULTS_DIRPATH):
            os.mkdir(RESULTS_DIRPATH)
        
        fileName = datetime.now().strftime("%Y_%m_%d-%I_%M_%S")
        filePath = os.path.join(RESULTS_DIRPATH, fileName)

        with open(filePath, 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter='|')
            csvWriter.writerow(fields)
            csvWriter.writerows(results)
    
    






                



                
                


        

    





