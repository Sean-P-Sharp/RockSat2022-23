'''
RRCC/ACC Rocksat-X 2023
Data Handling Framework

This file will
1. Create all necessary folders for data storage
2. Allow files to be created (named ID [date(m-d-y)]_[time(h-m-s)])
3. Allow data to be written to said files
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
        current_time = datetime.now().strftime("%m-%d-%Y_%Hhr-%Mmin-%Ssec")
        stop_char = ' '
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


### Variables ###
folders = ["BME680", "9DOF", "MLX90640", "Aux Camera", "Geiger Counter", "SEN14722"]
subfolders = {
    "BME680": ["Gas", "Humidity", "Pressure", "Temperature"],
    "9DOF": ["Accelerometer", "Magnetometer", "Gyroscope"]
}



### Main ###
#Create folders
file_structure = FileStructure(r"C:\Users\Gage\Desktop\Data", folders, subfolders)
file_structure.create_folders()



#   Note
#To write to a singular file while a sensor is activated, use a while loop that runs while a sensor is turned on. Close file once sensor is deactivated and break while loop


#Test
# test_number = str(20)
# file_structure.write_to_file("BME680", "Temperature", test_number) #Write to a subfolder
# file_structure.write_to_file('MLX90640', '', test_number) #Write to a folder

