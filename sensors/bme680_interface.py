'''
Concrete implementation for BME680 sensor interface 
Contrbutors: Gage Gunn, Angela Gabay, Vu Dang
RRCC/ACC Rocksat-X 2023
'''
import sensor_interface
import time

class BME680_interface(sensor_interface.sensor_interface):
    def __init__(self, name, BME680_object, csv_writer=None, sample_rate=3):
        super().__init__(name, BME680_object, csv_writer=csv_writer, sample_rate=sample_rate)

    def collect_data(self):
		
        while not self.stop_thread:
            t = time.time() - self._start_time

            temperature = self.sensor_obj.temperature
            print("\nTemperature: %0.1f C" % temperature)
            
            humidity = self.sensor_obj.humidity
            print("Humidity: %0.1f %%" % humidity)
            
            pressure = self.sensor_obj.pressure
            print("Pressure: %0.3f hPa" % pressure)

            altitude = self.sensor_obj.altitude
            print("Altitude = %0.2f meters" % altitude)
            
            self.store_data_as_csv(t, temperature, humidity, pressure, altitude)

            time.sleep(self.sample_rate)
