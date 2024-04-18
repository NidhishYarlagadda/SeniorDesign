import tkinter as tk
import time

#TO DO: MAKE THE ROBOT GO TO ORIGINAL POSITION AFTER CALIBRATION
class SCP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.test_stage = 0
        self.configure(bg='Silver')
        banner_frame = tk.Label(self, text="Calibrate Page", bg='DeepSkyBlue', justify='center', font=('bm jua', 35))
        banner_frame.pack(side='top', fill='x')

        logo = tk.Label(self, text="OEM Controls", font=('bm jua', 20), justify="left", bg="DeepSkyBlue", fg="White")
        logo.place(x=0, y=10)

        back_button = tk.Button(self, text='Back', bg='White', command=lambda: controller.show_home_page())
        back_button.pack(anchor='ne', padx=10, pady=0)

        # Start Calibration按钮
        calibrate_button = tk.Button(self, text='Start Six Side Calibration', font=('bm jua', 20), bg='lightgrey', fg='black', bd=1, command=self.start_calibration)
        calibrate_button.place(relx=0.5, rely=0.2, anchor="center")

        # 周期性操作控制
        self.running = True

        Emergency_Stop_button = tk.Button(self, text="STOP", bd=3, font=('bm jua', 20), relief="groove", bg="Red", activebackground="Darkred", fg="white", command=self.stop_tests)
        Emergency_Stop_button.place(relx=0.1, rely=0.20, anchor="center")

        self.create_calibration_buttons()
        
    def start_calibration(self):
        if self.running:
            self.test_stage += 1
            if self.test_stage > 6:
                self.test_stage = 1  # Reset back to X after Z

            arm = self.controller.robot_arm

            if not arm.as5.calibrationdone:
                print("Arm instance: ", arm)
                test_results = [arm.calibrate_zDN()]
                print("Z Down boolean:",test_results[0])
                #test_results = [True] if self.test_stage == 1 else [False]
                self.update_label_color(test_results,5)

                test_results = [arm.calibrate_zUP()]
                print("Z Up boolean:", test_results[0])
                #test_results = [True] if self.test_stage == 1 else [False]
                self.after(2000, self.update_label_color(test_results,4))

                test_results = [arm.calibrate_xDN()]
                print("X Down boolean:",test_results[0])
                #test_results = [True] if self.test_stage == 1 else [False]
                self.update_label_color(test_results,1)
                self.after(2000, self.update_label_color(test_results,1))

                test_results = [arm.calibrate_yUP()]
                print("Y Up boolean:",test_results[0])
                #test_results = [True] if self.test_stage == 1 else [False]
                self.update_label_color(test_results,2)
                self.after(2000, self.update_label_color(test_results,2))

                test_results = [arm.calibrate_xUP()]
                print("X Up boolean:",test_results[0])
                #test_results = [True] if self.test_stage == 1 else [False]
                self.update_label_color(test_results,0)
                self.after(2000, self.update_label_color(test_results,0))

                test_results = [arm.calibrate_yDN()]
                print("Y Down boolean:",test_results[0])
                #test_results = [True] if self.test_stage == 1 else [False]
                self.update_label_color(test_results,3)
                self.after(2000, self.update_label_color(test_results,3))

                # Schedule the next call
                #self.after(2000, self.start_calibration)  # call every 2 seconds
            else:
                print("AS5 ANGLE: ", arm.as5.getAngle(0))
                test_results = [True,True,True,True,True,True] if self.test_stage == 1 else [False,False,False,False,False,False]
                self.update_label_color(test_results,-1)

            # Schedule the next call
                #self.after(2000, self.start_calibration)  # call every 2 seconds

            
        
    def create_calibration_buttons(self):
        positions = [(0.2, 0.35), (0.5, 0.35), (0.8, 0.35), (0.2, 0.45), (0.5, 0.45), (0.8, 0.45)]
        directions = ['X Up', 'X Down', 'Y Up', 'Y Down', 'Z Up', 'Z Down']
        self.labels = []
        for pos, direction in zip(positions, directions):
            label = tk.Label(self, text=direction, bg='grey', width=20, height=2)
            label.place(relx=pos[0], rely=pos[1], anchor='center')
            self.labels.append(label)


    def update_label_color(self,statuses,place):
        index = (self.test_stage - 1)
        print("***In update label color")
        print("Status: ", statuses)
        print("Place: ",place)
        if len(statuses) == 1:
            if statuses[0]:
                    self.labels[place].config(bg='green')# Not changing to green
                

            else:
                    self.labels[place].config(bg='red')
        else:
            for i in range(6):
                if statuses[i]:
                    self.labels[index + i].config(bg='green')
                else:
                    self.labels[index + i].config(bg='red')

    def stop_tests(self):
        self.running = False
        print("Calibration stopped")           
 

    def test_function(self):
        arm = self.controller.robot_arm
        print("Arm instance: ", arm)

# 模拟的主控制器类，用于演示
class MainController:
    def show_home_page(self):
        print("Back to home page")


# 以下代码仅用于演示和测试，实际使用时应该嵌入到你的应用程序中
if __name__ == "__main__":
    root = tk.Tk()
    main_frame = SCP(parent=root, controller=MainController())
    main_frame.pack(fill='both', expand=True)
    root.mainloop()


'''

import tkinter as tk

class SCP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.test_stage = 0
        self.configure(bg='Silver')
        banner_frame = tk.Label(self, text="Calibrate Page", bg='DeepSkyBlue', justify='center', font=('bm jua', 35))
        banner_frame.pack(side='top', fill='x')

        logo = tk.Label(self, text="OEM Controls", font=('bm jua', 20), justify="left", bg="DeepSkyBlue", fg="White")
        logo.place(x=0, y=10)

        back_button = tk.Button(self, text='Back', bg='White', command=lambda: controller.show_home_page())
        back_button.pack(anchor='ne', padx=10, pady=0)

        # Start Calibration按钮
        calibrate_button = tk.Button(self, text='Start Six Side Calibration', font=('bm jua', 20), bg='lightgrey', fg='black', bd=1, command=self.start_calibration)
        calibrate_button.place(relx=0.5, rely=0.2, anchor="center")

        self.create_calibration_buttons()

        Emergency_Stop_button = tk.Button(self, text="STOP", bd=3, font=('bm jua', 20), relief="groove", bg="Red", activebackground="Darkred", fg="white", command=self.stop_tests)
        Emergency_Stop_button.place(relx=0.1, rely=0.20, anchor="center")

    def start_calibration(self):
        self.test_stage = 0  # Ensure we start from the beginning
        self.run_single_test()

    def run_single_test(self):
        if self.test_stage >= 6:
            return  # Stop if all tests are done

        arm = self.controller.robot_arm
        test_functions = [
            arm.calibrate_xUP,
            arm.calibrate_xDN,
            arm.calibrate_yUP,
            arm.calibrate_yDN,
            arm.calibrate_zUP,
            arm.calibrate_zDN
        ]
        result = test_functions[self.test_stage]()
        print(f"Test {self.test_stage + 1} result: {result}")
        self.update_label_color([result], self.test_stage)

        self.test_stage += 1  # Move to next test stage

        # Schedule the next test after 2 seconds
        if self.test_stage < 6:
            self.after(2000, self.run_single_test)

    def create_calibration_buttons(self):
        positions = [(0.2, 0.35), (0.5, 0.35), (0.8, 0.35), (0.2, 0.45), (0.5, 0.45), (0.8, 0.45)]
        directions = ['X Up', 'X Down', 'Y Up', 'Y Down', 'Z Up', 'Z Down']
        self.labels = []
        for pos, direction in zip(positions, directions):
            label = tk.Label(self, text=direction, bg='grey', width=20, height=2)
            label.place(relx=pos[0], rely=pos[1], anchor='center')
            self.labels.append(label)

    def update_label_color(self, statuses, place):
        color = 'green' if statuses[0] else 'red'
        self.labels[place].config(bg=color)

    def stop_tests(self):
        self.test_stage = 6  # Setting this high to stop the testing loop
        print("Calibration stopped")

# 模拟的主控制器类，用于演示
class MainController:
    def show_home_page(self):
        print("Back to home page")

# Application execution
if __name__ == "__main__":
    root = tk.Tk()
    main_frame = SCP(parent=root, controller=MainController())
    main_frame.pack(fill='both', expand=True)
    root.mainloop()'''
