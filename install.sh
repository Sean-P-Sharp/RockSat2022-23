#!/bin/sh
# RockSat 2022-23 Install Script
#   The purpose of this file is to automate the setup of the project on
#   a new Raspberry Pi.

# Nofity user instructions
echo "Please make sure that you are running this script as the root user, eg. 'sudo install.sh'"

# *** Install pip3 dependencies
pip3 install adafruit-circuitpython-bno055
pip3 install adafruit-circuitpython-vl53l0x
pip3 install adafruit-circuitpython-lsm9ds1
pip3 install adafruit-circuitpython-bme680
pip3 install adafruit-circuitpython-mlx90640

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
