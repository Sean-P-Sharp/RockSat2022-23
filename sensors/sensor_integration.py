from bme680_interface import BME680_interface
from bno055_interface import bno055_interface
from dof_interface import dof_interface
import board 
import busio
import digitalio
import adafruit_bme680
import adafruit_bno055
import adafruit_lsm9ds1
import time

# sample rates (in Hz)
bme_sample_rate = 1
bno_sample_rate = 10
dof_sample_rate = 100

# comm interfaces
cs=digitalio.DigitalInOut(board.D5)
spi=busio.SPI(board.SCLK,board.MOSI,board.MISO)
i2c = board.I2C()

# create the bme objects
bme = adafruit_bme680.Adafruit_BME680_SPI(spi,cs)
bme_interface = BME680_interface("BME", bme, sample_rate=bme_sample_rate)

# create the bno objects
bno = adafruit_bno055.BNO055_I2C(i2c)
bno055_interface = bno055_interface("BNO", bno, sample_rate=bno_sample_rate)

# create the 9dof objects
dof = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
dof_interface = dof_interface("9DOF", dof, sample_rate=dof_sample_rate)

# start the data collection
bme_interface.start_data_collection()
bno055_interface.start_data_collection()
dof_interface.start_data_collection()

time.sleep(20)

# stop the data collection
bme_interface.stop_data_collection()
bno055_interface.stop_data_collection()
dof_interface.stop_data_collection()


