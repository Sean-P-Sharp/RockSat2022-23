##################################
# MLX90640 Take Picture Interface
##################################
#
import math
from PIL import Image
import time,board,busio
import numpy as np
import time

# FILENAME = "mlx.jpg"

import ISensorInterface
import time

class ThermalCamInterface(ISensorInterface.ISensorInterface):
    
    def _init_(self, name, THERMAL_object, csv_writer=None, sample_rate=3):
        super(ThermalCamInterface, self)._init_(name, THERMAL_object, csv_writer=csv_writer, sample_rate=sample_rate)

    def save_photo_to(self, file_name):
        MINTEMP = 25.0 # Low range of temp
        MAXTEMP = 45.0 # High range of temp
        COLORDEPTH = 1000
        INTERPOLATE = 10 # scale factor for the final image


    #List of colors that can be used
        heatmap = (
            (0.0, (0, 0, 0)),
            (0.20,(0, 0, 0.5)),
            (0.40,(0, 0.5, 0)),
            (0.60,(0.5, 0, 0)),
            (0.80,(0.75, 0.75, 0)),
            (0.90,(1.0, 0.75, 0)),
            (1.00,(1.0, 1.0, 1.0))
        )
        colormap = [0] * COLORDEPTH

        for i in range(COLORDEPTH):
            colormap[i] = self.gradient(i, COLORDEPTH, heatmap)

    # get sensor data
        frame = [0] * 768
        success = False
        while not success:
            try:
                self.sensor_obj.getFrame(frame)
                success = True
            except ValueError:
                continue

    # create the image
        pixels = [0] * 768
        for i, pixel in enumerate(frame):
            coloridx = self.map_value(pixel, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1)
            coloridx = int(self.constrain(coloridx, 0, COLORDEPTH - 1))
            pixels[i] = colormap[coloridx]

    # save to file
        img = Image.new("RGB", (32, 24))
        img.putdata(pixels)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img = img.resize((32 * INTERPOLATE, 24 * INTERPOLATE), Image.BICUBIC)
        img.save(file_name)

    # utility functions
    def constrain(self, val, min_val, max_val):
        return min(max_val, max(min_val, val))

    def map_value(self, x, in_min, in_max, out_min, out_max):
        return(x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def gaussian(self, x, a, b, c, d=0):
        return a *math.exp(-((x-b)**2)/(2*c**2)) + d

    def gradient(self, x, width, cmap, spread=1):
        width = float(width)
        r = sum(
            self.gaussian(x, p[1][0], p[0]*width, width / (spread * len(cmap))) for p in cmap
        )
        g = sum(
            self.gaussian(x, p[1][1], p[0]*width, width / (spread * len(cmap))) for p in cmap
        )
        b = sum(
            self.gaussian(x, p[1][2], p[0] * width, width / (spread * len(cmap))) for p in cmap
        )
        r = int(self.constrain(r * 255, 0, 255))
        g = int(self.constrain(g * 255, 0, 255))
        b = int(self.constrain(b * 255, 0, 255))
        return r, g, b

    def collect_data(self):
        while not self.stop_thread:
            timestamp = time.asctime(time.gmtime())
            self.save_photo_to("./" + timestamp + ".jpg")
            time.sleep(1/self.sample_rate)
