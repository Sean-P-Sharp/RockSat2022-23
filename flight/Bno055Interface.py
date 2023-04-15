import ISensorInterface
import time


last_val = 0xFFFF

class Bno055Interface(ISensorInterface.ISensorInterface):

        def _init_(self, name, BNO_object, csv_writer=None, sample_rate=3):
                super(Bno055Interface, self)._init_(name, BNO_object, csv_writer=csv_writer, sample_rate=sample_rate, last_val=0xFFFF)
        
        def temperature(self):
                result = self.sensor_obj.temperature
                
                if abs(result - self._last_val) == 128:
                        result = self.sensor_obj.temperature
                        if abs(result - self._last_val) == 128:
                                return 0b00111111 & result
                self._last_val = result
                return result
                
        def collect_data(self):
                
                while not self.stop_thread:
                        
                        actual_time = time.time()
                        
                        temperature = self.sensor_obj.temperature
                        #print("Temperature: {} degrees C".format(self.sensor_obj.temperature))
                        
                        acceleration = self.sensor_obj.acceleration
                        print("Accelerometer (m/s^2): {}".format(self.sensor_obj.acceleration))
                        
                        magnetometer = self.sensor_obj.magnetic
                        print("Magnetometer (microteslas): {}".format(self.sensor_obj.magnetic))
                        
                        gyroscope = self.sensor_obj.gyro
                        print("Gyroscope (Rad/sec): {}".format(self.sensor_obj.gyro))
                        
                        euler = self.sensor_obj.euler
                        print("Euler angle: {}".format(self.sensor_obj.euler))
                        
                        quart = self.sensor_obj.quaternion
                        print("Quaternion: {}".format(self.sensor_obj.quaternion))
                        
                        linear = self.sensor_obj.linear_acceleration
                        print("Linear acceleration (m/s^2): {}".format(self.sensor_obj.linear_acceleration))
                        
                        gravity = self.sensor_obj.gravity
                        print("Gravity (m/s^2): {}".format(self.sensor_obj.gravity))
                        
                        self.store_data_as_csv(actual_time, temperature, acceleration, magnetometer, gyroscope, euler, quart, linear, gravity)
                        time.sleep(1/self.sample_rate)
                        
        

                                
