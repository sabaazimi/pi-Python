# Property of KPM Power for the ANZEN Battery Management System
# Code developed by Eric Dao
# Created: November 13, 2019
# Last Modified: June 03, 2020
# Modified by: Saba Azimi


import json
import requests
import config
import time
import os
from requests.exceptions import ConnectionError
import li_cell_data

print("send_api running")
# setup for API
url = config.apiUrl + "bms/" + config.bmsId + "/log"
headers = {"Authorization":"Basic "+config.token, "Content-Type":"application/json"}
li_cell_data.get_num_batt_temp()


while True:
    try:
        li_cell_data.main()       
        print("li flag is ", li_cell_data.bcm_flag)
        if li_cell_data.bcm_flag == True:
            payload = {
                "details": {
                    "noc" : li_cell_data.NUMBER_OF_CELLS,  # NUMBER OF CELLS
                    "nos" : li_cell_data.NUMBER_OF_SLAVES,  # NUMBER OF SLAVES
                    "not" : li_cell_data.NUMBER_OF_THERMISTORS, # NUMBER OF THERMISTORS
                    "master": li_cell_data.bcm_data,    # master BCM data Info
                    "slaves" : {          # Slave BMM data info
                        "v" :li_cell_data.cell_voltage,
                        "t" : li_cell_data.cell_temp ,
                        "c" : li_cell_data.cell_soc , 
                        "h" : li_cell_data.cell_soh
                    }
                  }
            }       
            data = json.dumps(payload)
            print("payload is ", payload)
            r = requests.post(url, headers=headers , data=data)
            print(json.dumps(r.json(),indent=2))
            time.sleep(1)
        li_cell_data.reset_param()
    except ConnectionError:
	    continue
    except Exception as error:
        print("some error happend, ", error)
	# os.system('sudo shutdown -r now')
      #  continue
        

