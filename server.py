#encoding: utf-8

#
'''
TODO list

Change time scale (sec -> milsec , float -> int)
Add shell script for operate Raspberry Pi3

'''
import time
from datetime import datetime
from MCP3208 import MCP3208
from fileSaveManager import FileSaveManager

#TODO Wait start Flag
# if raw_input()=='a':
#     exit()

start_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

#-----------------Initialize------------------
# class
spi = MCP3208(0)
fileSave = FileSaveManager(start_date)
# variable
dataSequence = []
startTime = time.time()
#---------------------------------------------

#-----------------Set Parameter------------------
frequency = 20 #Hz
saveSpan = 60 #sec
#------------------------------------------------


while True:
    #Get Data   20Hz(sum of integration)
    inputData = [datetime.now().strftime("%Y/%m/%d/%H:%M:%S:")+str(datetime.now().microsecond)] + spi.read_7ch(frequency)

    #TODO Gesture Recognition
    # inputData.append(gestureWasRecognized)

    dataSequence.append(inputData)

    # TODO for debug
    print inputData

    #Save data every 10 min to prevent data crashing (or program)
    if (time.time()-startTime) >= saveSpan:
        fileSave.save(datetime.now().strftime("%Y_%m_%d_%H:%M:%S:")+str(datetime.now().microsecond), dataSequence)
        #if Time 10min save Data sequence  data_seq=[time, ch1, ch2, ch3, ch4, GestureRecognition]
        # if fileSave.saveCSV(dataSequence) == 10:
        #     break
        # Initialize variable
        dataSequence = []
        startTime = time.time()
