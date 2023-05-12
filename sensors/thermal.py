"""
    thermal.py
        Thermal camera control and recording file.
"""

# Import dependencies
import os
import time
import logging

# Adafruit circutpython
import board
import busio

# MLX RockSat sensor
from sensors.mlx90640 import MLX90640

# Thermal camera control thread
def main(bootTime, telemetry):
    # Acquire existing logger
    logger = logging.getLogger(__name__)
    # Log from this new thread
    logger.info("Started thermal camera thread")

    # Start an instance of the I2C interface for the thermal camera
    i2c = None
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        logger.info("Started I2C interface for thermal camera")
    except Exception as e:
        logger.critical("Failed to enable i2c interface, the thermal camera thread will now crash!")
        logger.critical(f"Exception: {e}")
        return

    mlx = None
    try:
        # Start the sensor
        mlx = MLX90640(i2c)
        logger.info("Initialized MLX90640 thermal camera")
    except Exception as e:
        # Log failure
        logger.critical(f"Failed to initialize MLX90640 thermal camera. Exception: {e}")
        logger.critical("MLX90640 thermal thread will now crash")
        return

    # Create the MLX thermal camera data file
    logger.info(f"Writing MLX thermal camera frames to file: ./data/mlx_{str(int(bootTime))}.rstf") # rstf -> RockSat thermal frame
    os.system("mkdir -p data")
    mlxDataFile = open(f"data/mlx_{str(int(bootTime))}.rstf", "a")

    # Try/Except block to catch KeyboardInterrupt eg. SIGTERM
    try:
        # Keep polling the thermal camera forever
        while True:
            # Construct a line for the MLX thermal camera
            mlxLine = f"{str(time.time() * 1000)} --> {','.join([str(x) for x in mlx.poll()['MLX90640 Thermal Frame']])}\n" if mlx != None else None

            # Write & flush
            mlxDataFile.write(mlxLine)
            mlxDataFile.flush()
    # Capture SIGTERM
    except KeyboardInterrupt:
        logger.warning("Received SIGTERM, writing final data to file and terminating thermal camera thread")
        mlxDataFile.close()
        return