import RPi.GPIO as GPIO
import time

pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

while True:
    GPIO.output(pin, GPIO.LOW)
    input("0")
    GPIO.output(pin, GPIO.HIGH)
    input("1")
