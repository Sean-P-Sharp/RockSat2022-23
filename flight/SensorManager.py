class SensorManager:
    """
    Used to control all the sensors
    """
    def __init__(self, SensorFactory, bme1SampleRate, bme2SampleRate, bnoSampleRate, dofSampleRate, mlxSampleRate):
        #SensorFactory : a SensorFactory object to create sensors
        self._sensors = SensorFactory.createAllInterfaces(bme1SampleRate, bme2SampleRate, bnoSampleRate, dofSampleRate, mlxSampleRate)
        
    def startSensors(self):
        for sensor in self._sensors:
            if (sensor is not None):
                sensor.start_data_collection()
            
    def stopSensors(self):
        for sensor in self._sensors:
            if (sensor is not None):
                sensor.stop_data_collection()