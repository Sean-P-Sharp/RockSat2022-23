
import board
import busio
import digitalio
import adafruit_bno055
import bno055_interface
import time

#initilize i2c
i2c = board.I2C()
bno = adafruit_bno055.BNO055_I2C(i2c)

bno055_interface = bno055_interface.bno055_interface("BNO", bno, sample_rate=10)

bno055_interface.start_data_collection()

time.sleep(20)

bno055_interface.stop_data_collection()
