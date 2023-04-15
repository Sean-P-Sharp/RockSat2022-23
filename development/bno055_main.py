
import board
import busio
import digitalio
import adafruit_bno055
import Bno055Interface
import time

#initilize i2c
i2c = board.I2C()
bno = adafruit_bno055.BNO055_I2C(i2c)

Bno055Interface = Bno055Interface.Bno055Interface("BNO", bno, sample_rate=10)

Bno055Interface.start_data_collection()

time.sleep(20)

Bno055Interface.stop_data_collection()
