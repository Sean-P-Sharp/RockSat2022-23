import time
import serial

class Adafruit_Camera_Interface:
    def __init__(self, name, serial_port):
        self.name = name
        self.serial_port = serial_port
        
        self.serial = serial.Serial(self.serial_port, 38400)
        self.serial.write(b"\x56\x00\x26\x00")
        response = self.serial.read(5)
        if response != b"\x76\x00\x26\x00\x00":
            raise Exception("Failed to initialize camera")

    def capture_image(self, filename):
        self.serial.write(b"\x56\x00\x36\x01\x00")
        response = self.serial.read(5)
        if response != b"\x76\x00\x36\x00\x00":
            raise Exception("Failed to capture image")
        
        length = (ord(self.serial.read()) << 8) + ord(self.serial.read())
        data = self.serial.read(length)

        with open(filename, "wb") as f:
            f.write(data)