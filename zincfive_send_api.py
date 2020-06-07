# Property of KPM Power for the ANZEN Battery Management System
# Code developed by Eric Dao
# Created: November 13, 2019
# Last Modified: March 09, 2020
# Modified by: Saba Azimi

import json
import requests
import config
import time
import os
from requests.exceptions import ConnectionError
import fbs
from itertools import islice, takewhile
import system_dimension


print("send_api running")
# setup for API
url = config.apiUrl + "bms/" + config.bmsId + "/log"
headers = {"Authorization":"Basic "+config.token, "Content-Type":"application/json"}
system_dimension.get_num_batt_temp()


seclist = [12, 7, 7, 12]


def slv_generator(slices, temp_slices):
    z = 1
    slv = []
    for s in range(len(slices)):
        cells = []
        for c in range(len(slices[s])):
            cells.append({"id" : "cell"+ str(z), "v":slices[s][c], "temp":temp_slices[s][c]})
            if z < 39:
                z +=1    
        slv.append({"cells" : cells})
    return slv


while True:
    try:
        fbs.main()
        if fbs.bcm_flag == True:
            payload = {
                "details": {
                    "noc" : system_dimension.NUMBER_OF_CELLS,  # NUMBER OF CELLS
                    "nos" : system_dimension.NUMBER_OF_SLAVES,  # NUMBER OF SLAVES
                    "not" : system_dimension.NUMBER_OF_THERMISTORS, # NUMBER OF THERMISTORS
                    "master": fbs.bcm_data,
                    "err_t" : fbs.err_time_stamp,
                    "slaves" : {
                        "v" :fbs.monobloc_v,
                        "t" : fbs.monobloc_t 
                    }
  
                }
            }       
    	    
            print("payload iis  ", payload)
            data = json.dumps(payload)
            r = requests.post(url, headers=headers , data=data)
            print(json.dumps(r.json(),indent=2))
            fbs.reset_param()
            # time.sleep(10)
    except ConnectionError:
	    continue
    except Exception as error:
        print("some error happend, ", error)
	# os.system('sudo shutdown -r now')
      #  continue
        

