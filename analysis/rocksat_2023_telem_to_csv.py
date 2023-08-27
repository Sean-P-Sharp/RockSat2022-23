#/usr/bin/python
"""
    Konstantin Zaremski <konstantin.zaremski@gmail.com>
                        <kzaremsk@msudenver.edu>
                        <kzaremski@student.cccs.edu>
    
    August 18, 2023

    CC of CO RockSat-X 2022-23 Telemetry to CSV Converter
        This simple python program converts the archaic telemetry format 
        that the payload transmits in to CSV data for import in to MS Excel
        or another program for data analysis.

    Operation
        rocksat_2023_telem_to_csv.py <input_file_path> <output_file_path>
            This is the default behavior and usage of the program. The first
            option should be the absolute or relative path to the telemetry
            output file provided by NASA telemetry engineers or techs. The 
            second option should be the output file (csv format) that contains
            the converted telemetry sensor data.

        rocksat_2023_telem_to_csv.py <input_file_path> <output_file_path>
                -l <log_output_file_path>
        rocksat_2023_telem_to_csv.py <input_file_path> <output_file_path>
                --log <log_output_file_path>
            If you desire to have payload log events extracted from the
            telemetry output, use the option "-l" or "--log", followed by 
            an additional output file path where the log events that have
            been extracted will be saved in plain text format.


"""

# Import dependencies
import sys

# Map telemetry variables against their sensor counterparts
sensors = {
    "t": "Time",
    "T_i": "BME680 (Internal) Temperature",
    "T_e": "BME680 (External) Temperature",
    "d": "VL54L0X Distance",
    "a_x": "BNO055 Acceleration (x)",
    "a_y": "BNO055 Acceleration (y)",
    "a_z": "BNO055 Acceleration (z)",
}

# Main Method
def main(args):
    # Empty Variables    
    inPath = None
    outPath = None
    logPath = None
    # Parse Arguments
    if len(args) == 0:
        return print("Please specity input and output file paths.")
    elif len(args) == 1:
        return print("Please specify an output path.")
    # Primary Operation Mode, set the arguments
    elif len(args) == 2:
        inPath = args[0]
        outPath = args[1]
    elif len(args) == 3 and (arg[2] == "-l" or arg[2] == "--log"):
        return print("Please specify an output path for the payload log file since you have elected to export it with \"-l\" or \"--log\"!")
    # Mode that includes the logfile
    else:
        inPath = args[0]
        outPath = args[1]
        logPath = args[3]

    # Empty arrays representing the lines of the respective output files
    dataLines = [",".join(sensors.values())]
    logLines = []

    # Read in the input file
    inputBlobString = []
    with open(inPath, "r", errors="ignore") as inputFile:
        # Read in all the lines at once and then close the file
        #   The payload does not produce telemtry data at the scale 
        #   that we would be needing to read in the file chunks at a time.
        inputBlobString = inputFile.read()

    # Clean up the file prior to input
    #   Trim newlines
    inputBlobString = inputBlobString.replace("\n", "")
    #   Trim off the opening brackets
    inputBlobString = inputBlobString.replace("[", "")
    #   Trim off NASA/Wallops additions
    inputBlobString = inputBlobString.replace("%% Header %%", "")
    inputBlobString = inputBlobString.replace("%%        %%", "")
    
    # Split in to lines based on the closing brackets
    inputLines = inputBlobString.split("]")

    # Data Messages
    dataObjects = []

    # For each line
    for telemetryMessage in inputLines:
        # Split the line
        messageParts = telemetryMessage.split(">")
        # If invalid, skip
        if len(messageParts) != 2:
            continue
        
        # Extract the time that the payload says that it sent the message
        payloadTime = messageParts[0]
        # Determine if it is a log line or data line
        messageString = messageParts[1]
        dataLine = messageString[0:2] == "d:" or (messageString[1] == "_" and messageString[3] == ":") 

        # If is a data line, parse as such
        if dataLine:
            # Data Message
            dataObject = {}
            # Individual measurements
            measurements = messageParts[1].split(",")
            # For each measurement
            for measurement in measurements:
                # Split the measurement in to its respective key-value pair
                measurementParts = measurement.split(":")
                if len(measurementParts) != 2:
                    print(f"INVALID: {measurement}")
                    continue
                # Add it to the data object
                dataObject[sensors[measurementParts[0]]] = measurementParts[1]
            # Time for the measurements
            dataObject["Time"] = payloadTime
            # Add the dataObject to the dataObjects array
            dataObjects.append(dataObject)
        # Otherwise, it is a log line, parse as such
        else:
            outLine = f"[{payloadTime}] {messageString}"
            logLines.append(outLine)

    # For each data element
    for dataObject in dataObjects:
        dataLine = ""
        # For each column in the header
        for sensor in sensors.values():
            if sensor in dataObject.keys():
                dataLine = dataLine + str(dataObject[sensor]) + ","
            else:
                dataLine = dataLine + ","
        # Add the data line to the dataLins
        dataLine = dataLine[:-1]
        dataLines.append(dataLine)

    # Write to the output files
    if outPath != None:
        with open(outPath, "w") as file:
            file.write("\n".join(dataLines) + "\n")
    if logPath != None:
        with open(logPath, "w") as file:
            file.write("\n".join(logLines) + "\n")

    # Print a message to the user
    print("Done!")

# Runtime (if being run directly and not being imported by another file)
if __name__ == "__main__":
    main(sys.argv[1:])

