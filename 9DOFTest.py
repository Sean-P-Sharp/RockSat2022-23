'''
9DOF (LSM9DS1) Sensor Test File
Contributor(s): Gage Gunn, Angela Gabay
Rocksat-X 2022/2023
'''

import sensor_interface
import time
import board
import adafruit_lsm9ds1

i2c = board.I2C()   # uses board.SCL and board.SDA
DOF = adafruit_lsm9ds1.LSM9DS1_I2C(i2c, debug=False)

class BME680_interface(sensor_interface.sensor_interface):
    def __init__(self, name, DOF_object, csv_writer=None, sample_rate=3):
        super().__init__(name, DOF_object, csv_writer=csv_writer, sample_rate=sample_rate)

def collect_data(self):

    while not self._stop_thread:
        accel_x, accel_y, accel_z = self.sensor_obj.DOF.acceleration()
        acceleration = accel_x, accel_y, accel_z
        print("Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})".format(accel_x, accel_y, accel_z))

        mag_x, mag_y, mag_z = self.sensor_obj.DOF.magnetic
        magnetic = mag_x, mag_y, mag_z
        print("Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})".format(mag_x, mag_y, mag_z))

        gyro_x, gyro_y, gyro_z = self.sensor_obj.DOF.gyro
        gyroscope = gyro_x, gyro_y, gyro_z
        print("Gyroscope (rad/sec): ({0:0.3f},{1:0.3f},{2:0.3f})".format(gyro_x, gyro_y, gyro_z))

        self.store_data_as_csv(acceleration, magnetic, gyroscope)