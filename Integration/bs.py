import tkinter as tk
from TestPage import TestPage
from SensorCalibratePage import SCP
from tkinter import PhotoImage
from tkinter import *
from PIL import ImageTk, Image
from tkinter import Tk, Frame, Label
from main_test import RobotMain, get_arm





# 主应用程序窗口定义
class MainApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('OEM Controls')  # 窗口标题
        self.geometry('900x700')  # 窗口大小，根据需要调整
#/home/tech/Desktop/bswithphoto/
        self.bg_image = ImageTk.PhotoImage(Image.open("/home/tech/Downloads/SeniorDesign/XArm/xarmAPI/xArm-Python-SDK/example/wrapper/xarm6/xarm-1.jpg"))
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 初始化页面
        self.sensor_calibrate_page = SCP(self, self)
        self.test_page = TestPage(self, self)

        # 添加标题
        self.title_label = tk.Label(self, text='Home Page', font=('bm jua', 30), fg='black',bg='white')
        self.title_label.pack(side='top', pady=150)

        # 创建按钮框架
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(expand=True)

        # 添加按钮
        self.add_button('Sensor Calibrate', 0, 0, self.show_sensor_calibrate_page)
        self.add_button('Test', 0, 1, self.show_test_page)

        # initiate the robot amd the as5
        arm = get_arm()
        self.robot_arm = RobotMain(arm)

    def add_button(self, text, row, column, command=None):
        button = tk.Button(self.buttons_frame, text=text, command=command)
        button.grid(row=row, column=column, padx=50, pady=30)
        button.config(width=20, height=3, font=('bm jua', '20'))
        self.update() 

    def show_sensor_calibrate_page(self):
        self.hide_home_page()
        self.sensor_calibrate_page.pack(fill="both", expand=True)
        self.update() 

    def show_test_page(self):
        self.hide_home_page()
        self.test_page.pack(fill="both", expand=True)
        self.update() 

    def show_home_page(self):
        self.sensor_calibrate_page.pack_forget()
        self.test_page.pack_forget()
        self.title_label.pack(side='top', pady=150)
        self.buttons_frame.pack(expand=True)
        self.update() 

    def hide_home_page(self):
        self.buttons_frame.pack_forget()
        self.title_label.pack_forget()
        self.update() 

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

