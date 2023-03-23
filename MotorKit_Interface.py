'''
Motor Kit Controller
Contributors: Gage Gunn

RRCC/ACC Rocksat-X 2023
This file will control all motor function including throttle speed

'''

### Libraries ###
import time
from adafruit_motorkit import MotorKit

class ThrottleController:
    def __init__(self):
        self.kit = MotorKit()

    # def set_speed(self, speed):
    #     if speed > 0:
    #         speed = 1.0
    #     elif speed < 0:
    #         speed = -1.0
    #     elif speed == 0:
    #         speed = 0
    #     self.kit.motor1.throttle = speed

    def throttle_high(self): #Throttle up
        throttle_high = 1
        self.kit.motor1.throttle = throttle_high
        return throttle_high
    
    def throttle_low(self): #Throttle low
        throttle_low = -1
        self.kit.motor1.throttle = throttle_low
        return throttle_low
    
    def throttle_off(self): #Throttle off
        throttle_off = 0
        self.kit.motor1.throttle = throttle_off
        return throttle_off


