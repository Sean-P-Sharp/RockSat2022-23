"""
    sensors.py - Sensor control file
"""

# Import dependencies
import logging
import time

# Adafruit circutpython
import board
import busio

# Import RockSat sensors


# Template for a basic RockSat sensor
#   Each sensor is going to need to return a dictionary containing the data returned by the sensor and an ordered array of the headers for the CSV file
class RockSatSensor:
    # Initialize the sensor on the i2c bus
    def __init__(self):
        pass

    # Get the data column labels for the data returned by this sensor
    def getHeader(self):
        self.headers
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

    # Start the 
    try :
        i2c = busio.I2C(board.SCL, board.SDA)
        logging.info('I2C interface of sensors... OK')
    except :
        logging.critical('Failed to enable i2c interface, the sensor thread will now crash')
        return

    # Empty sensor stack
    sensors = []

    # Add all of the sensors that we want
    sensors.append(None)

    # Create the data file

    