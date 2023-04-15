##################################
# MLX90640 Take Picture Interface
##################################
#
import math
from PIL import Image
import time,board,busio
import numpy as np
import adafruit_mlx90640
import time

# FILENAME = "mlx.jpg"

def save_photo_to(file_name):
    MINTEMP = 25.0 # Low range of temp
    MAXTEMP = 45.0 # High range of temp
    COLORDEPTH = 1000
    INTERPOLATE = 10 # scale factor for the final image

    mlx = adafruit_mlx90640.MLX90640(board.I2C())

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
        colormap[i] = gradient(i, COLORDEPTH, heatmap)

    # get sensor data
    frame = [0] * 768
    success = False
    while not success:
        try:
            mlx.getFrame(frame)
            success = True
        except ValueError:
            continue

    # create the image
    pixels = [0] * 768
    for i, pixel in enumerate(frame):
        coloridx = map_value(pixel, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1)
        coloridx = int(constrain(coloridx, 0, COLORDEPTH - 1))
        pixels[i] = colormap[coloridx]

    # save to file
    img = Image.new("RGB", (32, 24))
    img.putdata(pixels)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img = img.resize((32 * INTERPOLATE, 24 * INTERPOLATE), Image.BICUBIC)
    img.save(file_name)

# utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map_value(x, in_min, in_max, out_min, out_max):
    return(x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def gaussian(x, a, b, c, d=0):
    return a *math.exp(-((x-b)**2)/(2*c**2)) + d

def gradient(x, width, cmap, spread=1):
    width = float(width)
    r = sum(
        gaussian(x, p[1][0], p[0]*width, width / (spread * len(cmap))) for p in cmap
    )
    g = sum(
        gaussian(x, p[1][1], p[0]*width, width / (spread * len(cmap))) for p in cmap
    )
    b = sum(
        gaussian(x, p[1][2], p[0] * width, width / (spread * len(cmap))) for p in cmap
    )
    r = int(constrain(r * 255, 0, 255))
    g = int(constrain(g * 255, 0, 255))
    b = int(constrain(b * 255, 0, 255))
    return r, g, b

def take_photos_every_5_seconds():
    while (True):
        time.sleep(5)
        timestamp = time.asctime(time.gmtime())
        save_photo_to("thermal-pics/" + timestamp + ".jpg")