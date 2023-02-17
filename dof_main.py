import board 
import busio
import digitalio
import adafruit_lsm9ds1
import dof_interface
import time

cs=digitalio.DigitalInOut(board.D17)
i2c = board.I2C()
dof = adafruit_lsm9ds1.LSM9DS1_I2C(i2c, debug=False)

bme_interface = dof_interface.dof_interface("9DOF", dof, sample_rate=1)

bme_interface.start_data_collection()

time.sleep(20)

bme_interface.stop_data_collection()