# RRCC/ACC Rocksat-X 2023
# Data Storing TEST BUILD - Gage Gunn
# THIS FILE IS FOR DATE AND TIME IN FILE NAME

## Libraries ##
import os
from datetime import datetime


## Variables ##
ID = 1
current_time = datetime.now()
file_path = r'C:\home\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt'
folder_path = r'C:\home'
stop_char = ' '


## Main ##

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

files_list = [file for file in os.listdir(folder_path) if file.split(stop_char)[0] == str(ID)]

while files_list:
    print('File ' + str(ID) + ' already exists') # <<<<<< Can be removed to save data
    ID += 1
    files_list = [file for file in os.listdir(folder_path) if file.split(stop_char)[0] == str(ID)]
    
file_path = r'C:\DHM2\\' + str(ID) + ' ' + current_time.strftime('%m-%d-%Y_%Hhr-%Mmin-%Ssec') + '.txt' #Update the file path to the new ID
with open(file_path, 'w') as fp:
    fp.write('This is a test file with ID ' + str(ID)) # <<<<<< Change for
