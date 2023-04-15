import board 
import busio
import digitalio
import adafruit_lsm9ds1
import DofInterface
import time

i2c = board.I2C()
dof = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

DofInterface = DofInterface.DofInterface("9DOF", dof, sample_rate=100)

DofInterface.start_data_collection()

time.sleep(20)

DofInterface.stop_data_collection()
