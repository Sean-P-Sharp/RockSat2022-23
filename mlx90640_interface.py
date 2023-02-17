'''
MLX90640 Sensor Interface
Contributor(s): Gage Gunn, Angela Gabay, Vu Dang
Rocksat-X 2022/2023
'''

import sensor_interface
import time
import board
import adafruit_mlx90640
import busio
import numpy as np
import matplotlib.pyplot as plt

i2c = board.I2C()   # uses board.SCL and board.SDA
mlx = adafruit_mlx90640.MLX90640(i2c, debug=False)

class MLX90640_interface(sensor_interface.sensor_interface):
    def __init__(self, name, MLX90640_object, csv_writer=None, sample_rate=3):
        super().__init__(name, MLX90640_object, csv_writer=csv_writer, sample_rate=sample_rate)

    def collect_data(self):
        while not self._stop_thread:
            frame = np.zeros((24, 32), dtype=float)
            self.mlx.getFrame(frame)

            plt.imshow(frame, cmap="hot")
            plt.axis("off")
            plt.savefig("C:\Data\image.png")
            pass