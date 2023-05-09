"""
    BME680
        Temperature, Humidity, Pressure and Gas Sensor
"""


# Base RockSatSensor Class
from sensors import RockSatSensor

# Adafruit Library for the BME680
import adafruit_bme680

# BME680 Object
class BME680(RockSatSensor):
    def __init__(self, i2c):
        # Configure the sensor on the supplied i2c bus
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
        # Define the header
        self.header = [
            "BME680 Temperature",
            "BME680 Gas",
            "BME680 Relative Humidity",
            "BME680 Pressure",
            "BME680 Altitude",
        ]

    def getHeader(self):
        return self.header
    
    def poll(self):
        return {
            "BME680 Temperature": self.bme680.temperature,
            "BME680 Gas": self.bme680.gas,
            "BME680 Relative Humidity": self.bme680.relative_humidity,
            "BME680 Pressure": self.bme680.pressure,
            "BME680 Altitude": self.bme680.altitude,
        }
