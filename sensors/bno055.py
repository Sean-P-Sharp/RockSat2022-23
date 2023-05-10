"""
    BNO055.py
        Absolute Orientation Sensor
"""

# Base RockSatSensor Class
from sensors import RockSatSensor

# Adafruit Library for the BNO055
import adafruit_bno055

# BNO055 Object
class BNO055(RockSatSensor):
    def __init__(self, i2c):
        # Configure the sensor on the supplied i2c bus
        self.bno055 = adafruit_bno055.BNO055_I2C(i2c)
        # Define the header
        self.header = [
            "BNO055 Temperature",
            "BNO055 Acceleration",
            "BNO055 Magnetic",
            "BNO055 Gyroscope",
            "BNO055 Euler",
            "BNO055 Quaternion",
            "BNO055 Linear Acceleration",
            "BNO055 Linear Gravity",
        ]

    def getHeader(self):
        return self.header
    
    def poll(self):
        return {
            "BNO055 Temperature": self.bno055.temperature,
            "BNO055 Acceleration": self.bno055.acceleration,
            "BNO055 Magnetic": self.bno055.magnetic,
            "BNO055 Gyroscope": self.bno055.gyroscope,
            "BNO055 Euler": self.bno055.euler,
            "BNO055 Quaternion": self.bno055.quaternion,
            "BNO055 Linear Acceleration": self.bno055.linear_acceleration,
            "BNO055 Linear Gravity": self.bno055.gravity,
        }
