'''
Sensor Interface
Contrbutors: Gage Gunn, Angela Gabay, Vu Dang
RRCC/ACC Rocksat-X 2023
'''

### Libraries ###
import time
from csv import writer
from threading import Thread


### Objects ###
class sensor_interface:
    def __init__(self, sensor_name, sensor_obj, csv_writer = None, sample_rate=3):
        self.sensor_obj = sensor_obj
        self.sample_rate = sample_rate
        self.sensor_name = sensor_name
        self._file_name = f"{sensor_name}_data.csv"
        
        if (csv_writer == None):
            self._csvfile = open(self._file_name, "a")
            self._writer_object = writer(self._csvfile)
        else:
            self._writer_object = csv_writer

        self._writer_object.writerow(["time, data"])

        self._collection_thread = Thread(target=self.collect_data) 
        self.stop_thread = False

    def init_sensor(self):
        return True

    def collect_data(self):
        return True

    def start_data_collection(self):
        self._start_time = time.time()
        self.stop_thread = False
        self._collection_thread.start()
        return True

    def stop_data_collection(self):
        self.stop_thread = True
        self._collection_thread.join()
        return True
    
    def cleanup(self):
        if (self._csvfile != None):
            self._csvfile.close()
            return True

    def store_data_as_csv(self, time, data_point_1):
        self._writer_object.writerow([time, data_point_1])
        return True

    def store_data_as_csv(self, time, data_point_1, data_point_2, datapoint_3, datapoint_4):
        self._writer_object.writerow([time, data_point_1, data_point_2, datapoint_3, datapoint_4])
        return True
