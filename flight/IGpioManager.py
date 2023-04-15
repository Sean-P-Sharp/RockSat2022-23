class IGpioManager:
    def __init__(self, gpioController):
        self._gpioController = gpioController
        
    def read(self, gpioPin):
        # TODO : instead of pass, do some logging here
        # to indicate that the base class function
        # was called which should have never happened
        pass
    
    def write(self, gpioPin, gpioValue):
        # TODO : instead of pass, do some logging here
        # to indicate that the base class function
        # was called which should have never happened
        pass