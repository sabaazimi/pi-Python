# Property of KPM Power for the ANZEN Battery Management System
# Code developed by Saba Azimi
# Created: May 22, 2020
# Last Modified: June 02, 2020
# Modified by: Saba Azimi

import can
import connect_can
import binascii
import time
from datetime import datetime
import alarm_obj
import alarm_func
import alarm_collector


class AlarmCreator :

    def __init__(self):
        self.chk_list = []
        self.array = [1, 2, 4, 8]
        self.alarms = []
        self.total_alarm = []


    def obj_creator(self, data,  array):
        arr = []
        data_str = data[2:]

        for i in range(len(data_str)) :
            temp_obj = [data[:2] , i + 2  , data_str[i]] #["01", index, value : 1-f in hex format]
            arr.append(alarm_obj.AlarmObject(temp_obj[0], datetime.utcnow().isoformat(), None, ([temp_obj[0], temp_obj[1] - 2 , temp_obj[2]]), {i:data_str[i]}))
        return arr     

    def poputator(self, array, data, dic) :
        for i in range(self.chk_list):
            if len(self.chk_list) == 0 :
                self.chk_list.insert(data[i]-1 , )


    def chk_list_populator(self, arr, array):
        if len(self.chk_list) == 0 :
            # print("zero")
            for i in range(len(arr)):
                self.chk_list.append(self.obj_creator(arr[i],self.array))
            
        else:
            # print("more")
            for j in range(len(arr)):
                new_data = arr[j][2:]
                for n in range(len(new_data)):
                    if self.chk_list[j][n].alarm_description[2] != new_data[n]:
                        self.chk_list[j][n] = alarm_obj.AlarmObject(arr[j], datetime.utcnow().isoformat(), None, ([arr[j][:2], n  , new_data[n]]), {n+2:new_data[n]})


    def main(self, arr, array):
        self.chk_list_populator(arr, array) 
        temp = []
        for i in range(len(self.chk_list)):
            temp.extend(self.chk_list[i])
        for i in range(len(temp)):
            if temp[i].alarm_description[2] != '0' :
                self.alarms.append({"st":temp[i].start_time, "d":temp[i].alarm_description})
            


    def alarm_count(self, data):
        tmp = []
        data_str = data[2:]
        for i in range(len(data_str)):
            tmp.extend(alarm_func.find_subset(self.array, int(data_str[i],16)))
        return len(tmp)
    
    def total_alarm_count(self, arr):
        # tmp = []
        del self.total_alarm[:]
        for i in range(len(arr)):
            self.total_alarm.append(self.alarm_count(arr[i]))
        return self.total_alarm