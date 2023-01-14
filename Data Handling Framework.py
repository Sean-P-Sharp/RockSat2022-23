# RRCC/ACC Rocksat-X 2023
# Data Handling Framework - Gage Gunn

### Plan ###
# 1. Create 'Data' folder
# 2. Create BME680, 9-DOF, MLX90640, Aux Camera, Geiger Counter, SEN14722 folders
# 3. Create sub folders where needed


### Libraries ###
import os
from datetime import datetime
import time

### Variables ###
ID = 1
stop_char = ' '
current_time = datetime.now()
bme_subfolders = ["Gas", "Humidity", "Pressure", "Temperature"]
dof_subfolders = ["Accelerometer", "Magnetometer", "Gyroscope"]



### Main ###
#Create Data folder
data_path = r"C:\Data"
if not os.path.exists(r'C:\Data\\'):
    os.makedirs(r'C:\Data\\')

#BME680 folder & subfolders
bme_path = r'C:\Data\BME680'
bme_fpath = r'C:\Data\BME680\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
for folder in ["BME680"]:
    path = os.path.join(data_path, folder)
    if not os.path.exists(path):
        os.makedirs(path)
    for subfolder in bme_subfolders:
        subpath = os.path.join(path, subfolder)
        if not os.path.exists(subpath):
            os.makedirs(subpath)
    file_paths = {subfolder: os.path.join(path, subfolder, f"{ID} {subfolder}_{current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec')}.txt") for subfolder in bme_subfolders}
    for subfolder, file_path in file_paths.items():
        open(file_path, "w").close()


#9-DOF folder
dof_path = r'C:\Data\9DOF'
dof_fpath = r'C:\Data\9DOF\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
for folder in ["9DOF"]:
    path = os.path.join(data_path, folder)
    if not os.path.exists(path):
        os.makedirs(path)
    for subfolder in dof_subfolders:
        subpath = os.path.join(path, subfolder)
        if not os.path.exists(subpath):
            os.makedirs(subpath)
    file_paths = {subfolder: os.path.join(path, subfolder, f"{ID} {subfolder}_{current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec')}.txt") for subfolder in dof_subfolders}
    for subfolder, file_path in file_paths.items():
        open(file_path, "w").close()
dof_flist = [file for file in os.listdir(dof_path) if file.split(stop_char)[0] == str(ID)]


#MLX90640 folder
mlx_path = r'C:\Data\MLX90640'
mlx_fpath = r'C:\Data\MLX90640\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
if not os.path.exists(mlx_path):
    os.makedirs(mlx_path)
mlx_flist = [file for file in os.listdir(mlx_path) if file.split(stop_char)[0] == str(ID)]


#Aux Camera folder
aux_path = r'C:\Data\Aux Camera'
aux_fpath = r'C:\Data\Aux Camera\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
if not os.path.exists(aux_path):
    os.makedirs(aux_path)
aux_flist = [file for file in os.listdir(aux_path) if file.split(stop_char)[0] == str(ID)]


#Geiger Counter folder
geiger_path = r'C:\Data\Geiger Counter'
geiger_fpath = r'C:\Data\Geiger Counter\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
if not os.path.exists(geiger_path):
    os.makedirs(geiger_path)
geiger_flist = [file for file in os.listdir(geiger_path) if file.split(stop_char)[0] == str(ID)]


#SEN14722 folder
sen_path = r'C:\Data\SEN14722'
sen_fpath = r'C:\Data\SEN14722\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
if not os.path.exists(sen_path):
    os.makedirs(sen_path)
sen_flist = [file for file in os.listdir(sen_path) if file.split(stop_char)[0] == str(ID)]




#Use code below for writing files (change each list with respective list)
# while files_list:
#     print('File ' + str(ID) + ' already exists') # <<<<<< Can be removed to save data
#     ID += 1
#     files_list = [file for file in os.listdir(folder_path) if file.split(stop_char)[0] == str(ID)]
    
# file_path = r'\home\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt' #Update the file path to the new ID
# with open(file_path, 'w') as fp:
#     fp.write('This is a test file with ID ' + str(ID))
