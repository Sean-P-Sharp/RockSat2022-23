import hcsr04_interface
import hcsr04
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

ultrasonic_sensor = hcsr04.hcsr04(22, 27)

ultrasonic_sensor_interface = hcsr04_interface.hcsr04_interface("HCSR04", ultrasonic_sensor, 2)

ultrasonic_sensor_interface.start_data_collection()

ultrasonic_sensor_interface.start_heartbeat()

time.sleep(100)

ultrasonic_sensor_interface.stop_data_collection()

ultrasonic_sensor_interface.stop_heartbeat()

GPIO.cleanup()
