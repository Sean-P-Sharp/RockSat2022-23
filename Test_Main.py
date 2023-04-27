import Thermial_Image
import VL53L0X_Interface
import Bno055Interface
from sensors import ISensorInterface
#from sensors import Bme680Interface, DofInterface, ISensorInterface
import board 
import busio
#import digitalio
#import adafruit_bme680
#import adafruit_lsm9ds1
#import adafruit_mlx90640
#import aux_interface
import os
import time
import threading

from File_Structure_Linux import FileStructure
fs = FileStructure()

import RPi._GPIO as GPIO
from adafruit_motorkit import MotorKit

#Create folders
fs.create_folders()
fs.write_to_folder('Flight_Log', '', 'Folders Checked\n')

# # Initialize BME sensor
# cs_bme = digitalio.DigitalInOut(board.D17)
# spi_bme = busio.SPI(board.SCLK, board.MOSI, board.MISO)
# bme = adafruit_bme680.Adafruit_BME680_SPI(spi_bme, cs_bme)
# bme_interface = Bme680Interface.Bme680Interface("BME", bme, sample_rate=1)

# # Initialize 9DOF sensor
# i2c_dof = board.I2C()
# dof = adafruit_lsm9ds1.LSM9DS1_I2C(i2c_dof)
# DofInterface = DofInterface.DofInterface("9DOF", dof, sample_rate=100)

# # Initialize MLX sensor
# i2c_mlx = board.I2C()
# mlx = adafruit_mlx90640.mlx90640_I2C(i2c_mlx, debug=False)
# mlx_interface = mlx90640_interface.mlx90640_interface("MLX90640", mlx, sample_rate=1)

# # Initialize Camera
# camera = aux_interface.Adafruit_Camera_Interface("Adafruit Camera", "/dev/ttyAMA0")
# directory = os.path.expanduser("~/images")
# if not os.path.exists(directory):
#     os.makedirs(directory)


#photo_thread = threading.Thread(target=Thermial_Image.take_photos_every_5_seconds, args=())
#photo_thread.start()

#BME_thread = threading.Tread(target = Bme680Interface.Bme680Interface.collect_data, args=())
#BME_thread.start()

#Dof_thread = threading.Thread(target = DofInterface.DofInterface.collect_data)
#Dof_thread.start()

VL53L0X_thread = threading.Thread(target=VL53L0X_Interface.VL53OX_interface.sample_distance, args=())
VL53L0X_thread.start()

BNO055_thread = threading.Thread(target= Bno055Interface.temprature, args=())
BNO055_thread.start()

