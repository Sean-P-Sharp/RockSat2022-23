import board 
import busio
import adafruit_mlx90640
import thermal_cam_interface
import time

i2c = board.I2C()
mlx = adafruit_mlx90640.MLX90640(i2c)

mlx_interface = thermal_cam_interface.thermal_cam_interface("MLX90640", mlx, sample_rate=0.2)

mlx_interface.start_data_collection()

time.sleep(20)

mlx_interface.stop_data_collection()
