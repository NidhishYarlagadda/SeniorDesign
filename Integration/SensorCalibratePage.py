import tkinter as tk

class SCP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # 设置背景颜色
        self.configure(bg='Silver')

        # 添加“Calibrate Page”标签
        banner_frame = tk.Label(self, text="Calibrate Page", bg='DeepSkyBlue', justify='center', font=('bm jua', 35))
        banner_frame.pack(side='top', fill='x')

        logo = tk.Label(self, text="OEM Controls", font=('bm jua', 20), justify="left", bg="DeepSkyBlue", fg="White")
        logo.place(x=0, y=10)

        # Back按钮
        back_button = tk.Button(self, text='Back', bg='White', command=lambda: controller.show_home_page())
        back_button.pack(anchor='ne', padx=10, pady=0)

        # Start Calibration按钮
        calibrate_button = tk.Button(self, text='Start Six Side Calibration', font=('bm jua', 20), bg='lightgrey', fg='black', bd=1, command=self.create_calibration_buttons)
        calibrate_button.place(relx=0.5, rely=0.2, anchor="center")

        Emergency_Stop_button = tk.Button(self, text="STOP", bd = 3, font=('bm jua', 20), relief="groove", bg="Red", activebackground="Darkred", fg="white", command=self.test_function)
        Emergency_Stop_button.place(relx = 0.1, rely = 0.20, anchor = "center")

        

    def create_calibration_buttons(self):
        # 定义显示框的位置
        positions = [(0.2, 0.35), (0.5, 0.35), (0.8, 0.35), (0.2, 0.45), (0.5, 0.45), (0.8, 0.45)]
        directions = ['X Up', 'X Down', 'Y Up', 'Y Down', 'Z Up', 'Z Down']
    

        # 创建显示框
        self.labels = []
        for pos, direction in zip(positions, directions):
            label = tk.Label(self, text=direction, bg='grey', width=20, height=2)
            label.place(relx=pos[0], rely=pos[1], anchor='center')
            self.labels.append(label)
        
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
            print("AS5 ANGLE: ", arm.as5.getAngle(0))

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
