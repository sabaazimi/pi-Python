import config
import json
import time
import can
import os
import connect_can #the .pyc and/or the .py file of this needs to be in the same folder for it to work
# import active_api
from datetime import datetime
import binascii
# import FilteredBufferedReader
import Queue
import math

cell_voltage = []
cell_temp = []
cell_soc = []
cell_soh = []
bcm_data = []  # master data
cell_volt_flag = False
cell_temp_flag = False
cell_soc_flag = False
cell_soh_flag = False
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





def list_len(number_of_cells, number_of_data_per_line):
    return (math.ceil(number_of_cells/number_of_data_per_line))




#  CELL DATA----------------------------



def create_request_send(frame):  # Create Sending Requests
    volt_send = can.Message(arbitration_id=frame, data=[
                            0x1, 0x1, 0, 0, 0, 0, 0, 0], extended_id=True)

    temp_send = can.Message(arbitration_id=frame, data=[
                            0x2, 0x1, 0, 0, 0, 0, 0, 0], extended_id=True)

    soc_send = can.Message(arbitration_id=frame, data=[
                        0x3, 0x1, 0, 0, 0, 0, 0, 0], extended_id=True)

    soh_send = can.Message(arbitration_id=frame, data=[
                        0x4, 0x1, 0, 0, 0, 0, 0, 0], extended_id=True)

    bcm_send = can.Message(arbitration_id=frame, data=[
                            0x5, 0, 0, 0, 0, 0, 0, 0], extended_id=True)                        
    
    connect_can.can0.send(volt_send)
    connect_can.can0.send(temp_send)
    connect_can.can0.send(soc_send)
    connect_can.can0.send(soh_send)
    connect_can.can0.send_periodic(bcm_send, 0.20)




def main():
    global cell_volt_flag 
    global cell_temp_flag
    global master_flag
    global bcm_flag
    global cell_soc_flag
    global cell_soh_flag
    global cell_soc
    global cell_soh
    cell_volt_flag = False
    cell_temp_flag = False
    cell_soc_flag = False
    cell_soh_flag = False
    master_flag = False
    bcm_flag = False
    n = 1  # volt counter
    t = 1  #temp counter
    c = 1  #soc counter
    h = 1  #soh counter

    create_request_send(0x1830e8f4)
    for z in range(150):
        msg = connect_can.can0.recv(10.0)
        if msg:
            data = binascii.hexlify(msg.data)
            frame_id = hex(msg.arbitration_id)  
            if frame_id[2:10] == "1831f4e8" and cell_volt_flag == False:    
                if int(data[:2], 16) == n :
                    cell_voltage.append(data)
                if n < (list_len(NUMBER_OF_CELLS,3) + 2):
                    n += 1
                else:
                    del cell_voltage[:]
                    cell_volt_flag =  False
                    # break
                if len(cell_voltage) > (list_len(NUMBER_OF_CELLS,3) + 2):
                    del cell_voltage[:]
                    cell_volt_flag = False
                    n = 1
                if len(cell_voltage) == (list_len(NUMBER_OF_CELLS,3) + 1): 
                    cell_volt_flag = True 
            if frame_id[2:10] == "1832f4e8" and cell_temp_flag == False:
                if int(data[:2], 16) == t :
                    cell_temp.append(data)
                if t < (list_len(NUMBER_OF_CELLS,6) + 2) :
                    t += 1
                else:
                    del cell_temp[:]
                    cell_temp_flag =  False
                if len(cell_temp) > (list_len(NUMBER_OF_CELLS,6) + 2):
                    del cell_temp[:]
                    cell_temp_flag = False
                    t = 1
                if len(cell_temp) == (list_len(NUMBER_OF_CELLS,6) + 1):
                    cell_temp_flag = True
            if frame_id[2:10] == "1833f4e8" and cell_soc_flag == False:    
                if int(data[:2], 16) == c :
                    cell_soc.append(data)
                if c < (list_len(NUMBER_OF_CELLS,6) + 2):
                    c += 1
                else:
                    del cell_soc[:]
                    cell_soc_flag =  False
                    # break
                if len(cell_soc) > (list_len(NUMBER_OF_CELLS,6) + 2):
                    del cell_soc[:]
                    cell_soc_flag = False
                    c = 1
                if len(cell_soc) == (list_len(NUMBER_OF_CELLS,6) + 1): 
                    cell_soc_flag = True

            if frame_id[2:10] == "1834f4e8" and cell_soh_flag == False:    
                if int(data[:2], 16) == h :
                    cell_soh.append(data)
                if h < (list_len(NUMBER_OF_CELLS,6) + 2):
                    h += 1
                else:
                    del cell_soh[:]
                    cell_soh_flag =  False
                    # break
                if len(cell_soh) > (list_len(NUMBER_OF_CELLS,6) + 2):
                    del cell_soh[:]
                    cell_soh_flag = False
                    h = 1
                if len(cell_soh) == (list_len(NUMBER_OF_CELLS,6) + 1): 
                    cell_soh_flag = True 

            if frame_id[2:10] == "1835f4e8" and master_flag == False:
                if data[:2] == "01" and len(bcm_data) == 0:
                    bcm_data.append(data)
                if data[:2] == "02" and len(bcm_data) == 1 :
                    bcm_data.append(data)
                if data[:2] == "03" and len(bcm_data) == 2 :
                    bcm_data.append( data)

            # print(bcm_data)
                if len(bcm_data) == 3 :
                    master_flag = True
        # print("master data", bcm_data)
        # print("voltage", cell_voltage)
        # print("temp", cell_temp)
        # print("master flag", master_flag)
        # print("temp_flag",cell_temp_flag )
        # print("voltage flag", cell_volt_flag)
        # print("-----------------------------------------------------------")
            if cell_volt_flag == True and cell_temp_flag == master_flag == cell_soc_flag == cell_soh_flag == True:
                bcm_flag = True
                # connect_can.can0.flush_tx_buffer()
                break

def reset_param():
    global bcm_flag
    global cell_temp_flag
    global cell_volt_flag
    global cell_soc_flag
    bcm_flag = False
    cell_temp_flag = False
    cell_volt_flag = False
    cell_soc_flag = False
    master_flag = False
    del bcm_data[:]
    del cell_temp[:]
    del cell_voltage[:]
    del cell_soc[:]

if __name__ == "__main__":
    get_num_batt_temp()
    while True:
        main()
        # print(bcm_flag)
        if bcm_flag == True:
            print("bcm Data: ", bcm_data)
            print("cell voltage :", cell_voltage)
            print("cell temp :", cell_temp)
            print("cell soc :", cell_soc)
            print("cell soh :", cell_soh)
        reset_param()