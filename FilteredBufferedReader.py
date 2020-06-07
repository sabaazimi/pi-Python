import config
import json
import time
import can
import os
# import connect_can #the .pyc and/or the .py file of this needs to be in the same folder for it to work
# import active_api
from datetime import datetime
import binascii
import Queue
try:
   import queue
except ImportError:
   import Queue as queue





class FilteredBufferedReader(can.BufferedReader):
    def __init__(self, filter):
        can.BufferedReader.__init__(self)
        self.buffer = queue.LifoQueue(0)
        self.filter_list = filter

    def on_message_received(self, msg):
        if self.filter_list is None:  # no filtering
            self.buffer.put(msg, False)
        else:
            if msg.arbitration_id in self.filter_list:
                self.buffer.put(msg, False)

    def get_message_noblock(self):
        try:
            return self.buffer.get_nowait()
        except queue.Empty:
            return None