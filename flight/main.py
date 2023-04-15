from SensorManager import SensorManager
from SensorInterfaceFactory import SensorInterfaceFactory
from PiGpioManager import PiGpioManager
import json

# this script is your main process
# this is where you instantiate objects and start processes and threads

# import the configs
f = open("config.json")
configs = json.load(f)

# parse out the configs
# this is useful for having configuration values that you want to change quickly
bme1Rate = configs["sample_rates"]["bme_1"]
bme2Rate = configs["sample_rates"]["bme_2"]
bnoRate = configs["sample_rates"]["bno"]
dofRate = configs["sample_rates"]["dof"]
mlxRate = configs["sample_rates"]["mlx"]
maxMotorDuration = configs["motor_max_time"]
outputGpioPins = configs["output_gpio"]
inputGpioPins = configs["input_gpio"]

# create the sensor factory
sensorFac = SensorInterfaceFactory()
# create the sensor manager
sensorMan = SensorManager(sensorFac, bme1Rate, bme2Rate, bnoRate, dofRate, mlxRate)
# create the GPIO manager
gpioMan = PiGpioManager(inputGpioPins, outputGpioPins)

# start collecting data for the sensors
sensorMan.startSensors()

# TODO : do some work here before stopping sensor data collection

# stop collecting data for the sensors
sensorMan.stopSensors()
