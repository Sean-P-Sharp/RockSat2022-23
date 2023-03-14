import qwiic
import time
import sys

ToF = qwiic.QwiicVL53L1X()
if (ToF.sensor_init() == None):                  # Begin returns 0 on a good init
    print("Sensor online!\n")

def runExample():

	print("\nSparkFun VL53L1X Example 1\n")
	mySensor = qwiic_vl53l1x.QwiicVL53L1X()

	#if mySensor.isConnected() == False:
	#	print("The Qwiic VL53L1X device isn't connected to the system. Please check your connection", \
	#		file=sys.stderr)
	#	return

	mySensor.sensor_init()
  

while True:
    try:
        ToF.start_ranging(0)                      # Write configuration bytes to initiate measurement
        time.sleep(.005)
        distance = ToF.get_distance()    # Get the result of the measurement from the sensor
        time.sleep(.005)
        ToF.stop_ranging(1000)

        distanceMeters = distance * 1000

        print("Distance(mm): %s Distance(m): %s" % (distance, distanceMeters))

    except Exception as e:
        print(e)
