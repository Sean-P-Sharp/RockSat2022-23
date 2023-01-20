'''
Data Handling Framework

RRCC/ACC Rocksat-X 2023
Data Handling Framework
This file will
1. Create all necessary folders for data storage
2. Allow files to be created (named ID [date(m-d-y)]_[time(h-m-s)])
3. Allow data to be written to said files

-----------------------------------------------------------------------

HOW TO USE
1. Create Folders - fs.create_folders() 
2. Create a new file - fs.write_to_file("Folder", "Sub Folder (if none just leave as '')", [value])
3. Write to the most recently created file - 
    folder_path = os.path.join(Main File Path, "Folder", "Subfolder") << If no subfolder, remove the last part
    file_path = highest_id_path[folder_path]
    with open(file_path, 'a') as file:
        file.write("\nAdditional data")

*Notes*
1. Make sure to assign correct file path to create folders to
'''


### Libraries ###
import os
from datetime import datetime

class FileStructure:
    def __init__(self, data_path, folders, subfolders):
        self.data_path = data_path
        self.folders = folders
        self.subfolders = subfolders
        self.ID = 1

    def create_folders(self):
        os.makedirs(self.data_path, exist_ok=True)
        for folder in self.folders:
            path = os.path.join(self.data_path, folder)
            os.makedirs(path, exist_ok=True)
            if folder in self.subfolders:
                for subfolder in self.subfolders[folder]:
                    subpath = os.path.join(path, subfolder)
                    os.makedirs(subpath, exist_ok=True)
        

    def write_to_file(self, folder_name, subfolder_name, data):
        while True:
            file_path = os.path.join(self.data_path, folder_name, subfolder_name, f"{self.ID} {current_time}.txt")
            folder_path = os.path.join(self.data_path, folder_name, subfolder_name)
            if [file for file in os.listdir(folder_path) if file.split(stop_char)[0] == str(self.ID)]:
                print(f"File with ID {self.ID} already exists.")
                self.ID += 1
            else:
                with open(file_path, 'w') as file:
                    file.write(data)
                self.ID = 1
                break
        
        find_highest_id(r"C:\Users\Gage\Desktop\Data")
            
    def flight_log(self, flog):
        while True:
            log_path = os.path.join(self.data_path, "_Flight Log")
            log_fpath = os.path.join(self.data_path, "_Flight Log", f"{self.ID} {current_time}.txt")
            if [file for file in os.listdir(log_path) if file.split(stop_char)[0] == str(self.ID)]:
                print(f"Flight Log with ID {self.ID} already exists.")
                self.ID += 1
            else:
                with open(log_fpath, 'w') as log:
                    log.write(flog)
                self.ID = 1
                break

### Functions ###
highest_id = 0
def find_highest_id(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            find_highest_id(item_path)
        else:
            # Check if the file name starts with an ID
            id = item.split(" ")[0]
            if id.isdigit():
                if fs.ID > highest_id:
                    highest_id_path[path] = item_path


### Variables ###
highest_id_path = {}
stop_char = ' '
current_time = datetime.now().strftime("%m-%d-%Y_%Hhr-%Mmin-%Ssec")
folders = ["BME680", "9DOF", "MLX90640", "PTC08", "Geiger Counter", "SEN14722", "_Flight Log", "VL53L1X"]
subfolders = {
    "BME680": ["Gas", "Humidity", "Pressure", "Temperature"],
    "9DOF": ["Accelerometer", "Magnetometer", "Gyroscope"]
}



### Main ###
#Create folders
fs = FileStructure(r"C:\Users\Gage\Desktop\Data", folders, subfolders)
fs.create_folders()
fs.flight_log('Folders have been created\n')



### Test Section ###
test_number = str(20)
test_flog = 'Testing'
fs.write_to_file("BME680", "Temperature", test_number) #Write to a subfolder
fs.write_to_file('MLX90640', '', test_number) #Write to a folder


#Test example for writing to the file with the highest ID in a given folder
folder_path = os.path.join(r"C:\Users\Gage\Desktop\Data", "MLX90640")
file_path = highest_id_path[folder_path]
with open(file_path, 'a') as file:
    file.write("\nAdditional data")
    


#Changes Needed
#1. Flight log will say "Folders have been created" every time, change so then it makes a note if folders have already been made
#2. Make a way to add to the flight log
#3. Change file name to something without spaces
