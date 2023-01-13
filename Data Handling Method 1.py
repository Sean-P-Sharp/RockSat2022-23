# RRCC/ACC Rocksat-X 2023
# Data Storing TEST BUILD - Gage Gunn
# THIS FILE IS FOR DATE AND TIME NOT IN FILE NAME, RATHER PRINTED ON THE FIRST LINE


## Libraries ##
import os
from datetime import datetime


## Variables ##
ID = 1
current_time = datetime.now()
file_path = r'C:\Users\ggunn\Documents\DHM1\#' + str(ID) + '.txt'


## Main ## 
while True:
    if os.path.exists(file_path): #If file already exists
        ID += 1
        print('File already exists, now trying #' + str(ID))
        file_path = r'C:\Users\ggunn\Documents\DHM1\#' + str(ID) + '.txt' #Update the file path to the new ID
    else: #If file doesnt already exist
        with open(file_path, 'w') as fp:
            fp.write('Test   -   ')
            fp.write(current_time.strftime('%d-%m-%Y %Hhr-%Mmin-%Ssec'))
        break