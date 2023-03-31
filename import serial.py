import serial

# Configure serial port
ser = serial.Serial(
    port= #replace with serial port name
    baudrate=19200
    timeout=1
)

#send the test string 
ser.write(b'Test String')

#Close serial port
ser.close()
