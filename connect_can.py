
# Property of KPM Power for the ANZEN Battery Management System
# Code developed by Eric Dao
# Created: November 13, 2019
# Last Modified: December 23, 2019
# Modified by: Eric Dao

import os
import can

os.system('sudo ip link set can0 type can bitrate 250000') # setup CAN-BUS
os.system('sudo ifconfig can0 up')  # initialize CAN-Bus
os.system('sudo ifconfig can0 txqueuelen 1000')

can0 = can.interface.Bus(
    channel='can0', bustype='socketcan_ctypes')  # socketcan_native