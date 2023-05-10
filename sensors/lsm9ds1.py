"""
    LSM9DS1.py
        Accelerometer/Magnetometer/Gyroscope Sensor
"""

# Base RockSatSensor Class
from sensors.base import RockSatSensor

# Adafruit Library for the LSM9DS1
import adafruit_lsm9ds1

# LSM9DS1 Object
class LSM9DS1(RockSatSensor):
    def __init__(self, i2c):
        # Configure the sensor on the supplied i2c bus
        self.lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c, 0x1e)
        # Define the header
        self.header = [
            "LSM9DS1 Acceleration (x)",
            "LSM9DS1 Acceleration (y)",
            "LSM9DS1 Acceleration (z)",
            "LSM9DS1 Magnetometer (x)",
            "LSM9DS1 Magnetometer (y)",
            "LSM9DS1 Magnetometer (z)",
            "LSM9DS1 Gyroscope (x)",
            "LSM9DS1 Gyroscope (y)",
            "LSM9DS1 Gyroscope (z)",
            "LSM9DS1 Temperature",
        ]

    def getHeader(self):
        return self.header
    
    def poll(self):
        # This sensor is odd, get the data as suggested in the circutpython documentation
        accel_x, accel_y, accel_z = self.lsm9ds1.acceleration
        mag_x, mag_y, mag_z = self.lsm9ds1.magnetic
        gyro_x, gyro_y, gyro_z = self.lsm9ds1.gyro
        temp = self.lsm9ds1.temperature
        # Return polled sensors
        return {
            "LSM9DS1 Acceleration (x)": accel_x,
            "LSM9DS1 Acceleration (y)": accel_y,
            "LSM9DS1 Acceleration (z)": accel_z,
            "LSM9DS1 Magnetometer (x)": mag_x,
            "LSM9DS1 Magnetometer (y)": mag_y,
            "LSM9DS1 Magnetometer (z)": mag_z,
            "LSM9DS1 Gyroscope (x)": gyro_x,
            "LSM9DS1 Gyroscope (y)": gyro_y,
            "LSM9DS1 Gyroscope (z)": gyro_z,
            "LSM9DS1 Temperature": temp,
        }
