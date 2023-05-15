"""
    sensors.py - Sensor control file
"""

# Import dependencies
import os
import time
import logging

# Adafruit circutpython
import board
import busio

# Import RockSat sensors
from sensors.timems import TimeMS
from sensors.bme680 import BME680_Inside, BME680_Outside
from sensors.bno055 import BNO055
from sensors.vl53l0x import VL53L0X
from sensors.lsm9ds1 import LSM9DS1

# Main sensor thread
def main(bootTime, telemetry):
    # Acquire the existing logger
    logger = logging.getLogger(__name__)

    # Log from this new thread
    logger.info("Started sensor thread")

    # Start the I2C interface for the sensors
    i2c = None
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        logger.info("Started I2C interface for sensors")
        logger.info(f"Found I2C devices at addresses: {', '.join([hex(x) for x in i2c.scan()])}")
    except Exception as e:
        logger.critical("Failed to enable i2c interface, the sensor thread will now crash!")
        logger.critical(f"Exception: {e}")
        return

    # Desired sensors
    desiredSensors = [
        BME680_Inside,      # Temperature, Humidity, Pressure and Gas Sensor (inside e-box)
        BME680_Outside,     # Temperature, Humidity, Pressure and Gas Sensor (outside e-box)
        BNO055,             # Absolute Orientation Sensor
        VL53L0X,            # Time of Flight Distance Sensor
        LSM9DS1,            # Accelerometer/Magnetometer/Gyroscope Sensor
    ]

    # Active sensors
    sensors = []

    # Add all of the sensors that we want
    logger.info("Initializing sensors...")
    sensors.append(TimeMS())            # The first is a virtual sensor "TimeMS" which returns the current system time in milliseconds when polled
    
    # Loop through the desired sensors and add them to the active sensors array
    for Sensor in desiredSensors:
        try:
            # Start the sensor
            sensorInstance = Sensor(i2c)
            if sensorInstance: sensors.append(sensorInstance)
            logger.info(f"Initialized {Sensor.__name__} over I2C")
        except Exception as e:
            # Log failure
            logger.critical(f"Failed to initialize {Sensor.__name__} over I2C. Exception: {e}")
    logger.info("Finished initializing sensors")

    # Create the data file
    logger.info(f"Writing sensor data to file: ./data/sensors_{str(int(bootTime))}.csv")
    os.system("mkdir -p data")
    dataFile = open(f"data/sensors_{str(int(bootTime))}.csv", "a")

    # Configure the order of the columns in the CSV file
    sensorOrder = []
    # For each sensor in the list of sensors, add the label elements in the header array 
    for sensor in sensors: sensorOrder = sensorOrder + sensor.getHeader()

    # Write the header line to the CSV file as the first line
    dataFile.write(",".join(sensorOrder) + "\n")

    # Try/Except block to catch KeyboardInterrupt eg. SIGTERM
    telemetryTimeLastSent = 0
    try:
        # Keep polling sensors forever
        while True:
            # Poll all sensors
            data = {}
            for sensor in sensors:
                # Add the sensor data to the current data
                try:
                    next = sensor.poll()
                    data = { **data, **next }
                except Exception as e:
                    logger.critical(f"Failed to poll for next value on sensor {sensor.__name__} at {str(int(time.time() * 1000))}")

            # Construct the CSV line
            csvLine = ""
            i = 0
            for column in sensorOrder:
                # Get the data for this column
                csvLine += str(data[column])
                # Add a comma unless this is the last value
                if i != len(sensorOrder) - 1: csvLine += ","
                i += 1
            csvLine += "\n"

            # Write the CSV line to the file
            dataFile.write(csvLine)
            # Force a flush to ensure that no data is being built up in the memory buffer that could be lost during power failure
            dataFile.flush()

            # Write to telemetry
            if (time.time() - telemetryTimeLastSent > 1) and telemetry != None:
                package = []
                if "BME680 0x76 Temperature" in data: package.append(f"T_i:{str(data['BME680 0x76 Temperature'])}")
                if "BME680 0x77 Temperature" in data: package.append(f"T_e:{str(data['BME680 0x77 Temperature'])}")
                if "VL54L0X Distance" in data: package.append(f"d:{str(data['VL54L0X Distance'])}")
                if "BNO055 Acceleration (x)" in data: package.append(f"a_x:{str(data['BNO055 Acceleration (x)'])}")
                if "BNO055 Acceleration (y)" in data: package.append(f"a_y:{str(data['BNO055 Acceleration (y)'])}")
                if "BNO055 Acceleration (z)" in data: package.append(f"a_z:{str(data['BNO055 Acceleration (z)'])}")
                telemetry.transmit(",".join(package))
                telemetryTimeLastSent = time.time()
    # Capture SIGTERM
    except KeyboardInterrupt:
        logger.warning("Received SIGTERM, writing final data to file and terminating sensor thread")
        dataFile.close()
        return
