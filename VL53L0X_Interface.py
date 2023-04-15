import time
import board
import busio
import adafruit_vl53l0x
from sensors import ISensorInterface

#initilize the I2c
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

#adjust the measurment timing budget to chage speed and accuracy
#Faster sample speed but lessend accuracy
#vl53.measurement_timing_budget = 20000

#slower sample spped greater accuracy
vl53.measurement_timing_budget = 200000
range = vl53.range


class VL53OX_interface(ISensorInterface.ISensorInterface):
    def __init__(self, name, VL53OX_object, csv_writer=None, sample_rate=3):
       super().__init__(name, VL53OX_object, csv_writer=csv_writer, sample_rate=sample_rate)
    
    def sample_distance():
        Distance_Data = []
        while True:
            Distance_Data.append("Range: {0}mm".format(vl53.range))
            print(Distance_Data)
            time.sleep(1)




        


