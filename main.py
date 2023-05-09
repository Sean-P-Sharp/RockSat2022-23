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
        ...

"""

# Import dependencies
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import multiprocessing as multiprocessing
import sys
import datetime

# Import RockSat experiment modules
import sensors.sensors as sensors

# Main Method    str(datetime.datetime.now().strftime("%Y-%m-%d T%H:%M:%S"))
def main(commandLineArguments):
    # Initialize the logging module and log the startup time of the payload in the UNIX epoch
    #   Create a log folder if it does not exist yet
    os.system("mkdir -p ./logs")
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
    logger.info(f'CC of CO payload finished booting at {round(bootTime * 1000)} (UNIX millis)')

    # Initialize multiprocessing
    multiprocessing.set_start_method('spawn')
    processQueue = multiprocessing.Queue()
    logger.info('Initialized multiprocessing')
    
    # Handle command line arguments
    #   If no arguments are given when the file is run from the command line, run all functions
    runAll = len(commandLineArguments) == 1
    #   Sensors
    sensorThread = None # Initialized to a None value so that it can be skipped when exiting (if it is not run)
    if '--sensors' in commandLineArguments or runAll:
        sensorThread = multiprocessing.Process(target=sensors.main, args=[bootTime])
        sensorThread.start()

    # Loop in place of timer event handling
    time.sleep(10)

    # Stop the sensor thread
    if sensorThread != None:
        sensorThread.terminate()
        sensorThread.join()
        sensorThread.close()
        logger.info("Finished stopping sensor thread")
    
    # Shutdown the pi
    if "--debug" not in commandLineArguments:
        logger.info("Shutting down electronics in preparation for splashdown!")
        time.sleep(1)
        os.system("sudo shutdown -h now")
        return
    else:
        logger.info("--debug flag detected, electronics will not be shut down. Exiting script...")
        return

# If this file is run on its own (which it will be, run the main method) 
if __name__ == "__main__":
    main(sys.argv)
