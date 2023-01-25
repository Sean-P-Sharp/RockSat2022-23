import sensor_interface
import time

class hcsr04_interface(sensor_interface.sensor_interface):
	def __init__(self, name, hcsr04_object, csv_writer=None, sample_rate=5):
		super().__init__(name, hcsr04_object, csv_writer=csv_writer, sample_rate=sample_rate)
					
	def collect_data(self):
		while not self._stop_thread:
			(t,d) = self._sensor_obj.distance()
			print(f"data at time {t} = {d}")
			self.store_data_as_csv(t, d)
			time.sleep(1/self._sample_rate)
			
		
		
