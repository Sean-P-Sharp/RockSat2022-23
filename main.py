###############################################################################
#                                                                             #
#       RockSat-X 2022/2023                                                   #
#         Main Flight Code                                                    #
#           Contributors - Gage Gunn, Sean Sharp, Angela Gabay, Vu Dang       #
#                                                                             #
###############################################################################


import board 
import busio
import digitalio
import adafruit_bme680
import bme680_interface
import adafruit_lsm9ds1
import dof_interface
import adafruit_mlx90640
import mlx90640_interface
import aux_interface
import os
import time

# Initialize BME sensor
cs_bme = digitalio.DigitalInOut(board.D17)
spi_bme = busio.SPI(board.SCLK, board.MOSI, board.MISO)
bme = adafruit_bme680.Adafruit_BME680_SPI(spi_bme, cs_bme)
bme_interface = bme680_interface.BME680_interface("BME", bme, sample_rate=1)

# Initialize 9DOF sensor
i2c_dof = board.I2C()
dof = adafruit_lsm9ds1.LSM9DS1_I2C(i2c_dof)
dof_interface = dof_interface.dof_interface("9DOF", dof, sample_rate=100)

# Initialize MLX sensor
i2c_mlx = board.I2C()
mlx = adafruit_mlx90640.mlx90640_I2C(i2c_mlx, debug=False)
mlx_interface = mlx90640_interface.mlx90640_interface("MLX90640", mlx, sample_rate=1)

# Initialize Camera
camera = aux_interface.Adafruit_Camera_Interface("Adafruit Camera", "/dev/ttyAMA0")
directory = os.path.expanduser("~/images")
if not os.path.exists(directory):
    os.makedirs(directory)


