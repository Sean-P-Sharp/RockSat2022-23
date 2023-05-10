"""
    sensors.py - Sensor control file
"""

# Import dependencies
import logging
import time
import os

# Adafruit circutpython
import board
import busio

# Import RockSat sensors
from timems import TimeMS
from mlx90640 import MLX90640
from bme80 import BME680
from bno055 import BNO055
from vl53l0x import VL53L0X
from lsm9ds1 import LSM9DS1

# Template for a basic RockSat sensor
#   Each sensor is going to need to return a dictionary containing the data returned by the sensor and an ordered array of the headers for the CSV file
class RockSatSensor:
    # Initialize the sensor on the i2c bus
    def __init__(self):
        pass

    # Get the data column labels for the data returned by this sensor
    def getHeader(self):
        return self.header
        pass

    # Poll for the next dataset from this sensor
    def poll(self):
        pass

# Main sensor thread
def main(bootTime):
    # Get the active logging object
    logger = logging.getLogger(__name__)

    # Log from this new thread
    logger.info("Started sensor thread")

    # Start the I2C interface for the sensors
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        logging.info('Started I2C interface for sensors')
    except:
        logging.critical('Failed to enable i2c interface, the sensor thread will now crash')
        return

    # Desired sensors
    desiredSensors = [
        BME680,             # Temperature, Humidity, Pressure and Gas Sensor
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
        except:
            # Log failure
            logger.critical(f"Failed to initialize {Sensor.__name__} over I2C")
    logger.info("Finished initializing sensors")

    # MLX90640 Thermal Camera (special)
    mlx = None
    try:
        # Start the sensor
        mlx = MLX90640(i2c)
        logger.info("Initialized MLX90640 thermal camera")
    except:
        # Log failure
        logger.critical("Failed to initialize MLX90640 thermal camera")

    # Create the data file
    logger.info(f"Writing sensor data to file: ./data/sensors_{str(int(bootTime))}.csv")
    os.system("mkdir -p data")
    dataFile = open(f"data/sensors_{str(int(bootTime))}.csv", "a")

    # Create the MLX thermal camera data file
    mlxDataFile = None
    if mlx != None:
        logger.info(f"Writing MLX thermal camera frames to file: ./data/mlx_{str(int(bootTime))}.rstf") # rstf -> RockSat thermal frame
        mlxDataFile = open(f"data/mlx_{str(int(bootTime))}.rstf", "a")

    # Configure the order of the columns in the CSV file
    sensorOrder = []
    # For each sensor in the list of sensors, add the label elements in the header array 
    for sensor in sensors: sensorOrder = sensorOrder + sensor.getHeader()

    # Write the header line to the CSV file as the first line
    dataFile.write(sensorOrder.join(",") + "\n")

    # Try/Except block to catch KeyboardInterrupt eg. SIGTERM
    try:
        # Keep polling sensors forever
        while True:
            # Poll all sensors
            data = {}
            for sensor in sensors:
                # Add the sensor data to the current data
                data = dict(data, **sensor.poll)

            # Construct the CSV line
            csvLine = ""
            i = 0
            for column in sensorOrder:
                # Get the data for this column
                csvLine += data[column]
                # Add a comma unless this is the last value
                if i != len(sensorOrder) - 1: csvLine += ","
            csvLine += "\n"

            # Construct a line for the MLX thermal camera
            mlxLine = f"{data['Time']} --> {mlx.poll().join(',')}" if mlx != None else None

            # Write the CSV line to the file
            dataFile.write(csvLine)
            if mlx != None: mlxDataFile.write(mlxLine)
            # Force a flush to ensure that no data is being built up in the memory buffer that could be lost during power failure
            dataFile.flush()
            if mlx != None: mlxDataFile.flush()
    # Capture SIGTERM
    except KeyboardInterrupt:
        logger.warning("Received SIGTERM, writing final data to file and terminating sensor thread")
        if mlx != None: mlxDataFile.close()
        dataFile.close()
        return
