import board 
import busio
import digitalio
import adafruit_bme680
import Bme680Interface
import time

cs=digitalio.DigitalInOut(board.D5)
spi=busio.SPI(board.SCLK,board.MOSI,board.MISO)
bme = adafruit_bme680.Adafruit_BME680_SPI(spi,cs)

bme_interface = Bme680Interface.Bme680Interface("BME", bme, sample_rate=1)

bme_interface.start_data_collection()

time.sleep(20)

bme_interface.stop_data_collection()


