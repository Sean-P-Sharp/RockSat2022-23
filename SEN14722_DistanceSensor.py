#import sensor_interface
import time
import sys
import qwiic_vl53l1x

#i2c = board.I2C()
#SEN_interface = qwiic_vl53l1x.QwiicVL53L1X(i2c)

#class SEN14722_interface(sensor_interface.sensor_interface):
 #   def __init__(self,name, SEN14722_object, csv_writer=None, sample_rate=3):
  #      super().__init__(name, SEN14722_object, csv_writer=csv_writer, sample_rate=sample_rate)
#def collect_data(self):
 #   distance_sensor = self.sensor_obj
  #  distance_sensor.begin()

 #   while not self.stop_thread:

  #      distance_mm = distance_sensor.get_distance()
   #     distance_cm = distance_mm/10.0
    #    self.store_distance_as_csv(distance_cm)

     #   time.sleep(self.sample_rate)
      #  distance_sensor.end()

def runExample():
    print("\nSparkFun VL53L1X Example 1\n")
    mySensor = qwiic_vl53l1x.QwiicVL53L1X()

    if mySensor.isConnected() == False:
        print("The Qwiic VL53L1X device isn't connected to the system. Please check your connection", \
              file=sys.stderr)
        return

    mySensor.sensor_init()

    while True:
        try:
            mySensor.start_ranging()  # Write configuration bytes to initiate measurement
            time.sleep(.005)
            distance = mySensor.get_distance()  # Get the result of the measurement from the sensor
            time.sleep(.005)
            mySensor.stop_ranging()

            print("Distance(mm): %s" % distance)

        except Exception as e:
            print(e)

