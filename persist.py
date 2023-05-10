"""
    persist.py - Persistence module
        Simply reads from and writes to a state file.

    Ripped from CC of CO RockSat-X 2019-2021 Flight Code.
"""

# Import dependencies
import os

# Save a variable as the first line of the state file
def set(value):
    try:
        stateFile = open("state", "w")
        stateFile.write(str(value))
        stateFile.close()
        return True
    except:
        return False

# Read the state file and return the first line with no newline characters
def read():
    try:
        stateFile = open("state", "r")
        value = stateFile.readline().replace("\n", "")
        stateFile.close()
        return value
    except:
        return None

# Delete the state file so that None is returned when read
def clear():
    try:
        os.remove("state")
        return True
    except:
        return False