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



### Main ###
#Create Data folder
if not os.path.exists(r'\home\Data\\'):
    os.makedirs(r'\home\Data\\')

#BME680 folder
bme_path = r'\home\Data\BME680'
bme_fpath = r'\home\Data\BME680\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
if not os.path.exists(bme_path):
    os.makedirs(bme_path)
bme_flist = [file for file in os.listdir(bme_path) if file.split(stop_char)[0] == str(ID)]

if not os.path.exists(bme_path + '\Gas'): #Gas Folder
    os.makedirs(bme_path + '\Gas')
bme_gas_path = bme_path + '\Gas'
bme_gas_fpath = bme_gas_path + '\\' + str(ID) + ' ' + 'Gas_' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'

if not os.path.exists(bme_path + '\Humidity'): #Humidity Folder
    os.makedirs(bme_path + '\Humidity')
bme_humidity_path = bme_path + '\Humidity'
bme_humidity_fpath = bme_humidity_path + '\\' + str(ID) + ' ' + 'Humidity_' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'

if not os.path.exists(bme_path + '\Pressure'): #Pressure Folder
    os.makedirs(bme_path + '\Pressure')
bme_pressure_path = bme_path + '\Pressure'
bme_pressure_fpath = bme_pressure_path + '\\' + str(ID) + ' ' + 'Pressure_' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'

if not os.path.exists(bme_path + '\Temperature'): #Temperature Folder
    os.makedirs(bme_path + '\Temperature')
bme_temperature_path = bme_path + '\Temperature'
bme_temperature_fpath = bme_temperature_path + '\\' + str(ID) + ' ' + 'Temperature_' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'


#9-DOF folder
dof_path = r'\home\Data\9DOF'
dof_fpath = r'\home\Data\9DOF\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
if not os.path.exists(dof_path):
    os.makedirs(dof_path)
dof_flist = [file for file in os.listdir(dof_path) if file.split(stop_char)[0] == str(ID)]

if not os.path.exists(dof_path + '\Accelerometer'): #Accelerometer Folder
    os.makedirs(dof_path + '\Accelerometer')
dof_accelerometer_path = dof_path + '\Accelerometer'
dof_accelerometer_fpath = dof_accelerometer_path + '\\' + str(ID) + ' ' + 'Accelerometer_' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'

if not os.path.exists(dof_path + '\Magnetometer'): #Magnetometer Folder
    os.makedirs(dof_path + '\Magnetometer')
dof_magnetometer_path = dof_path + '\Magnetometer'
dof_magnetometer_fpath = dof_magnetometer_path + '\\' + str(ID) + ' ' + 'Magnetometer_' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'

if not os.path.exists(dof_path + '\Gyroscope'): #Gyroscope Folder
    os.makedirs(dof_path + '\Gyroscope')
dof_gyroscope_path = dof_path + '\Gyroscope'
dof_gyroscope_fpath = dof_gyroscope_path + '\\' + str(ID) + ' ' + 'Gyroscope_' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'


#MLX90640 folder
mlx_path = r'\home\Data\MLX90640'
mlx_fpath = r'\home\Data\MLX90640\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
if not os.path.exists(mlx_path):
    os.makedirs(mlx_path)
mlx_flist = [file for file in os.listdir(mlx_path) if file.split(stop_char)[0] == str(ID)]


#Aux Camera folder
aux_path = r'\home\Data\Aux Camera'
aux_fpath = r'\home\Data\Aux Camera\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
if not os.path.exists(aux_path):
    os.makedirs(aux_path)
aux_flist = [file for file in os.listdir(aux_path) if file.split(stop_char)[0] == str(ID)]


#Geiger Counter folder
geiger_path = r'\home\Data\Geiger Counter'
geiger_fpath = r'\home\Data\Geiger Counter\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
if not os.path.exists(geiger_path):
    os.makedirs(geiger_path)
geiger_flist = [file for file in os.listdir(geiger_path) if file.split(stop_char)[0] == str(ID)]


#SEN14722 folder
sen_path = r'\home\Data\SEN14722'
sen_fpath = r'\home\Data\SEN14722\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
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
