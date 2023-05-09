"""
    timems.py
        Virtual sensor that polls as the system time in MS    
"""

# Base RockSatSensor Class
from sensors import RockSatSensor

# Time library
import time

# Time Sensor Object
class TimeMS(RockSatSensor):
    def __init__(self):
        self.header = ["Time"]
        pass

    def getHeader(self):
        return self.header
    
    def poll(self):
        return [int(round(time.time() * 1000))]
