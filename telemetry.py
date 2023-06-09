"""
    telemetry.py
        Telemetry controller class. The reference to the object instantiated from this class can be passed
        around to whatever threads need it so that they can send around their own telemetry data.
"""

# Import dependencies
import serial
import logging
import time

# Telemetry class
class Telemetry:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ser = None
        try:
            self.ser = serial.Serial(
                port="/dev/ttyS0",
                baudrate=19200,
                timeout=1
            )
            self.logger.info("Opened RS232 interface for telemetry")
        except:
            self.logger.critical("Failed to open RS232 interface for telemetry")
            self.ser = None

    def transmit(self, message):
        # Do not send if failed to open
        if self.logger == None: return False
        
        # Message format [system time milliseconds>message]
        message = f"[{str(int(time.time() * 1000))}>{str(message)}]"
        
        # Attempt send/write to serial
        try:
            self.ser.write(bytes(message, "utf-8"))
        except Exception as e:
            self.logger.critical(f"Failed to send message {message} at {str(int(time.time() * 1000))}\nException: {str(e)}")
    
    def end(self, message):
        # Do not close if failed to open
        if self.logger == None: return False
        
        self.ser.close()
