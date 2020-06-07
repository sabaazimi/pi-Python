# Property of KPM Power for the ANZEN Battery Management System
# Code developed by Saba Azimi
# Created: Jan 28, 2020
# Last Modified: 
# Modified by: Saba Azimi

import can
import connect_can
import binascii
import time
import alarm_func
from datetime import datetime

class AlarmObject:

    def __init__(self, data, s_t, e_t, desc, i_v):
        if data[:2] == "01":
            self.alarm_type = "critical"
            self.type_id = "01"
        elif data[:2] == "02":
            self.alarm_type = "serious"
            self.type_id = "02"
        elif data[:2] == "03":
            self.alarm_type = "warning" 
            self.type_id = "03"        
        # self.alarm_type = a_type
        self.start_time = s_t
        self.end_time = e_t
        self.alarm_description = desc
        self.alarm_index_val = i_v     #this property uniquly identifies the index and value at which the alarm occured. it is an dictionary {index : value}


    def start_time_setter(self, val):
        if self.start_time != val:
            self.start_time = val

    def end_time_setter(self, val):
        self.end_time = val 

    def alarm_type_setter(self, val):
        self.alarm_type = val 

    def alarm_description_setter(self, val):
        self.alarm_description = val                     

