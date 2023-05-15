"""
    BME680
        Temperature, Humidity, Pressure and Gas Sensor
"""

# Base RockSatSensor Class
from sensors.base import RockSatSensor

# Adafruit Library for the BME680
import adafruit_bme680

# BME680 Object
class BME680(RockSatSensor):
    def __init__(self, i2c, addr):
        # Configure the sensor on the supplied i2c bus
        self.addr = addr
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, addr)
        # Define the header
        self.header = [
            f"BME680 0x{hex(self.addr)} Temperature",
            f"BME680 0x{hex(self.addr)} Gas",
            f"BME680 0x{hex(self.addr)} Relative Humidity",
            f"BME680 0x{hex(self.addr)} Pressure",
            f"BME680 0x{hex(self.addr)} Altitude",
        ]

    def getHeader(self):
        return self.header
    
    def poll(self):
        return {
            f"BME680 0x{hex(self.addr)} Temperature": self.bme680.temperature,
            f"BME680 0x{hex(self.addr)} Gas": self.bme680.gas,
            f"BME680 0x{hex(self.addr)} Relative Humidity": self.bme680.relative_humidity,
            f"BME680 0x{hex(self.addr)} Pressure": self.bme680.pressure,
            f"BME680 0x{hex(self.addr)} Altitude": self.bme680.altitude,
        }

# Internal BME680, address 0x76 (soldered back)
class BME680_Inside(BME680):
    def __init__(self, i2c):
        super().__init__(i2c, 0x76)

    def getHeader(self):
        return super().getHeader()

    def poll(self):
        return super().poll()

# External BME680, address 0x77 (unsoldered)
class BME680_Outside(BME680):
    def __init__(self, i2c):
        super().__init__(i2c, 0x77)

    def getHeader(self):
        return super().getHeader()

    def poll(self):
        return super().poll()
