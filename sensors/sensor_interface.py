import time
from csv import writer
from threading import Thread

class sensor_interface:
	def __init__(self, sensor_name, sensor_obj, csv_writer = None, sample_rate=5):
		self._sensor_obj = sensor_obj
		self._sample_rate = sample_rate
		self._sensor_name = sensor_name
		self._file_name = f"{sensor_name}_data.csv"
		
		if (csv_writer == None):
			self._csvfile = open(self._file_name, "a")
			self._writer_object = writer(self._csvfile)
		else:
			self._writer_object = csv_writer

		self._writer_object.writerow(["time, data"])

		self._collection_thread = Thread(target=self.collect_data) 
		self._stop_thread = False

		self._heartbeat_thread = Thread(target=self.heartbeat)
		self._stop_heartbeat_thread = False
		
	def init_sensor(self):
		return True
		
	def start_data_collection(self):
		self._stop_thread = False
		self._collection_thread.start()
		return True
		
	def collect_data(self):
		return True
		
	def stop_data_collection(self):
		self._stop_thread = True
		self._collection_thread.join()
		return True
		
	def cleanup(self):
		if (self._csvfile != None):
			self._csvfile.close()
		return True
		
	def store_data_as_csv(self, time, data_point):
		self._writer_object.writerow([time, data_point])
		return True
		
	def start_heartbeat(self):
		self._stop_heartbeat_thread = False
		self._heartbeat_thread.start()
		return True
		
	def stop_heartbeat(self):
		self._stop_heartbeat_thread = True
		self._heartbeat_thread.join()
		return True
		
	def heartbeat(self):
		while not self._stop_heartbeat_thread:
			print("Sensor is still alive")
			time.sleep(1)
