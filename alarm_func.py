# Property of KPM Power for the ANZEN Battery Management System
# Code developed by Saba Azimi,
# Created: Dec 30, 2019
# Last Modified: Dec 30, 2019
# Modified by: 


from datetime import datetime
import alarm_dic_rev


# to create sub_sum of a number to its associated sub categories
def find_subset(frame_data, req_sum):
    l = len(frame_data)

    # ROWS : array
    # COL : range(sum)
    row = l
    col = req_sum + 1

    # 2d array storing Sum
    dp_array = [[0] * col for i in range(row)]

    for i in range(row):
        for j in range(1, col):
            # Row 0
            if i == 0:
                if j >= frame_data[i]:
                    dp_array[i][j] = frame_data[i]
                else:
                    continue
            else:
                if j - frame_data[i] >= 0:
                    dp_array[i][j] = max(dp_array[i - 1][j], (frame_data[i] + dp_array[i - 1][j - frame_data[i]]))
                elif j >= frame_data[i]:
                    # take from row above it
                    dp_array[i][j] = max(dp_array[i - 1][j], frame_data[i])
                else:
                    dp_array[i][j] = dp_array[i - 1][j]

    # Find out which Numbers should be in the subset
    # give from index 0
    row -= 1
    col -= 1
    sum_subset = []

    # check if the Subset is possible : if not, return None
    if dp_array[row][col] != req_sum:
        return None

    # get the subset
    while col >= 0 and row >= 0 and req_sum > 0:
        # First Row
        if (row == 0):
            sum_subset.append(frame_data[row])
            break

        # Bottom-Right most ele
        if (dp_array[row][col] != dp_array[row - 1][col]):
            # print(req_sum,' : ',dp_array[row][col],dp_array[row-1][col],' : ',frame_data[row])
            sum_subset.append(frame_data[row])
            req_sum -= frame_data[row]
            col -= frame_data[row]
            row -= 1
        else:
            row -= 1

    return sum_subset

start_time = datetime.now() 
end_time = 0 
time_flag = False

def update_time():
    global time_flag
    if time_flag == True:
        start_time = datetime.now()
    time_flag =  False


str_data=""


# returns a dictionary of position and value for the recieving data, if it is not zero
def signal_detector(arr, data_str):
    global start_time
    global end_time
    global str_data
    global time_flag
    dic = {}
    for i in range(len(data_str)):
        if data_str.strip() and data_str[i] != "0":
            dic.update({i: [find_subset(arr,int(data_str[i], 16)), end_time]})
    return dic



# return the index-value set of non_zero elements in a data peice
def index_val_set(data):
    dic = {}
    for i in range(len(data)):
        if data[i] !="0":
            dic.update({i: data[i]})

    return dic        

# calculate the total number of alarms of each kind
def total_alarm_count(d):
    sum = 0 
    for i in d.values():
        sum = sum + len(i[0])
    return sum    

# return arrays of alarms details [position, alarm_number, alarm_description]
# e.g 013c00000 returns 
                # [
                #     [1, 1, 'description'], 
                #     [2, 1, 'description'], [2, 2 ,'description'], 
                #     [3, 4, 'description'], [3, 8 ,'description']
                # ]
def get_alarm_details(array, s, dic):  #have to supply s[2:] 
    data = signal_detector (array, s)
    alarm_detail = []
    for key, value in data.items():
        for i in value[0]:
            alarm_detail.append([key, i, dic[key][i],value[1]])
    return alarm_detail    




def get_alarm_description(val):
    alarm_type = alarm_type_finder(val[0])
    return alarm_type[val[1]][int(val[2])]




def alarm_type_finder(data):
    alarm_type=""
    if data[:2] == "01":
        alarm_type = alarm_dic_rev._1
    elif data[:2] == "02":
        alarm_type = alarm_dic_rev._2
    elif data[:2] == "03":
        alarm_type = alarm_dic_rev._3
    return alarm_type            




# TEST TO GET ALL THE COMPOUNENT OF AN ALARM :
def get_alarm_details2(array, s, dic):
    data = signal_detector (array, s)
    alarm_detail = []
    for key, value in data.items():
        for i in value:
            alarm_detail.append([key, i, dic[key][i], index_validator(dic[key][i], 1)])
    return alarm_detail     

# check to see if a certain index i exists in list arr , otherwise return False
def index_validator(arr,i):
    try:
        return arr[i]
    except IndexError:
        return None    



def all_zero_validator(data):
    for i in data:
        if i != "0" and i != "f":
            return False
            break
    return True        








    # def signal_detector(arr, data_str):
    # global start_time
    # global end_time
    # global str_data
    # global time_flag
    # dic = {}
    # for i in range(len(data_str)):
    #     if data_str.strip() and data_str[i] != "0":
    #         if data_str != str_data:
    #             str_data = data_str
    #             time_flag = True
    #             update_time()
    #         dic.update({i: [find_subset(arr,int(data_str[i], 16)), start_time, end_time]})
    #         print(time_flag)
    # return dic