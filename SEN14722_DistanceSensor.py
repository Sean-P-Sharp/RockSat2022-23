import sensor_interface
import time




class SEN14722_interface(sensor_interface.sensor_interface):
    def __init__(self,name, SEN14722_object, csv_writer=None, sample_rate=3):
        super().__init__(name, SEN14722_object, csv_writer=csv_writer, sample_rate=sample_rate)
def collect_data(self):
    distance_sensor = self.sensor_obj
    distance_sensor.begin()

    while not self.stop_thread:

        distance_mm = distance_sensor.get_distance()
        distance_cm = distance_mm/10.0
        self.store_distance_as_csv(distance_cm)

        time.sleep(self.sample_rate)
        distance_sensor.end()
