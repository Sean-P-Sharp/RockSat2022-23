import RPi.GPIO as GPIO
import time

class hcsr04:
	def __init__(self, trig_pin, echo_pin):
		self._trig_pin = trig_pin
		self._echo_pin = echo_pin
		GPIO.setup(self._trig_pin, GPIO.OUT)
		GPIO.setup(self._echo_pin, GPIO.IN)

	def distance(self):
     		GPIO.output(self._trig_pin, 1)
     		time.sleep(0.000001)
     		GPIO.output(self._trig_pin, 0)
     		start_time = time.time()
     		end_time = time.time()
     		while (GPIO.input(self._echo_pin) == 0):
             		start_time = time.time()
     		while (GPIO.input(self._echo_pin) == 1):
             		end_time = time.time()
     		elapsed = end_time - start_time
     		distance = elapsed * 34300 / 2
     		return (end_time, distance) 
     		
