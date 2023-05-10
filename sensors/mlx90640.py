"""
    MLX90640.py
        Thermal Camera 
"""

# Base RockSatSensor Class
from sensors import RockSatSensor

# Adafruit Library for the MLX90640
import adafruit_mlx90640

# MLX90640 Object
class MLX90640(RockSatSensor):
    def __init__(self, i2c):
        # Configure the sensor on the supplied i2c bus
        self.mlx90640 = adafruit_mlx90640.MLX90640(i2c)
        # Set the refresh rate to 2Hz
        mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
        # Define the header
        self.header = [
            "MLX90640 Thermal Frame",
        ]

    def getHeader(self):
        return self.header
    
    def poll(self):
        frame = [0] * 768
        self.mlx90640.getFrame(frame)
        return {
            "MLX90640 Thermal Frame": frame,
        }
