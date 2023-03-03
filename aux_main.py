import aux_interface
import os
import time

camera = aux_interface.Adafruit_Camera_Interface("Adafruit Camera", "/dev/ttyAMA0")

directory = os.path.expanduser("~/images")
if not os.path.exists(directory):
    os.makedirs(directory)

for i in range(5):
    filename = os.path.join(directory, "image{}.jpg".format(i))
    camera.capture_image(filename)
    print("Captured image {} to {}".format(i, filename))
    time.sleep(1)

'''
 Note that you'll need to specify the correct serial port for your camera in the Adafruit_Camera_Interface 
 You can find the serial port by running the 'ls /dev' command in a 
 terminal before and after plugging in the camera, and looking for the new device that appears. 
 On some Raspberry Pi models, the serial port may be /dev/ttyS0 instead of /dev/ttyAMA0.
'''