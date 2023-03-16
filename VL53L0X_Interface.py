import time
import board
import busio
import adafruit_vl53l0x

#initilize the I2c
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

#adjust the measurment timing budget to chage speed and accuracy
#Faster sample speed but lessend accuracy
#vl53.measurement_timing_budget = 20000

#slower sample spped greater accuracy
#vl53.measurement_timing_budget = 200000

while True:
    print("Range: {0}mm".format(vl53.range))
    time.sleep(1)


