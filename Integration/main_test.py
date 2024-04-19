#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>
from as5 import AS5
import canopen
import time

# TODO
'''
    if one angle fails, break code (send message)
'''
"""
# Notice
#   1. Changes to this file on Studio will not be preserved
#   2. The next conversion will overwrite the file with the same name
# 
# xArm-Python-SDK: https://github.com/xArm-Developer/xArm-Python-SDK
#   1. git clone git@github.com:xArm-Developer/xArm-Python-SDK.git
#   2. cd xArm-Python-SDK
#   3. python setup.py install
"""
import sys
import math
import time
import queue
import datetime
import random
import traceback
import threading
from xarm import version
from xarm.wrapper import XArmAPI


class RobotMain(object):
    """Robot Main Class"""
    def __init__(self, robot, **kwargs):
        self.alive = True
        self._arm = robot
        self._ignore_exit_state = False
        self._tcp_speed = 50   # OG 100
        self._tcp_acc = 2000    # OG 2000
        self._angle_speed = 20  # OG 20
        self._angle_acc = 500   # OG 500
        self._vars = {}
        self._funcs = {}
        ####### AS5 OBJECT CREATION
        network = canopen.Network()
        #Hardcoding which channel to use
        network.connect(bustype='pcan', channel= 'PCAN_USBBUS1', bitrate= 125000)
        self.as5 = AS5(network)

        self._robot_init()

        #TO DO:
        # MERGE SENSOR API WITH THIS > Composition
        # Create the instance of the Angle sensor here
        # Then make Methods recalling the as5 methods.


    # Robot init
    def _robot_init(self):
        self._arm.clean_warn()
        self._arm.clean_error()
        self._arm.motion_enable(True)
        self._arm.set_mode(0)
        self._arm.set_state(0)
        time.sleep(1)
        self._arm.register_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.register_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'register_count_changed_callback'):
            self._arm.register_count_changed_callback(self._count_changed_callback)

    # Register error/warn changed callback
    def _error_warn_changed_callback(self, data):
        if data and data['error_code'] != 0:
            self.alive = False
            self.pprint('err={}, quit'.format(data['error_code']))
            self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)

    # Register state changed callback
    def _state_changed_callback(self, data):
        if not self._ignore_exit_state and data and data['state'] == 4:
            self.alive = False
            self.pprint('state=4, quit')
            self._arm.release_state_changed_callback(self._state_changed_callback)

    # Register count changed callback
    def _count_changed_callback(self, data):
        if self.is_alive:
            self.pprint('counter val: {}'.format(data['count']))

    def _check_code(self, code, label):
        if not self.is_alive or code != 0:
            self.alive = False
            ret1 = self._arm.get_state()
            ret2 = self._arm.get_err_warn_code()
            self.pprint('{}, code={}, connected={}, state={}, error={}, ret1={}. ret2={}'.format(label, code, self._arm.connected, self._arm.state, self._arm.error_code, ret1, ret2))
        return self.is_alive

    @staticmethod
    def pprint(*args, **kwargs):
        try:
            stack_tuple = traceback.extract_stack(limit=2)[0]
            print('[{}][{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1], ' '.join(map(str, args))))
        except:
            print(*args, **kwargs)

    @property
    def arm(self):
        return self._arm

    @property
    def VARS(self):
        return self._vars

    @property
    def FUNCS(self):
        return self._funcs

    @property
    def is_alive(self):
        if self.alive and self._arm.connected and self._arm.error_code == 0:
            if self._ignore_exit_state:
                return True
            if self._arm.state == 5:
                cnt = 0
                while self._arm.state == 5 and cnt < 5:
                    cnt += 1
                    time.sleep(0.1)
            return self._arm.state < 4
        else:
            return False

    # Robot Main Run
    def run(self):
        try:
            # Joint Motion
            self._angle_speed = 40
            self._angle_acc = 100
            for i in range(int(1)):
                if not self.is_alive:
                    break
                t1 = time.monotonic()

                # NEGATIVE Z-AXIS0
                print("Negative z-axis Test")

                # set arm to initial position
                initial_pos = self._arm.get_initial_point()[1]
                code = self._arm.set_servo_angle(angle=initial_pos, wait=True)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                
                # set arm to test start position (-80 degrees)
                code = self._arm.set_position(x=0,y=0,z=0,roll=0,pitch=0,yaw=-80, relative=True, is_radian=False, wait=True)
                if not self._check_code(code, 'set_position'):
                    return

                # iterate through all angles in the z-axis rotation
                yaw_ct = -80
                while(yaw_ct <= 80):
                    # send angle to frontend (TODO)
                    
                    # wait for backend to receive inpput from AS5 (TODO)

                    # rotate the arm 5 degrees more
                    code = self._arm.set_position(x=0,y=0,z=0,roll=0,pitch=0,yaw=10, relative=True, is_radian=False, wait=True)
                
                    if not self._check_code(code, 'set_position'):
                        return
                    print("Angle ", yaw_ct, " done!")
                    yaw_ct += 10

                # set arm to initial position
                initial_pos = self._arm.get_initial_point()[1]
                code = self._arm.set_servo_angle(angle=initial_pos, wait=True, speed=self._angle_speed)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                print("Back to initial position!")

                # set interval for wait time
                interval = time.monotonic() - t1
                if interval < 0.01:
                    time.sleep(0.01 - interval)

                # POSITIVE Z-AXIS
                print("Positive z-axis Test")

                # set the arm to face positive z-axis
                code = self._arm.set_position(x=0,y=0,z=0,roll=180,pitch=0,yaw=0, relative=True, is_radian=False, wait=True, speed=30)
                if not self._check_code(code, 'set_position'):
                    return
                
                # iterate through all angles in the z-axis rotation
                yaw_ct = -80
                while(yaw_ct <= 80):
                    # send angle to frontend (TODO)
                    
                    # wait for backend to receive inpput from AS5 (TODO)

                    # rotate the arm 5 degrees more
                    code = self._arm.set_position(x=0,y=0,z=0,roll=0,pitch=0,yaw=10, relative=True, is_radian=False, wait=True)
                
                    if not self._check_code(code, 'set_position'):
                        return
                    print("Angle ", yaw_ct, " done!")
                    yaw_ct += 10

                # set arm to initial position
                initial_pos = self._arm.get_initial_point()[1]
                code = self._arm.set_servo_angle(angle=initial_pos, wait=True, speed=self._angle_speed)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                print("Back to initial position!")

                # set interval for wait time
                interval = time.monotonic() - t1
                if interval < 0.01:
                    time.sleep(0.01 - interval)

        except Exception as e:
            self.pprint('MainException: {}'.format(e))
        finally:
            self.alive = False
            self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)
            self._arm.release_state_changed_callback(self._state_changed_callback)
            if hasattr(self._arm, 'release_count_changed_callback'):
                self._arm.release_count_changed_callback(self._count_changed_callback)
    
    def angleTest(self):
        try:
            # Joint Motion
            self._angle_speed = 20
            self._angle_acc = 20
            speed = 10
            for i in range(int(1)):
                if not self.is_alive:
                    break
                t1 = time.monotonic()
            initial_pos = self._arm.get_initial_point()[1]
        # -----------------Angle Testing-------------------------
            print("Angle Testing")
            angle = -90
            angleTest = True
            failedCounter = 0
            while(angle <= 90 and failedCounter < 3):
                print("Testing ", angle, " degree")
                code = self._arm.set_servo_angle(angle = [0,0,0,0,-90,angle], wait=True, speed = speed)
                if not self._check_code(code, 'set_position'):
                    return
                if(self.as5.getAngle(axis = 2) == angle):
                    print(f'Angle {angle} Passed')
                    angle += 5
                    failedCounter = 0
                else:
                    failedCounter += 1

                
                # call AS5 angle function (if error stop)
                #if(sensor angle == angle): continue else: angleTest = False store angle and break
                #perhaps we consider using yield and yield each angle then the failed angle is already displayed because its no longer increasing

            print("Load Position")
            code = self._arm.set_servo_angle(angle = [0,0,0,0,-90,0], wait=True, speed = speed)
            if not self._check_code(code, 'set_position'):
                return

            #if angleTest == False: return failed angle else: return Pass

        except Exception as e:
            print('MainException: {}'.format(e))
        finally:
            self.alive = False
            self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)
            self._arm.release_state_changed_callback(self._state_changed_callback)
            if hasattr(self._arm, 'release_count_changed_callback'):
                self._arm.release_count_changed_callback(self._count_changed_callback)

    def calibrate(self):
        try:
            # Joint Motion
            self._angle_speed = 10
            self._angle_acc = 10
            speed = 10
            for i in range(int(1)):
                if not self.is_alive:
                    break
                t1 = time.monotonic()
            initial_pos = self._arm.get_initial_point()[1]                
            # ----------------- -180 Degree Check -------------------------
            print("-180 Degree Check")
            code = self._arm.set_servo_angle(angle = [0,0,0,0,-90,-180], wait=True, speed = speed)
            if not self._check_code(code, 'set_position'):
                return
            # call AS5 calibration function (if error stop)
            #if(planes are equal): continue else: return Failed 
            # call AS5 angle function (if error stop)
            #if(sensor angle == angle): continue else: return Failed 

            # ----------------- -90 Degree Check Test -------------------------
            print("-90 Degree Check")
            code = self._arm.set_servo_angle(angle = [0,0,0,0,-90,-90], wait=True, speed = speed)
            if not self._check_code(code, 'set_position'):
                return
            # call AS5 angle function (if error stop)
            #if(sensor angle == angle): continue else: return Failed 

            # ----------------- 0 Degree Check Test -------------------------
            print("0 Degree Check")
            code = self._arm.set_servo_angle(angle = [0,0,0,0,-90,0], wait=True, speed = speed)
            if not self._check_code(code, 'set_position'):
                return
            # call AS5 angle function (if error stop)
            #if(sensor angle == angle): continue else: return Failed 

            # ----------------- 90 Degree Check Test -------------------------
            print("0 Degree Check")
            code = self._arm.set_servo_angle(angle = [0,0,0,0,-90,90], wait=True, speed = speed)
            if not self._check_code(code, 'set_position'):
                return
            # call AS5 angle function (if error stop)
            #if(sensor angle == angle): continue else: return Failed 

            # NEGATIVE Z-AXIS
            print("Negative z-axis Test")

            code = self._arm.set_servo_angle(angle=initial_pos, wait=True)
            if not self._check_code(code, 'set_position'):
                return   
            # call AS5 calibration function (if error stop)
            #if(planes are equal): continue else: return Failed 

            # ----------------- POSITIVE Z-AXIS -------------------------
            print("Positive z-axis Test")
            
            code = self._arm.set_position(x=0,y=0,z=0,roll=-180,pitch=0,yaw=0, relative=True, is_radian=False, wait=True, speed=speed)
            #rough estimate might need a better way of doing, but minimal movement and no jerking
            #code = self._arm.set_servo_angle(angle = [0,15.7,-14.7,90,180,0], wait=True, speed = 10)
            # set the arm to face positive z-axis
            if not self._check_code(code, 'set_position'):
                return

            # call AS5 calibration function (if error stop)
            #if(planes are equal): continue else: return Failed 

            # Back to Load Position
            print("Load Position")
            code = self._arm.set_servo_angle(angle = [0,0,0,0,-90,0], wait=True, speed = speed)
            if not self._check_code(code, 'set_position'):
                return
            #return success

        except Exception as e:
            self.print('MainException: {}'.format(e))
        finally:
            self.alive = False
            self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)
            self._arm.release_state_changed_callback(self._state_changed_callback)
            if hasattr(self._arm, 'release_count_changed_callback'):
                self._arm.release_count_changed_callback(self._count_changed_callback)

    def emergency_stop(self):
        self.emergency_stop()
        return True

    def calibrate_zDN(self):
        #### ----------------- Z-AXIS DOWN -------------------------
        print("Z-axis Down Test")

        # set arm to negative z-axis
        initial_pos = self._arm.get_initial_point()[1]
        code = self._arm.set_servo_angle(angle=initial_pos, wait=True)
        if not self._check_code(code, 'set_servo_angle'):
            return False
        #print("*****Going to Sleep")
        #time.sleep(5)
        # call AS5 calibration function (if error try again)
        self.as5.DoCal()

        response = self.as5.isZdncalibrated()
        if not response:
            print("Z down did not calibrate")
            return False
        else:
            print("Success!")
            return True

    def calibrate_zUP(self):
# ----------------- Z-AXIS UP -------------------------
        print("Z-axis Up Test")

        code = self._arm.set_servo_angle(angle=[0.0, 0.0, -90.0, 0.0, -90.0, 0.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return False
        
        # set the arm to face positive z-axis
        code = self._arm.set_position(x=316,y=-2.9,z=724.2,roll=0,pitch=0,yaw=180, relative=False, is_radian=False, wait=True, speed=30)
        if not self._check_code(code, 'set_position'):
            return False
        #print("*****Going to Sleep")
        #time.sleep(5)

        # call AS5 calibration function (if error try again)
        self.as5.DoCal()

        response = self.as5.isZupcalibrated()
        if not response:
            print("Z up did not calibrate")
            return False
        else:
            print("Success!")
            return True

    def calibrate_xDN(self):
    #### ----------------- X-AXIS DOWN -------------------------
        print("X-axis Down Test")

        # set the arm to face positive z-axis
        code = self._arm.set_servo_angle(angle=[0,0,0,0,-90,0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        if not self._check_code(code, 'set_servo_angle'):
            return False
        
        code = self._arm.set_position(x=224.3, y=-1.4, z=287.6, roll=-90, pitch=-90, yaw=-90, relative=False, is_radian=False, wait=True, speed=30)
        if not self._check_code(code, 'set_position'):
            return False
        
        #print("*****Going to Sleep")
        #time.sleep(5)

        # call AS5 calibration function (if error try again)
        self.as5.DoCal()

        response = self.as5.isXdncalibrated()
        if not response:
            print("X down did not calibrate")
            return False
        else:
            print("Success!")
            return True

    def calibrate_yUP(self):
#### ----------------- Y-AXIS UP -------------------------
        print("Y-AXIS UP  Test")

        # set the arm to face positive z-axis
        code = self._arm.set_servo_angle(angle=[0,0,0,0,-90,90], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
        if not self._check_code(code, 'set_position'):
            return False
        
        #print("*****Going to Sleep")
        #time.sleep(5)

        # call AS5 calibration function (if error try again)
        self.as5.DoCal()

        response = self.as5.isYupcalibrated()
        if not response:
            print("Y up did not calibrate")
            return False
        else:
            print("Success!")
            return True

    def calibrate_xUP(self):
#### ----------------- X-AXIS UP -------------------------
        print("X-AXIS UP Test")

        # set the arm to face positive z-axis
        code = self._arm.set_servo_angle(angle=[0,0,0,0,-90, 180], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
        if not self._check_code(code, 'set_position'):
            return False
        
        #print("*****Going to Sleep")
        #time.sleep(5)

        # call AS5 calibration function (if error try again)
        self.as5.DoCal()

        response = self.as5.isXupcalibrated()
        if not response:
            print("X up did not calibrate")
            return False
        else:
            print("Success!")
            return True

    def calibrate_yDN(self):
#### ----------------- Y-AXIS DOWN -------------------------
        print("Y-AXIS DOWN Test")

        # set the arm to face positive z-axis
        code = self._arm.set_servo_angle(angle=[0,0,0,0,-90, 270], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
        if not self._check_code(code, 'set_position'):
            return False
        
        #print("*****Going to Sleep")
        #time.sleep(5)

        # call AS5 calibration function (if error try again)
        self.as5.DoCal()

        response = self.as5.isXupcalibrated()
        if not response:
            print("Y down did not calibrate")
            return False
        else:
            print("Success!")
            return True

    def calibration(self): #TO DO: REMOVE THE AS5 instance here.
        try:
            '''
                go through all movements and for each movement call the AS5 function
            '''

            ####### AS5 OBJECT CREATION
            network = canopen.Network()
            # Hardcoding which channel to use
            network.connect(bustype='pcan', channel= 'PCAN_USBBUS1', bitrate= 125000)

            as5 = AS5(network)

#### ----------------- Z-AXIS DOWN -------------------------
            print("Z-axis Down Test")

            # set arm to negative z-axis
            initial_pos = self._arm.get_initial_point()[1]
            code = self._arm.set_servo_angle(angle=initial_pos, wait=True)
            if not self._check_code(code, 'set_servo_angle'):
                return
            print("*****Going to Sleep")
            time.sleep(5)
            # call AS5 calibration function (if error try again)
            as5.DoCal()

            response = as5.isZdncalibrated()
            if not response:
                print("Z down did not calibrate")
                #return
            else:
                print("Success!")

# ----------------- Z-AXIS UP -------------------------
            print("Z-axis Up Test")

            code = self._arm.set_servo_angle(angle=[0.0, 0.0, -90.0, 0.0, -90.0, 0.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            
            # set the arm to face positive z-axis
            code = self._arm.set_position(x=316,y=-2.9,z=724.2,roll=0,pitch=0,yaw=180, relative=False, is_radian=False, wait=True, speed=30)
            if not self._check_code(code, 'set_position'):
                return
            print("*****Going to Sleep")
            time.sleep(5)

            # call AS5 calibration function (if error try again)
            as5.DoCal()

            response = as5.isZupcalibrated()
            if not response:
                print("Z up did not calibrate")
                #return
            else:
                print("Success!")

#### ----------------- X-AXIS DOWN -------------------------
            print("X-axis Down Test")

            # set the arm to face positive z-axis
            code = self._arm.set_servo_angle(angle=[0,0,0,0,-90,0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            
            code = self._arm.set_position(x=224.3, y=-1.4, z=287.6, roll=-90, pitch=-90, yaw=-90, relative=False, is_radian=False, wait=True, speed=30)
            if not self._check_code(code, 'set_position'):
                return
            
            print("*****Going to Sleep")
            time.sleep(5)

            # call AS5 calibration function (if error try again)
            as5.DoCal()

            response = as5.isXdncalibrated()
            if not response:
                print("X down did not calibrate")
            else:
                print("Success!")

    
#### ----------------- Y-AXIS UP -------------------------
            print("Y-AXIS UP  Test")

            # set the arm to face positive z-axis
            code = self._arm.set_servo_angle(angle=[0,0,0,0,-90,90], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_position'):
                return
            
            print("*****Going to Sleep")
            time.sleep(5)

            # call AS5 calibration function (if error try again)
            as5.DoCal()

            response = as5.isYupcalibrated()
            if not response:
                print("Y up did not calibrate")
            else:
                print("Success!")

#### ----------------- X-AXIS UP -------------------------
            print("X-AXIS UP Test")

            # set the arm to face positive z-axis
            code = self._arm.set_servo_angle(angle=[0,0,0,0,-90, 180], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_position'):
                return
            
            print("*****Going to Sleep")
            time.sleep(5)

            # call AS5 calibration function (if error try again)
            as5.DoCal()

            response = as5.isXupcalibrated()
            if not response:
                print("X up did not calibrate")
            else:
                print("Success!")

#### ----------------- Y-AXIS DOWN -------------------------
            print("Y-AXIS DOWN Test")

            # set the arm to face positive z-axis
            code = self._arm.set_servo_angle(angle=[0,0,0,0,-90, 270], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_position'):
                return
            
            print("*****Going to Sleep")
            time.sleep(5)

            # call AS5 calibration function (if error try again)
            as5.DoCal()

            response = as5.isXupcalibrated()
            if not response:
                print("Y down did not calibrate")
            else:
                print("Success!")

            network.disconnect()

        except Exception as e:
            self.pprint('MainException: {}'.format(e))
        finally:
            self.alive = False
            self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)
            self._arm.release_state_changed_callback(self._state_changed_callback)
            if hasattr(self._arm, 'release_count_changed_callback'):
                self._arm.release_count_changed_callback(self._count_changed_callback)

    def test_frontend(self):
        # set to initial position
        initial_pos = self._arm.get_initial_point()[1]
        code = self._arm.set_servo_angle(angle=initial_pos, wait=True)

        # move the arm
        code = self._arm.set_servo_angle(angle=[0,0,-90,0,0,0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
        
        # go back to initial position
        code = self._arm.set_servo_angle(angle=initial_pos, wait=True)

    def get_angle(self):
        return self._arm.get_servo_angle(servo_id=6)

    def move_to_angle(self, angle):
        code = self._arm.set_servo_angle(angle = [0,0,0,0,-90,angle],speed=self._angle_speed, wait=True)

def get_arm():
    return XArmAPI('192.168.1.214', baud_checkset=False, is_radian=False)

if __name__ == '__main__':
    #TO DO:
        # MERGE SENSOR API WITH THIS > Composition
        # Create the instance of the Angle sensor here
        # Then make Methods recalling the as5 methods.
    RobotMain.pprint('xArm-Python-SDK Version:{}'.format(version.__version__))
    arm = XArmAPI('192.168.1.214', baud_checkset=False, is_radian=False)
    robot_main = RobotMain(arm)
    #robot_main.calibrate_zDN()
    robot_main.calibration()
    #robot_main.calibrate()
    #robot_main.angleTest()
    arm.reset(wait=True)
    arm.disconnect()

    #TO DO:
    # Implement the calibration integration.

