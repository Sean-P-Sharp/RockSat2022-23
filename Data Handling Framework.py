# RRCC/ACC Rocksat-X 2023
# Data Handling Framework - Gage Gunn


### Libraries ###
import os
from datetime import datetime

### Variables ###
ID = 1
stop_char = ' '
current_time = datetime.now()
folders = ["BME680", "9DOF", "MLX90640", "Aux Camera", "Geiger Counter", "SEN14722"]
subfolders = {
    "BME680": ["Gas", "Humidity", "Pressure", "Temperature"],
    "9DOF": ["Accelerometer", "Magnetometer", "Gyroscope"]
}

### Main ###

# Create Data folder
data_path = r"C:\Data"
if not os.path.exists(data_path):
    os.makedirs(data_path)

# Create folders and Subfolders 
for folder in folders:
    path = os.path.join(data_path, folder)
    if not os.path.exists(path):
        os.makedirs(path)
    if folder in subfolders:
        for subfolder in subfolders[folder]:
            subpath = os.path.join(path, subfolder)
            if not os.path.exists(subpath):
                os.makedirs(subpath)




#Use code below for writing files (change each list with respective list)
# while files_list:
#     print('File ' + str(ID) + ' already exists') # <<<<<< Can be removed to save data
#     ID += 1
#     files_list = [file for file in os.listdir(folder_path) if file.split(stop_char)[0] == str(ID)]
    
# file_path = r'\home\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt' #Update the file path to the new ID
# with open(file_path, 'w') as fp:
#     fp.write('This is a test file with ID ' + str(ID))
