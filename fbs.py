import config
import json
import time
import can
import os
import connect_can #the .pyc and/or the .py file of this needs to be in the same folder for it to work
# import active_api
from datetime import datetime
import binascii
import FilteredBufferedReader
import Queue
import math

monobloc_v = []
monobloc_t = []
err_time_stamp = ""
error = ""
monobloc_flag = False
monobloc_t_flag = False
bcm_flag = False
master_flag = False


NUMBER_OF_CELLS = 38 # change this to amount of cells
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


# get_num_batt_temp()

bcm_data = []



def list_len(number_of_cells, number_of_data_per_line):
    return (math.ceil(number_of_cells/number_of_data_per_line))




#  CELL DATA----------------------------

fbr = FilteredBufferedReader.FilteredBufferedReader([0x1830cce8,0x1831cce8,0x1834cce8])
notifier = can.Notifier(connect_can.can0, [fbr])



def main():
    global monobloc_flag 
    global monobloc_t_flag
    global master_flag
    global bcm_flag
    global err_time_stamp
    global error
    monobloc_flag = False
    n = 1
    t = 1
    monobloc_t_flag = False
    master_flag = False
    bcm_flag = False
    # error = ""
    # err_time_stamp = ""
    for z in range(150):
        msg = fbr.get_message(0.05)
        # msg = connect_can.can0.recv(1.0)
        if msg:
            # print(msg)
            data = binascii.hexlify(msg.data)
            frame_id = hex(msg.arbitration_id)          
            if frame_id[2:10] == "1830cce8":
                if int(data[:2], 16) == n :
                    monobloc_v.append(data)
                if n < (list_len(NUMBER_OF_CELLS,3) + 2):
                    n += 1
                else:
                    del monobloc_v[:]
                    monobloc_flag =  False
                    # break
                if len(monobloc_v) > (list_len(NUMBER_OF_CELLS,3) + 2):
                    del monobloc_v[:]
                    monobloc_flag = False
                    n = 1
                if len(monobloc_v) == (list_len(NUMBER_OF_CELLS,3) + 1): 
                    monobloc_flag = True
                    # break
            if frame_id[2:10] == "1831cce8":
                if int(data[:2], 16) == t :
                    monobloc_t.append(data)
                if t < 8 :
                    t += 1
                else:
                    del monobloc_t[:]
                    monobloc_t_flag =  False
                    # break
                if len(monobloc_t) > (list_len(NUMBER_OF_CELLS,6) + 2):
                    del monobloc_t[:]
                    monobloc_t_flag = False
                    t = 1
                if len(monobloc_t) == (list_len(NUMBER_OF_CELLS,6) + 1):
                    monobloc_t_flag = True
                    # break                 
            if frame_id[2:10] == "1834cce8":
                if data[:2] == "01" and len(bcm_data) == 0:
                    bcm_data.append(data)
                    if data[8:10] != error:
                        err_time_stamp = datetime.utcnow().isoformat()
                        error = data[8:10]

                if data[:2] == "02" and len(bcm_data) == 1 :
                    bcm_data.append(data)
                if data[:2] == "03" and len(bcm_data) == 2 :
                    bcm_data.append( data)
                if data[:2] == "04" and len(bcm_data) == 3 :
                    bcm_data.append(data)
            # print(bcm_data)
            if len(bcm_data) == 4 :
                master_flag = True
        # print("master data", bcm_data)
        # print("voltage", monobloc_v)
        # print("temp", monobloc_t)
        # print("master flag", master_flag)
        # print("temp_flag",monobloc_t_flag )
        # print("voltage flag", monobloc_flag)
        # print("-----------------------------------------------------------")
        if master_flag == True and monobloc_flag == True and monobloc_t_flag == True:
            bcm_flag = True
            connect_can.can0.flush_tx_buffer()
            break

def reset_param():
    global bcm_flag
    global monobloc_t_flag
    global monobloc_flag
    bcm_flag = False
    monobloc_t_flag = False
    monobloc_flag = False
    master_flag = False
    del bcm_data[:]
    del monobloc_t[:]
    del monobloc_v[:]

if __name__ == "__main__":
    while True:
        main()
        if bcm_flag == True:
            print("bcm Data: ", bcm_data)
            print("cell voltage :", monobloc_v)
            print("cell temp :", monobloc_t)
            print("error", error)
            print("err time stamp", err_time_stamp)
        reset_param()