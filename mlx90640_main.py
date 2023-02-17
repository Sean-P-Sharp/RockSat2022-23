'''
MLX90640 Sensor Main
Contributor(s): Gage Gunn, Angela Gabay, Vu Dang
Rocksat-X 2022/2023
'''

import board 
import busio
import digitalio
import adafruit_mlx90640
import mlx90640_interface
import time

i2c = board.I2C()
mlx = adafruit_mlx90640.mlx90640_I2C(i2c, debug=False)

mlx_interface = mlx90640_interface.mlx90640_interface("MLX90640", mlx, sample_rate=1)

mlx_interface.start_data_collection()

time.sleep(20)

mlx_interface.stop_data_collection()