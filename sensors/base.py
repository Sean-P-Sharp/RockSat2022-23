"""
    base.py
        RockSatSensor template class.

        Moved to its own file to avoid circular dependency.
"""

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
