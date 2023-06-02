"""
    manualctl-web/app.py
        Manual control over the payload and the main control script from an easy-to-user web interface.

    Contributors:
        Konstantin Zaremski  <kzaremski@student.cccs.edu> <kzaremsk@msudenver.edu> <konstantin.zaremski@gmail.com>

    Based on Python flask.

    May 31, 2023
"""

# Import dependencies
from flask import Flask, render_template, send_from_directory, request
import time 
import json
import multiprocessing
import subprocess, signal
import os
# GPIO
import RPi.GPIO as GPIO
import busio
import board
 
# Flask app from the name of the current module.
app = Flask(__name__)

# Initialize GPIO inputs
inputPinNumbers = [
    4,
    18,
    27,
    22,
    23,
    24,
    25,
    5,
    6,
    12,
    13,
    16,
    19,
    20,
    21,
]
for pin in inputPinNumbers: GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize camera (GPIO output)
def toggleRecord():
    GPIO.output(CAMERA, GPIO.HIGH)
    time.sleep(1.25)
    GPIO.output(CAMERA, GPIO.LOW)

# MotorKit
from adafruit_motorkit import MotorKit
# Initialize motor hat
motorKit = MotorKit(i2c=busio.I2C(board.SCL, board.SDA))
arm = motorKit.motor1
arm.throttle = 0 # Reset motor
# Arm auto extension and retraction
def extendArm():
    arm.throttle = 1
    while arm.throttle == 1:
        if GPIO.input(23) == 1:
            arm.throttle = 0
def retractArm():
    arm.throttle = -1
    while arm.throttle == -1:
        if GPIO.input(27) == 1:
            arm.throttle = 0

# Threads
motorThread = None
cameraThread = None
softwareThread = None
currentLogFileName = None
multiprocessing.set_start_method("fork")
processQueue = multiprocessing.Queue()
 
# Root route
@app.route("/")
def index_route():
    return render_template("index.html")

# GPIO States (JSON)
@app.route("/api/gpio/inputstate")
def send_input_states():
    pinStates = {}
    for pin in inputPinNumbers:
        pinStates[str(pin)] = GPIO.input(pin) == 1
    return json.dumps(pinStates)

# Camera Toggle
@app.route("/api/camera/toggle")
def toggle_camera():
    cameraThread = multiprocessing.Process(target=toggleRecord, args=[])
    cameraThread.start()
    response = { "state": "complete" }
    return json.dumps(response)

# Motor Hat
@app.route("/api/motor")
def set_throttle():
    throttle = request.args.get("throttle")
    if throttle != None:
        try:
            motorThread.kill()
            motorThread.join()
        except:
            pass
        arm.throttle = float(throttle)
    response = {
        "throttle": str(arm.throttle)
    }
    return json.dumps(response)
@app.route("/api/arm/extend")
def extend_arm():
    try:
        motorThread.kill()
        motorThread.join()
    except:
        pass
    arm.throttle = 0
    motorThread = multiprocessing.Process(target=extendArm, args=[])
    motorThread.start()
    return json.dumps({"result": "true"})
@app.route("/api/arm/retract")
def extend_arm():
    try:
        motorThread.kill()
        motorThread.join()
    except:
        pass
    arm.throttle = 0
    motorThread = multiprocessing.Process(target=retractArm, args=[])
    motorThread.start()
    return json.dumps({"result": "true"})

# Software control API endpoints
@app.route("/api/software/start/<options:options>")
def start_software():
    if softwareThread == None or softwareThread.poll() == None:
        os.listdir("")
        softwareThread = subprocess.Popen(['/usr/bin/python /root/RockSat22-23/main.py'], pwd="/root/RockSat22-23/")
    return json.dumps({ "result": "true"})

@app.route("/api/software/log")
def get_software_log():
    if currentLogFileName == None: return json.dumps({ "log": "No log output at this time." })
    file = open(currentLogFileName,mode="r")
    logString = file.read()
    file.close()
    return json.dumps({ "log": logString })

@app.route("/api/software/kill")
def kill_software():
    if softwareThread != None and softwareThread.poll() != None:
        softwareThread.terminate()
        softwareThread.wait()
    return json.dumps({ "result": "true"})

# Static files
@app.route('/static/<path:path>')
def send_static_resource(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Run the server
    app.run()
