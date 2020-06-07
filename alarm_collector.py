# Property of KPM Power for the ANZEN Battery Management System
# Code developed by Saba Azimi
# Created: May 22, 2020
# Last Modified: June 02, 2020
# Modified by: Saba Azimi

import can
import connect_can
import binascii
import json
import requests
import time
from datetime import datetime
import alarm_creator
import config
from requests.exceptions import ConnectionError





def create_request_send(frame):  # Create Sending Requests
    alarm_send = can.Message(arbitration_id=frame, data=[
                            0x8, 0, 0, 0, 0, 0, 0, 0], extended_id=True)
                            
    connect_can.can0.send(alarm_send)




alarm_array = []
alarm_flag = False
array = [1,2,4,8] 
zero_flag = False
def main(al_arr):  
    global alarm_flag
    global zero_flag
    zero_flag = False
    alarm_flag = False
    create_request_send(0x1830e8f4)
    j = 1
    for i in range(15):
        msg = connect_can.can0.recv(10.0)
        if msg:
            data = binascii.hexlify(msg.data)
            frame_id = hex(msg.arbitration_id)                 
            if frame_id[2:10] == "1838f4e8":
                if data == '0000000000ffffff':
                    zero_flag = True
                    alarm_flag = True
                    al_arr = [0, 0 , 0]
                elif int(data[:2], 16) == j :
                    zero_flag = False
                    alarm_array.append(data) 
                    j += 1  
                else:
                    zero_flag = False
                    del alarm_array[:]
                    alarm_flag = False
                    j = 1
                if j > 4 :
                    del alarm_array[:]
                    alarm_flag=False  
                    j = 1
                if len(alarm_array) > 4:
                    del alarm_array[:]
                    j = 1
                    alarm_flag = False
                if len(alarm_array) == 3 :
                    alarm_flag = True




if __name__ == "__main__":
    alarm_url = config.apiUrl + "bms/" + config.bmsId + "/alarm-log"
    headers = {"Authorization":"Basic "+config.token, "Content-Type":"application/json"}
    alarmCreator = alarm_creator.AlarmCreator()
    zero_submission_flag = False
    while True:
        try:
            del alarmCreator.alarms[:]
            main(alarmCreator.total_alarm)
            if alarm_flag == True :
                if zero_flag == True and zero_submission_flag == False:
                    alarmCreator.total_alarm = [0, 0, 0]
                    # submit once and wait for next non-zero Alarm
                    alarm_payload = {
                        "details": {
                            "alarms":alarmCreator.total_alarm,  
                        }
                    }
                    alarm_data = json.dumps(alarm_payload)
                    # print(alarm_payload)
                    req = requests.post(alarm_url, headers=headers , data=alarm_data)
                    print(json.dumps(req.json(),indent=2))
                    zero_submission_flag = True
                else:
                    alarmCreator.total_alarm_count(alarm_array)
                    alarmCreator.main(alarm_array, array)
                print("-------------------------------")
                if zero_flag == False:
                    alarm_payload = {
                            "details": {
                                "alarms":alarmCreator.total_alarm,  
                            "alarm_descriptions":alarmCreator.alarms}
                    }
                    alarm_data = json.dumps(alarm_payload)
                    print(alarm_payload)
                    zero_submission_flag = False
                    req = requests.post(alarm_url, headers=headers , data=alarm_data)
                    print(json.dumps(req.json(),indent=2))
        except ConnectionError:
	        continue
        except Exception as error:
            print("some error happend, ", error)                    