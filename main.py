"""
    RockSat-X 2022/2023 Payload Control Code

    main.py - This file is the main entry point for the payload control software.
        The systemd unit file calls this file and from here all of the child threads for sensor data logging
        and motor control are created. The "global" objects for the i2c bus, the logging module, etc. are inherited
        by the threads that need them. This helps prevent the issues of multiple threads trying to mess with the
        GPIO, RS232, and I2C independently all at once which can cause a number of problems.

        Once all setup is completed and all child threads are created, the main thread enters a while loop in which
        it listens to the GPIO pins responsible for timer events. Once certain conditions are met, this main control file
        will trigger arm movement, camera actions, and safely shut things down before splashdown.

    Contributors:
        Vu Dang
        Sean Sharp
        Angela Gabay
        Gage Gunn
        Konstantin Zaremski <kzaremski@student.cccs.edu> <konstantin.zaremski@gmail.com>

    Operation:
        If any arguments are given, the payload will only run those specific functions. For example, if no arguments are given,
        the payload will run everything. If only --sensors is given, then the payload will only run the sensor thread. If only
        --motor is given, the payload will run only the arm extension. If --sensors and --motor are supplied at the command line,
        the sensor and motor functionality will be run.

            $ python main.py                         # runs everything (flight mode or full test)
            $ python main.py --reset                 # runs everything starting from the beginning (most common for testing)
            $ python main.py --sensors               # only runs sensors
            $ python main.py --motor                 # only runs motor extension
            $ python main.py --sensors --motor       # runs both sensor and motor functionality
            $ python main.py --motor --sensors       # order of arguments makes no difference
        
        (no arguments)
            Run all functions of the payload. To be used for full testing or flight mode.

        --debug
            Debug mode. Does not shut down the Pi after splashdown condition as to not inconvenience the tester.

        --reset
            Resets the persistence file of the payload. If reset is not supplied, the payload will assume power failure and resume from
            the timer event or condition stored in the persistence file. To manually reset the payload from the command line without
            quitting, delete the 'state' file from 'RockSat2022-23'.

        --sensors
            Runs the sensor thread. This will run all sensors and output data to the ./data directory.

        --thermal
            Runs the thermal camera thread. This will run the thermal camera over I2C and output frames to a file in the ./data directory.

        --aux-camera
            Records using the auxiliary camera.
        
        --motor
            Throttles the motor and obeys the signals of the physical limit switches.
        
        --camera
            Controls the GoPro via solid state relay based on the timer events that are supplied by external power.

        --telemetry
            Communicates live sensor data over RS232. This option is not useful without also using --sensors.

    Note Regarding File Paths:
        This file and the remainder fo the program make use of relative pathing eg. "./".

        This program expects that the working directory is "/home/pi/RockSat2022-23", which is what is configured in the
        systemd service unit file.

    Note Regarding Dates & Timestamps:
        Log and data files are timestamped with the start time of the script in UNIX seconds rounded down to the nearest second.
        This makes it easier to corroborate the data from the sensors with the respective log files. 

    Timer Events:
        GSE     T-30s             Payload powers on and all relevant threads are started. Begins camera recording and data collection.
        TE-2    T+20s             Extend the 360-camera arm.
        TE-3    T+30s             Retract the 360-camera arm.
                TE-3+30s          Cycle GoPro recording to force file saving. Safe shutdown of payload control computer and other
                                  electronic hardware.
"""

# Import dependencies
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import configparser
import multiprocessing as multiprocessing
import sys
import datetime

# RPi GPIO
import RPi.GPIO as GPIO
import busio
import board

# MotorKit
from adafruit_motorkit import MotorKit

# Import RockSat experiment modules
import sensors.sensors as sensors
import sensors.thermal as thermal
import persist
from telemetry import Telemetry

# Main Method    str(datetime.datetime.now().strftime("%Y-%m-%d T%H:%M:%S"))
def main(commandLineArguments):
    # Initialize the logging module and log the startup time of the payload in the UNIX epoch
    #   Create a log folder if it does not exist yet
    os.system("mkdir -p logs")
    #   Get the boot time
    bootTime = time.time()
    #   Rotating file handler (large file size, so logs will probably not be rotated)
    rotatingFileHandler = RotatingFileHandler(
        filename=f"logs/payload_log_{str(int(bootTime))}.log",
        mode="a",
        maxBytes=20 * 1024 * 1024,
        backupCount=2,
        encoding="utf-8",
        delay=0
    )
    #   By default, log at the debug level using the file handler that was created
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s.%(msecs)03d][%(module)7s][%(levelname)8s]\t%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[rotatingFileHandler]
    )
    #   In addition to outputting to the file, output all logs to console so they can be viewed live while debugging
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    #   Acquire the active logger
    logger = logging.getLogger(__name__)
    #   Finally, log the boot time of the payload    
    logger.info(f"Launched from command: {' '.join(commandLineArguments)}")
    logger.info(f'CC of CO payload finished booting at {round(bootTime * 1000)} (UNIX millis)')

    # Reset the persisting state if they have flagged to do so
    if "--reset" in commandLineArguments:
        logger.info("Cleared persisting state")
        os.system("rm -f state")

    # Load previous state
    currentState = persist.read()
    if currentState: logger.warning(f"Persisting state detected ({currentState}). Possible power failure has occurred.")
    else: logger.info("No persisting state was detected, proceeding with normal execution order")

    # Identify power failures
    powerFailed = True if currentState != None else False
    if powerFailed:
        logger.warning("Possible power failure detected: persisting state implies shutdown before splashdown conditions")

    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('./config.ini')
    
    # Load pins from config
    TE_2 = int(config['Timer Event']['TE_2'])                   # Spacecraft Battery Bus Timer Event (TE-2)
    TE_3 = int(config['Timer Event']['TE_3'])                   # Spacecraft Battery Bus Timer Event (TE-3)
    EXTEND_LIMIT = int(config['Limit Switch']['EXTENDED'])      # Arm Extension Limit Switch
    RETRACT_LIMIT = int(config['Limit Switch']['RETRACTED'])    # Arm Retraction Limit Switch
    INHIBIT_1 = int(config['Inhibitor']['INHIBIT_1'])           # Flight Arm Inhibit
    CAMERA = int(config['Camera Control']['CAMERA'])            # Camera Control
    # Load timing config
    POST_TE_3_DWELL_TIME_SECONDS = int(config["Timing"]["TE_3_SHUTDOWN_DWELL"])
    if "--debug" in commandLineArguments: POST_TE_3_DWELL_TIME_SECONDS = 30
    # Notify
    logger.info("Loaded configuration from 'config.ini'")

    # Initialize multiprocessing
    multiprocessing.set_start_method("fork")
    processQueue = multiprocessing.Queue()
    logger.info("Initialized multiprocessing")

    # Handle command line arguments
    #   If no arguments are given when the file is run from the command line, run all functions
    runAll = len(commandLineArguments) == 1
    #   Telemetry
    telemetry = None
    if "--telemetry" in commandLineArguments or runAll:
        telemetry = Telemetry()
        telemetry.transmit("Hello Wallops")
    #   Sensors
    sensorThread = None # Initialized to a None value so that it can be skipped when exiting (if it is not run)
    if '--sensors' in commandLineArguments or runAll:
        sensorThread = multiprocessing.Process(target=sensors.main, args=[bootTime, telemetry])
        sensorThread.start()
    #   Thermal Camera
    thermalThread = None # Initialized to a None value so that it can be skipped when exiting (if it is not run)
    if '--thermal' in commandLineArguments or runAll:
        thermalThread = multiprocessing.Process(target=thermal.main, args=[bootTime, telemetry])
        thermalThread.start()

    # Configure the GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TE_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(TE_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(EXTEND_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RETRACT_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(INHIBIT_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(CAMERA, GPIO.OUT)
    logger.info("Configured GPIO")

    # Shorthand functions for conditions
    def armExtended(): return GPIO.input(EXTEND_LIMIT) == 1
    def armRetracted(): return GPIO.input(RETRACT_LIMIT) == 1
    def inhibit(): return GPIO.input(INHIBIT_1) == 1
    def TE(id):
        if id == 2: return GPIO.input(TE_2) == 1
        if id == 3: return GPIO.input(TE_3) == 1

    # Configure MotorKit
    motorKit = MotorKit(i2c=busio.I2C(board.SCL, board.SDA))
    arm = motorKit.motor1

    # Arm Extension & Retraction Methods
    def extendArm():
        try:
            # If extend limit switch not hit, extend (positive throttle),
            # Otherwise, return True to signify extension
            if not armExtended():
                arm.throttle = 1
                time.sleep(1)
                while arm.throttle == 1:
                    # Once extend limit is hit, set throttle to 0 and return True to signify extension
                    # If the arm does not finish extending by the time that TE-3 triggers, just stop moving it as now we have to retract
                    if armExtended() or TE(3):
                        arm.throttle = 0
                        if telemetry: telemetry.transmit("Extension limit switch hit")
                        return True
            else: return True
        except: return False
    def retractArm():
        try:
            # If extend limit switch not hit, retract (negative throttle),
            # Otherwise, return True to signify retraction
            if not armRetracted():
                arm.throttle = -1
                time.sleep(1)
                while arm.throttle == -1:
                    # Once retract limit is hit, set throttle to 0 and return True to signify retraction
                    if armRetracted():
                        arm.throttle = 0
                        if telemetry: telemetry.transmit("Retraction limit switch hit")
                        return True
            else: return True
        except: return False

    # Camera Control
    def toggleRecord():
        GPIO.output(CAMERA, GPIO.HIGH)
        time.sleep(1.25)
        GPIO.output(CAMERA, GPIO.LOW)
    
    # Check if inhibitor pin set
    inhibited = inhibit()
    if inhibited:
        logger.warning("Testing inhibitor pin is active, arm motor will not move")
        logger.warning("Testing inhibitor pin is active, persisting state cleared")
        persist.clear()
        currentState = persist.read()

    # If camera is in scope of operation, toggle recording on
    if ("--camera" in commandLineArguments or runAll) and not powerFailed:
        toggleRecord()
        logger.info("Toggled main camera recording on")
        if telemetry: telemetry.transmit("Camera Toggle Record On")

    # Keep looping and take action based on the timer events.
    operating = True
    logger.info("Finished loading other functionality, now listening to timer events coming from the spacecraft battery bus")
    TE3time = 0
    while operating:
        # If TE-2 pin fires
        if TE(2) and (not currentState or currentState == "TE-2"):
            if telemetry: telemetry.transmit("TE-2 Triggered")
            logger.info("Battery bus timer event TE-2 triggered")
            # Set current state
            currentState = "TE-2"
            if not inhibited: persist.set(currentState)
            # Extend the arm
            if ("--motor" in commandLineArguments or runAll) and not inhibited:
                logger.info("Starting camera arm extension")
                extendArm() 
                logger.info("Camera arm extended")
                if telemetry: telemetry.transmit("Extension limit switch hit")
            # Mark the system as ready for the next event
            currentState = "TE-2_Done"
            if not inhibited: persist.set(currentState)
            # Notify complete
            logger.info("TE-2 tasks completed")
        # If TE-3 pin fires
        if (TE(3) and currentState == "TE-2_Done") or currentState == "TE-3":
            if telemetry: telemetry.transmit("TE-3 Triggered")
            logger.info("Battery bus timer event TE-3 triggered")
            # Log the time that TE-3 fired
            TE3time = time.time()
            # Set current state
            currentState = "TE-3"
            if not inhibited: persist.set(currentState)
            # Retract the arm
            if ("--motor" in commandLineArguments or runAll) and not inhibited:
                logger.info("Starting camera arm retraction")
                retractArm() 
                logger.info("Camera arm retracted")
            # Mark the system as ready for the next event
            currentState = "TE-3_Done"
            if not inhibited: persist.set(currentState)
            # Notify complete
            logger.info("TE-3 tasks completed")
        # 30 seconds after TE-3, safe shutdown
        if time.time() - TE3time > POST_TE_3_DWELL_TIME_SECONDS and currentState == "TE-3_Done":
            if telemetry: telemetry.transmit(f"Post TE-3 dwell complete")
            logger.info(f"It is now {str(POST_TE_3_DWELL_TIME_SECONDS)} seconds after TE-3, beginning safe shutdown in preparation for splashdown")
            operating = False

    # Stop the thermal thread
    if thermalThread != None:
        thermalThread.terminate()
        thermalThread.join()
        thermalThread.close()
        logger.info("Finished stopping thermal camera thread")
        if telemetry: telemetry.transmit("Stopped sensors")

    # Stop the sensor thread
    if sensorThread != None:
        sensorThread.terminate()
        sensorThread.join()
        sensorThread.close()
        logger.info("Finished stopping sensor thread")
        if telemetry: telemetry.transmit("Stopped thermal camera")
    
    # If camera is in scope of operation, toggle recording on
    if "--camera" in commandLineArguments or runAll:
        toggleRecord()
        logger.info("Toggled main camera recording off")
        if telemetry: telemetry.transmit("Camera Toggle Record Off")

    # Clear persistence flag regardless of inhibitor state (if we have reached splashdown, just take it from the top)
    #   The reason for this is that the camera has stopped recording and it is already to start clean
    persist.clear()

    # If inhibitor was changed during operation, that means that we do not want to shutdown (eg. want a shell)
    if inhibited and not inhibit():
        logger.warning("Inhibitor pin, which was originally connected, was disconnected during operation signalling the desire to keep the Pi on after this test run")
        return True
    elif not inhibited and inhibit():
        logger.warning("Inhibitor pin, which was originally disconnected, was connected during operation signalling the desire to keep the Pi on after this test run")
        return True
    
    # Shutdown the pi
    if "--debug" not in commandLineArguments:
        logger.info("Shutting down electronics in preparation for splashdown!")
        time.sleep(1)
        os.system("shutdown -h now")
        return
    else:
        logger.info("--debug flag detected, electronics will not be shut down. Exiting script...")
        return

# If this file is run on its own (which it will be, run the main method) 
if __name__ == "__main__":
    main(sys.argv)
