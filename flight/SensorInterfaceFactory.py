from Bme680Interface import Bme680Interface
from Bno055Interface import Bno055Interface
from DofInterface import DofInterface
from ThermalCamInterface import ThermalCamInterface
import board 
import busio
import digitalio
import adafruit_bme680
import adafruit_bno055
import adafruit_lsm9ds1
import adafruit_mlx90640

class SensorInterfaceFactory:
    def __init__(self):
        self._bme_1_interface = None
        self._bme_2_interface = None
        self._bno_interface = None
        self._dof_interface = None
        self._mlx_interface = None
        self._i2c = board.I2C()
        self._bme_1 = None
        self._bme_2 = None
        self._bno = None
        self._dof = None
        self._mlx = None

    ### create the BME 1 Interface
    def createBme1Interface(self, sampleRate):
        if (self._bme_1 == None):
            try:
                self._bme_1 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76)
            except:
                # TODO : some kind of logging should be done here to indicate failure
                self._bme_1 = None

        if (self._bme_1_interface == None):
            if (self._bme_1 is not None):
                try:
                    self._bme_1_interface = Bme680Interface("BME_1", bme, sample_rate=sampleRate)
                except:
                    # TODO : some kind of logging should be done here to indicate failure
                    self._bme_1_interface = None
        # return the bme 1 interface object                    
        return self._bme_1_interface

    ### Create the BME 2 interface
    def createBme2Interface(self, sampleRate):
        # create the adafruit bme object if it hasn't been already
        if (self._bme_2 == None):
            try:
                self._bme_2 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
            except:
                # TODO : some kind of logging should be done here to indicate failure
                self._bme_2 = None

        if (self._bme_2_interface == None):
            # create the bme interface object if it hasn't been already
            if (self._bme_2 is not None):
                try:
                    # but only create it if the bme object was successfully created
                    self._bme_2_interface = Bme680Interface("BME_2", bme_2, sample_rate=sampleRate)
                except:
                    # TODO : some kind of logging should be done here to indicate failure
                    self._bme_2_interface = None
        # return the bme 2 interface object
        return self._bme_2_interface   

    def createBnoInterface(self, sampleRate):
        # create the adafruit bno object if it hasn't been already
        if (self._bno == None):
            try:
                self._bno = adafruit_bno055.BNO055_I2C(i2c)
            except:
                # TODO : some kind of logging should be done here to indicate failure
                self._bno = None

        if (self._bno_interface == None):
            # create the bme interface object if it hasn't been already
            if (self._bno is not None):
                try:
                    # but only create it if the bme object was successfully created
                    self._bno_interface = Bno055Interface("BNO", bno, sample_rate=bno_sample_rate)
                except:
                    # TODO : some kind of logging should be done here to indicate failure
                    self._bno_interface = None
        # return the bno interface object
        return self._bno_interface   

    def createDofInterface(self, sampleRate):
        # create the adafruit dof object if it hasn't been already
        if (self._dof == None):
            try:
                self._dof = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
            except:
                # TODO : some kind of logging should be done here to indicate failure
                self._dof = None

        if (self._dof_interface == None):
            # create the bme interface object if it hasn't been already
            if (self._dof is not None):
                try:
                    # but only create it if the bme object was successfully created
                    self._dof_interface = DofInterface("9DOF", dof, sample_rate=sampleRate)
                except:
                    # TODO : some kind of logging should be done here to indicate failure
                    self._dof_interface = None
        # return the dof interface object
        return self._dof_interface       

    def createMlxInterface(self, sampleRate):
        # create the adafruit mlx object if it hasn't been already
        if (self._mlx == None):
            try:
                self._mlx = adafruit_mlx90640.MLX90640(i2c)
            except:
                # TODO : some kind of logging should be done here to indicate failure
                self._mlx = None

        if (self._mlx_interface == None):
            # create the bme interface object if it hasn't been already
            if (self._mlx is not None):
                try:
                    # but only create it if the bme object was successfully created
                    self._mlx_interface = ThermalCamInterface("MLX90640", mlx, sample_rate=sampleRate)
                except:
                    # TODO : some kind of logging should be done here to indicate failure
                    self._mlx_interface = None
        # return the mlx interface object
        return self._mlx_interface   

    def createAllInterfaces(self, bme1SampleRate, bme2SampleRate, bnoSampleRate, dofSampleRate, mlxSampleRate):
        # create an array of interface objects
        return [self.createBme1Interface(bme1SampleRate), self.createBme2Interface(bme2SampleRate), self.createBnoInterface(bnoSampleRate), self.createDofInterface(dofSampleRate), self.createMlxInterface(mlxSampleRate)]                  
            

