
import time
import board
import adafruit_bno055


#initilize i2c
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)


last_val = 0xFFFF

def temprature():
        global last_val
        result = sensor.temperature
        if abs(result - last_val) == 128:
                result = sensor.temperature
                if abs(result - last_val) ==128:
                        return 0b00111111 & result
        last_val = result
        return result

while True:
        print("Temprature: {} degrees".format(sensor.temperature))
        
        print ("Temprature : {} degrees C".format(sensor.temperature))

        print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
        print("Magnetometer (microteslas): {}".format(sensor.magnetic))
        print("Gyroscope (Rad/sec): {}".format(sensor.gyro))
        print("Euler angle: {}".format(sensor.euler))
        print("Quaternion: {}".format(sensor.quaternion))
        print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
        print("Gravity (m/s^2): {}".format(sensor.gravity))
    
        time.sleep(1)