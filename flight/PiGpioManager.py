from IGpioManager import IGpioManager
import RPi.GPIO as GPIO

class PiGpioManager(IGpioManager):
    def __init__(self, inputGpios, outputGpios, mode="BCM"):
        super.__init__(GPIO)
        # set the GPIO mode, BOARD or BCM
        if (mode == "BCM"):
            self._gpioController.setmode(GPIO.BCM)
        else:
            self._gpioController.setmode(GPIO.BOARD)
        
        # set up the input GPIOs
        for pin in inputGpios:
            self._gpioController.setup(pin, GPIO.IN)
            
        # set up the output GPIOs
        for pin in outputGpios:
            self._gpioController.setup(pin, GPIO.OUT)
            
        self._inputPins = inputGpios
        self._outputPins = outputGpios
        
    def read(self, gpioPin):
        # TODO : do some logging here to indicate function was called
        if (gpioPin not in self._inputPins):
            # do some logging here to indicate failure
            return False 
        return self._gpioController.input(gpioPin)
    
    def write(self, gpioPin, state):
        # TODO : do some logging here to indicate function was called
        if (gpioPin not in self._outputPins):
            # TODO : do some logging here to indicate that gpioPin input is incorrect
            return False
        if (state not in [True, False]):
            # TODO : do some logging here to indicate state is not correct
            return False
        self._gpioController.output(gpioPin, state)
        # if operation was successful, return true
        return True