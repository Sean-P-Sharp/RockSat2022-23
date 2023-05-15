"""
    BNO055.py
        Absolute Orientation Sensor
"""

# Base RockSatSensor Class
from sensors.base import RockSatSensor

# Adafruit Library for the BNO055
import adafruit_bno055

# BNO055 Object
class BNO055(RockSatSensor):
    def __init__(self, i2c):
        # Configure the sensor on the supplied i2c bus
        self.bno055 = adafruit_bno055.BNO055_I2C(i2c, 0x28)
        # Define the header
        self.header = [
            # "BNO055 Temperature",
            "BNO055 Acceleration (x)",
            "BNO055 Acceleration (y)",
            "BNO055 Acceleration (z)",
            "BNO055 Magnetic (x)",
            "BNO055 Magnetic (y)",
            "BNO055 Magnetic (z)",
            "BNO055 Gyroscope (x)",
            "BNO055 Gyroscope (y)",
            "BNO055 Gyroscope (z)",
            "BNO055 Euler (x)",
            "BNO055 Euler (y)",
            "BNO055 Euler (z)",
            "BNO055 Quaternion (a)",
            "BNO055 Quaternion (b)",
            "BNO055 Quaternion (c)",
            "BNO055 Quaternion (d)",
            "BNO055 Linear Acceleration (x)",
            "BNO055 Linear Acceleration (y)",
            "BNO055 Linear Acceleration (z)",
            "BNO055 Linear Gravity (x)",
            "BNO055 Linear Gravity (y)",
            "BNO055 Linear Gravity (z)",
        ]

    def getHeader(self):
        return self.header
    
    def poll(self):
        # Poll sensor
        temperature = self.bno055.temperature,
        accel_x, accel_y, accel_z = self.bno055.acceleration
        mag_x, mag_y, mag_z = self.bno055.magnetic
        gyro_x, gyro_y, gyro_z = self.bno055.gyro
        euler_x, euler_y, euler_z = self.bno055.euler
        quat_a, quat_b, quat_c, quat_d = self.bno055.quaternion
        linear_x, linear_y, linear_z = self.bno055.linear_acceleration
        gravity_x, gravity_y, gravity_z = self.bno055.linear_acceleration
        # Construct return object
        return {
            # "BNO055 Temperature": temperature,
            "BNO055 Acceleration (x)": accel_x,
            "BNO055 Acceleration (y)": accel_y,
            "BNO055 Acceleration (z)": accel_z,
            "BNO055 Magnetic (x)": mag_x,
            "BNO055 Magnetic (y)": mag_y,
            "BNO055 Magnetic (z)": mag_z,
            "BNO055 Gyroscope (x)": gyro_x,
            "BNO055 Gyroscope (y)": gyro_y,
            "BNO055 Gyroscope (z)": gyro_z,
            "BNO055 Euler (x)": euler_x,
            "BNO055 Euler (y)": euler_y,
            "BNO055 Euler (z)": euler_z,
            "BNO055 Quaternion (a)": quat_a,
            "BNO055 Quaternion (b)": quat_b,
            "BNO055 Quaternion (c)": quat_c,
            "BNO055 Quaternion (d)": quat_d,
            "BNO055 Linear Acceleration (x)": linear_x,
            "BNO055 Linear Acceleration (y)": linear_y,
            "BNO055 Linear Acceleration (z)": linear_z,
            "BNO055 Linear Gravity (x)": gravity_x,
            "BNO055 Linear Gravity (y)": gravity_y,
            "BNO055 Linear Gravity (z)": gravity_z,
        }
