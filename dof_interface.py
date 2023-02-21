'''
9DOF Sensor Test File
Contributor(s): Gage Gunn, Angela Gabay
Rocksat-X 2022/2023
'''

import sensor_interface
import time

class dof_interface(sensor_interface.sensor_interface):
	def __init__(self, name, DOF_object, csv_writer=None, sample_rate=3):
		super().__init__(name, DOF_object, csv_writer=csv_writer, sample_rate=sample_rate)

	def collect_data(self):

		while not self.stop_thread:
			accel_x, accel_y, accel_z = self.sensor_obj.acceleration
			acceleration = accel_x, accel_y, accel_z
			print("Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})".format(accel_x, accel_y, accel_z))

			mag_x, mag_y, mag_z = self.sensor_obj.magnetic
			magnetic = mag_x, mag_y, mag_z
			print("Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})".format(mag_x, mag_y, mag_z))

			gyro_x, gyro_y, gyro_z = self.sensor_obj.gyro
			gyroscope = gyro_x, gyro_y, gyro_z
			print("Gyroscope (rad/sec): ({0:0.3f},{1:0.3f},{2:0.3f})".format(gyro_x, gyro_y, gyro_z))

			self.store_data_as_csv(acceleration, magnetic, gyroscope)
			time.sleep(1/self.sample_rate)
