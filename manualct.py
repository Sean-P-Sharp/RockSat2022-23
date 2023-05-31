"""
    manualctl.py
        Manual control over camera and motor.
"""

import configparser
import code
import time

# RPi GPIO
import RPi.GPIO as GPIO
import busio
import board

# MotorKit
from adafruit_motorkit import MotorKit

def main():
    # Shorthand functions for conditions
    def armExtended(): return GPIO.input(EXTEND_LIMIT) == 1
    def armRetracted(): return GPIO.input(RETRACT_LIMIT) == 1

    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('./config.ini')

    # Configure MotorKit
    motorKit = MotorKit(i2c=busio.I2C(board.SCL, board.SDA))
    arm = motorKit.motor1
    arm.throttle = 0 # Reset motor

    CAMERA = int(config['Camera Control']['CAMERA'])            # Camera Control

    def f():
        arm.throttle = 1
    def r():
        arm.throttle = -1
    def s():
        arm.throttle = 0

    # Camera Control
    def toggleRecord():
        GPIO.output(CAMERA, GPIO.HIGH)
        time.sleep(1.25)
        GPIO.output(CAMERA, GPIO.LOW)

    code.interact(locals=locals())

if "__name__" == __main__:
    main()
