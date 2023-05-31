"""
    manualctl-web/app.py
        Manual control over the payload and the main control script from an easy-to-user web interface.

    Contributors:
        Konstantin Zaremski  <kzaremski@student.cccs.edu> <kzaremsk@msudenver.edu> <konstantin.zaremski@gmail.com>

    Based on Python flask.

    May 31, 2023
"""

# Import dependencies
from flask import Flask, render_template, send_from_directory
import time 
import json
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

# Initialize motor hat
 
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

# Motor Hat

# Static files
@app.route('/static/<path:path>')
def send_static_resource(path):
    return send_from_directory('static', path)
 
if __name__ == '__main__':
    # Run the server
    app.run()
