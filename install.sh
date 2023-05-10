#!/bin/sh
# RockSat 2022-23 Install Script
#   The purpose of this file is to automate the setup of the project on
#   a new Raspberry Pi.

# Nofity user instructions
echo "Please make sure that you are running this script as the root user, eg. 'sudo install.sh'"

# Enable root login over ssh
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# Disable sudo password (so that the payload can shut itself down)
# echo "pi ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# *** Install pip3 dependencies
pip3 install adafruit-blinka                    # Adafruit Circutpython, etc.
pip3 install adafruit-circuitpython-bno055      # Absolute Orientation Sensor
pip3 install adafruit-circuitpython-vl53l0x     # Time of Flight Distance/Ranging Sensor
pip3 install adafruit-circuitpython-lsm9ds1     # Accelerometer/Magnetometer/Gyroscope Sensor
pip3 install adafruit-circuitpython-bme680      # Temperature, Humidity, Pressure and Gas Sensor
pip3 install adafruit-circuitpython-mlx90640    # Infrared Thermal Camera Sensor

# Install the systemd unit file and notify the user of how to enable it
cp ~/rocksat.service /etc/systemd/system
echo "Installed systemd unit file to /etc/systemd/system"
echo "Do you wish to enable the service (the Pi will boot in to the program on next boot)? "
while true; do
    read -p "$* [y/n]: " yn
    case $yn in
        [Yy]*) systemctl enable rocksat.service ; echo "Enabled rocksat.service systemd unit file" ; break ;; 
        [Nn]*) echo "Service not enabled, when you need to, use 'sudo systemctl enable rocksat.service'" ; break ;;
    esac
done

# Notify completion
echo "* * * FINISHED INSTALLATION * * *"
