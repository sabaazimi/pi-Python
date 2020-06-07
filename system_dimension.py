# Property of KPM Power for the ANZEN Battery Management System
# Code developed by Saba Azimi
# Created: June 05, 2020
# Last Modified: 
# Modified by: 

import can
import time
import binascii
from datetime import datetime
import connect_can

NUMBER_OF_CELLS = 0 # change this to amount of cells
NUMBER_OF_THERMISTORS = 0 # cange this to amount of thermistors
NUMBER_OF_SLAVES = 0 

def create_batt_temp_request(): # send request for num cells and num thermistors
    batt_temp_send = can.Message(arbitration_id=0x181fe8f4, data=[
                            0x14, 0, 0, 0, 0, 0, 0, 0], extended_id=True)
    connect_can.can0.send_periodic(batt_temp_send, 0.20)

def get_num_batt_temp(): # get and store num cells and num thermistors
    global NUMBER_OF_CELLS
    global NUMBER_OF_THERMISTORS 
    global NUMBER_OF_SLAVES   
    for x in range(1000):
        create_batt_temp_request()
        message = connect_can.can0.recv(10.0)
        if message:   
            data = binascii.hexlify(message.data)
            frame = hex(message.arbitration_id)
            if frame[2:10] == "1814f4e8" and data[0:2] == "01":
                NUMBER_OF_CELLS = int(data[6:8], 16)
                NUMBER_OF_THERMISTORS = int(data[10:12], 16)
                NUMBER_OF_SLAVES = int(data[2:4] , 16)
                
                print("number of cell is ", NUMBER_OF_CELLS)
                print("number of thermoster is ", NUMBER_OF_THERMISTORS)
                print("number of SLAVES  is ", NUMBER_OF_SLAVES)

        else:
            NUMBER_OF_CELLS = 16
            NUMBER_OF_THERMISTORS = 4   
    # except AttributeError:
        # print("nothing found this time, continue ....")
    print("number of cells", NUMBER_OF_CELLS)
    print("number of Thermosters", NUMBER_OF_THERMISTORS)    





if __name__ == "__main__":
    get_num_batt_temp()