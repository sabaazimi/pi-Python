# Property of KPM Power for the ANZEN Battery Management System
# Dictionary developed by Saba Azimi, source: Erics (Alarm_Dictionary.xlsx)
# Created: Dec 31, 2019
# Last Modified: Dec 31, 2019
# Modified by: 




# Dictionary manifest :
#---------------------------------------
# GENERAL STRUCTURE : 
#     alarm_type : {
#             data_index : {
#                   data_value : data_description
#                   }
#             }
#     }
#---------------------------------------
# DESCRIPTION:
#     alarm_type : serious, general, slight
#     data_index : index of alarm in the generated data if the value is not zero, for example in example_data, none zeros are 1c5
#     data_value : value of non_zero data 
#     data_description : the actual alarm data_description
#---------------------------------------
# EXAMPLE : 
#     example_data = 01 01 c5 00 00 00  
#  ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___
# | 0 | 1 | 0 | 1 | c | 5 | 0 | 0 | 0 | 0 | 0 | 0 |  <--- DATA
#  ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___
#   0   1   2   3   4   5   6   7   8   9   10  11   <--- INDEX
#
# example_data[0:3] == 01 -> alarm_type = serious alarm
# example_data[3] = 1 -> data_index = 3 and 
#                        data_value = 1
#                        then -> data_description = "Serious unknown alarm (Triggered when setting uppwer limit cell voltage overvoltage)"
            

#------------------------------------------------- CRITICAL Alarms ------------------------------------------------------------------
_1 = {

   0 : {    
            1: "System voltage too high",   #"Serious unknown alarm (Triggered when setting upper limit pack overvoltage)",
            2: "Fast charging current too high", #"Serious unknown alarm (Triggered when setting fast charge current over current)",
            4: "Slow charging current too high",   #"Serious unknown alarm (Triggered when setting slow charge current over current) ",
            8: "Feedback current too high" #"Serious unknown alarm (Triggered when setting feedback current over current)"current over current)"
        } ,

    1 : {
            1: "BMS supply voltage too low",  #"Serious alarm of power supply voltage under voltage",
            2: "BMS supply voltage too high", #"Serious alarm of power supply voltage over voltage",
            4: "M800 temperature too high", #"Serious alarm of upper limit module temperature",
            8: "System voltage too low"  #"Serious unknown alarm (Triggered when setting lower limit pack undervoltage)"},
        },   
    2 : {
            1: "Cell voltage too high",  #"Serious unknown alarm (Triggered when setting upper limit cell voltage overvoltage)",
            2: "Cell voltage too low",  #"Serious unknown alarm (Triggered when setting lower limit cell voltage undervoltage)",
            4: "Voltage difference between two cells too high", #"Serious unknown alarm (Triggered when setting cell voltage differential)",
            8: "Temperature too high during charging" #"Serious unknown alarm (Triggered when setting upper limit of charging cell overtemperature)"},
        },
    3 : {
            1: "Current too high during discharging" ,  # "Serious dischage current overcurrent alarm",
            2: "Low Insulation resistance",
            4: "Battery charge is too low",  #"Serious SOC is too LOW alarm",
            8: "Battery charge is too high"  #"Serious SOC is too HIGH alarm"

        },
    4 : {
           1: "SOC difference between two cells", #"Serious unknown alarm (Triggered when setting SOC differential)",
           2: "UNKNOWN ALARM",
           4: "UNKNOWN ALARM",
           8: "UNKNOWN ALARM"
        },
    5 : {
            1: "Battery too cold for charging", #"Serious charging unit under temperature alarm",
            2: "Cell temperature too high",
            4: "Battery too cold for discharging",  #"Serious the lower limit disCharging cell temprature alarm",
            8: "Difference between two cell temperatures too high" #"Serious single temperature difference alarm"           
        },
    6:  {
            1: "UNKNOWN ALARM",
            2: "UNKNOWN ALARM",
            4: "UNKNOWN ALARM",
            8: "UNKNOWN ALARM"
        },  
    7:  {
            1: "UNKNOWN ALARM",
            2: "UNKNOWN ALARM",
            4: "UNKNOWN ALARM",
            8: "UNKNOWN ALARM"
        },
    8:  {
            1: "UNKNOWN ALARM",
            2: "UNKNOWN ALARM",
            4: "UNKNOWN ALARM",
            8: "UNKNOWN ALARM"

        }          
}


#------------------------------------------------- SERIOUS Alarms ------------------------------------------------------------------
_2 = {

   0 : {    
            1: "System voltage is getting too high",   
            2: "Fast charging current is getting too high",
            4: "Slow charging current is getting too high",
            8: "Feedback current is getting too high" 
        } ,

    1 : {
            1: "BMS supply voltage is getting too low",  
            2: "BMS supply voltage is getting too high", 
            4: "M800 temperature is getting too high", 
            8: "System voltage is getting too low"  
        },
    2 : {
            1: "Cell voltage is getting too high",
            2: "Cell voltage is getting too low", 
            4: "Voltage difference between two cells is getting too high", 
            8: "Temperature is getting too high during charging" 
        },   
    3 : {
            1: "Current is getting too high during discharging" ,  
            2: "Low Insulation resistance",
            4: "Battery charge is getting too low", 
            8: "Battery charge is getting too high" 

        },
    4 : {
           1: "SOC difference between two cells", 
           2: "UNKNOWN ALARM",
           4: "UNKNOWN ALARM",
           8: "UNKNOWN ALARM"
        },
    5 : {
            1: "Battery is getting too cold for charging",
            2: "Cell temperature is getting too high",
            4: "Battery is getting too cold for discharging",  
            8: "Difference between two cell temperatures is getting too high" 
        },
    6:  {
            1: "UNKNOWN ALARM",
            2: "UNKNOWN ALARM",
            4: "UNKNOWN ALARM",
            8: "UNKNOWN ALARM"
        },  
    7:  {
            1: "UNKNOWN ALARM",
            2: "UNKNOWN ALARM",
            4: "UNKNOWN ALARM",
            8: "UNKNOWN ALARM"
        },
    8:  {
            1: "UNKNOWN ALARM",
            2: "UNKNOWN ALARM",
            4: "UNKNOWN ALARM",
            8: "UNKNOWN ALARM"

        }          
}

#------------------------------------------------- WARNINGS Alarms ------------------------------------------------------------------

_3 = {

   0 : {    
            1: "System voltage is slightly too high",   
            2: "Fast charging current is slightly too high",
            4: "Slow charging current is slightly too high",
            8: "Feedback current is slightly too high" 
        } ,

    1 : {
            1: "BMS supply voltage is slightly too low",  
            2: "BMS supply voltage is slightly too high", 
            4: "M800 temperature is slightly too high", 
            8: "System voltage is slightly too low" 
        } ,   
    2 : {
            1: "Cell voltage is slightly too high", 
            2: "Cell voltage is slightly too low",  
            4: "Voltage difference between two cells is slightly too high", 
            8: "Temperature is slightly too high during charging"
        },
    3 : {
            1: "Current is slightly too high during discharging" ,  
            2: "Low Insulation resistance",
            4: "Battery charge is slightly too low",  
            8: "Battery charge is slightly too high"  

        },
    4 : {
           1: "SOC difference between two cells", 
           2: "UNKNOWN ALARM",
           4: "UNKNOWN ALARM",
           8: "UNKNOWN ALARM"
        },
    5 : {
            1: "Battery is slightly  too cold for charging",
            2: "Cell temperature is slightly too high",
            4: "Battery is slightly too cold for discharging",  
            8: "Difference between two cell temperatures is slightly too high" 
        },
    6:  {
            1: "UNKNOWN ALARM",
            2: "UNKNOWN ALARM",
            4: "UNKNOWN ALARM",
            8: "UNKNOWN ALARM"
        },  
    7:  {
            1: "UNKNOWN ALARM",
            2: "UNKNOWN ALARM",
            4: "UNKNOWN ALARM",
            8: "UNKNOWN ALARM"
        },
    8:  {
            1: "UNKNOWN ALARM",
            2: "UNKNOWN ALARM",
            4: "UNKNOWN ALARM",
            8: "UNKNOWN ALARM"

        }          
}





