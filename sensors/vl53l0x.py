"""
    VL53L0X.py
        Time of Flight Distance Sensor
"""

# Base RockSatSensor Class
from sensors import RockSatSensor

# Adafruit Library for the VL53L0X
import adafruit_vl53l0x

# VL53L0X Object
class VL53L0X(RockSatSensor):
    def __init__(self, i2c):
        # Configure the sensor on the supplied i2c bus
        self.vl53l0x = adafruit_vl53l0x.VL53L0X(i2c)
        # Define the header
        self.header = [
            "VL54L0X Distance",
        ]

    def getHeader(self):
        return self.header
    
    def poll(self):
        return {
            "VL54L0X Distance": self.vl53l0x.range,
        }
