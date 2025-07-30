#
# -*- coding: utf-8  -*-
#=================================================================
# Created by: Jieming Ye
# Created on: Feb 2024
# Last Modified: Feb 2024
#=================================================================
# Copyright (c) 2024 [Jieming Ye]
#
# This Python source code is licensed under the 
# Open Source Non-Commercial License (OSNCL) v1.0
# See LICENSE for details.
#=================================================================
"""
Pre-requisite: 
SimulationName.oof: default oslo output file after successfully run a simulation.
xxxxx.txt: User configuration file under some options.
Used Input:
simname: to locate the result file or file rename
main_option: to decide which subfunction to go
time_start: to define the analysis start time
time_end: to define the analysis end time
option_select: to define the option selected in subfunction
text_input:
low_v:
time_step:
Expected Output:
Various new .csv file depending on the option selection.
Description:
This script defines 3 options which is easy to achieve.
In list_train_data(), it generates ****.osop.lst file using default list file extraction command. Then it reads the file line by line depending on the header. Rearrange the information in list manipulation and output as a csv file. Very straightforward.
In low_voltage_analysis(), it calls the list_train-data() first. Then it analysis the result list one by one comparing the voltage against the threshold and save the new information in a new list. Then it collates all information which meets the criteria and rearrange in a new list. Very straightforward method.
In umean_useful(), it generates ****.osop.lst file using default list file extraction command. Then it read the file line by line and filter out the train information within the selected branches. Then it processes the big list, split the train and calculate the average value. The process is straightforward in general and the detailed mean useful calculation is defined in umean_useful_process(). It should be noted that the calculation is still under debate which value should be used for the output. There for the calculation output principle might needs to be changed. Some other output option is commented out but kept in to code in case the designer want to change at some point.
Attention:
Option 1 and 2 need to be further updated in the future as their usage is not that meaningful.


"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
#=================================================================
# Set Information Variable
# N/A
#=================================================================

import sys
import os
import math
import copy
import csv

from vision_oslo_extension.shared_contents import SharedMethods


def main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):

    #User Interface - Welcome message:
    print("")
    print("VISION OSLO Post Processing - - - > ")
    print("")

    # get simulation name name from input
    print("Checking Result File...")
    check = SharedMethods.check_oofresult_file(simname)
    if check == False:
        return False
    
    if not main_menu(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):
        return False

    return True
    
# Main Menu
def main_menu(simname, option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):

    print(f"\nOption Selected --> Option {option_select}")

    time_increment = 5
    #25/02/2025 should this be changed to time_increment = time_step?

    if option not in ["0","1","2","4"]:
        SharedMethods.print_message("ERROR: Error: Contact Support. Issue in post_processing.py. Please contact Support.","31")
        return False

    if option == "0":
        SharedMethods.print_message("ERROR: Please select an option and run again","31")
        return False

    if option == "1":
        if not list_train_data(simname, time_start, time_end, option_select, text_input):
            return False
        
    elif option == "2":
        if not low_voltage_analysis(simname, time_start, time_end, option_select, text_input, low_v,time_increment):
            return False

    elif option == "4":
        if not umean_useful(simname, time_start, time_end, option_select, text_input,time_increment):
            return False
    
    print("")
    print("Processing loop completed. Check information above")
    print("")
    return True

#==================================================================================
# seleciton 1 list train data
def list_train_data(simname, time_start, time_end, option_select, text_input):

    br_list_input = []
    # branch_name = ""

    if option_select not in ["0","1","2","3","4"]:
        SharedMethods.print_message("ERROR: Contact Support. Issue in post_processing.py --> list_train_data","31")
        return False

    if option_select in ["3","4"]:
        # prepare the list file
        print("\nCheck Branch List File...")
        # branch_name = input()
        branch_list = text_input + ".txt"
        if not os.path.isfile(branch_list): # if the branch list file exist
           SharedMethods.print_message(f"ERROR: Branch list file {branch_list} does not exist. Exiting...","31")
           return False

        # reading the branch list file     
        with open(branch_list) as fbrlist:
            for index, line in enumerate(fbrlist):
                br_list_input.append(line[:50].strip())
        print(br_list_input)
    
    if option_select in ["2","4"]:
        # User defined time windows extraction
        time_start = SharedMethods.time_input_process(time_start,2)
        time_end = SharedMethods.time_input_process(time_end,2)
        
        if time_start == False or time_end == False:
            return False

    time_info_sum = [option_select, time_start, time_end, br_list_input]

    # check the list file
    if not SharedMethods.check_and_extract_lst_file(simname):
        return False

    filename = simname + ".osop.lst"
    # define essential list to be updated
    train_info = ["VISION ID","BHTPBANK"] # train basic information 
    train_e =[]

    branch_lookup = {} # dictionary data type
    u_branch_lookup = {} #dictonary data type for umean useful branch recognition

    # analysis list file
    lst_data_reading_process(filename,train_e,train_info,branch_lookup,u_branch_lookup)
    # List Train Information
    csv_train_info(train_e,branch_lookup,br_list_input,u_branch_lookup,time_info_sum,text_input)

    return True

# train information sort and output    
def csv_train_info(train_e,branch_lookup,br_list_input,u_branch_lookup,time_info_sum,branch_name):
    
    # select the output data
    if time_info_sum[0] == "1":
        sorted_train_e = copy.deepcopy(train_e) # memory consuming but want to avoid touching train_e
        output_name = 'train_list.csv'

    elif time_info_sum[0] == "2":
        output_name = 'train_list_'+str(time_info_sum[1])+"-"+str(time_info_sum[2])+'.csv'
        sorted_train_e = []

        print("Sorting the data within the selected time window...")
        
        for row in train_e:
            if time_info_sum[1] <= row[1] <= time_info_sum[2]:
                sorted_train_e.append(row)

        sorted_train_e = copy.deepcopy(sorted_train_e)

    elif time_info_sum[0] == "3":
        output_name = 'train_list_'+ branch_name +'.csv'
        sorted_train_e = []
        branch_id = []

        print("Sorting the data within the selected branches...")
        
        # get OSLO ID for branch input
        for item in br_list_input:
            branch_id.append(u_branch_lookup.get(item))
            
        for row in train_e:
            if row[12] in branch_id:
                sorted_train_e.append(row)
        sorted_train_e = copy.deepcopy(sorted_train_e)

    else:
        output_name = 'train_list_'+branch_name+ "_" + str(time_info_sum[1])+"-"+str(time_info_sum[2])+'.csv'
        stage_train_e = []
        sorted_train_e = []
        branch_id = []
        
        print("Sorting the data within the selected time window...")
        
        for row in train_e:
            if time_info_sum[1] <= row[1] <= time_info_sum[2]:
                stage_train_e.append(row)
        
        print("Sorting the data within the selected branches...")


        # get OSLO ID for branch input
        for item in br_list_input:
            branch_id.append(u_branch_lookup.get(item))
            
        for row in stage_train_e:
            if row[12] in branch_id:
                sorted_train_e.append(row)
        
        sorted_train_e = copy.deepcopy(sorted_train_e)
        
         
    # list data sorting with train No.
    sorted_train_e.sort(key=lambda row: (row[0], row[1]), reverse=False)

    # replace branch ID to branch Name from OSLO
    for row in range(len(sorted_train_e)):
        sorted_train_e[row][12] = branch_lookup.get(sorted_train_e[row][12])
     

##    sorted_train_e.insert(0, ["VO_ID","T_STEP","TIME","V_Re","V_Im","V_T", \
##                                  "I_Re","I_Im","I_T","P_Re","P_Im","P_T","BRANCH", \
##                                  "DELTA","E_TE","PERC%","DIS_GONE","INS_SPD","AV_SPD"])          
    #print(train_e)
    # write information to a text file
    print("Data Extraction Completed. Writing to csv file...")

    with open(output_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile) # create the csv writer
        lock = 0
        row = 1
        writer.writerow(["VO_ID", "T_STEP", "TIME", "V_Re", "V_Im", "V_T", "I_Re", "I_Im", "I_T", \
                         "P_Re", "P_Im", "P_T", "BRANCH", "DELTA", "E_TE", "PERC%", "DIS_GONE", "INS_SPD", "AV_SPD"])
        row = row + 1
        writer.writerows(sorted_train_e)
    
    return

#=====================================================================================
# selection 2 low votlage analysis
def low_voltage_analysis(simname, time_start, time_end, option_select, text_input, low_v, time_increment):

    print(f"\nThe voltage threshold in XXXXX format (V): {low_v}")
    v_limit = float(low_v)
    #check if the selected voltage is between 0 and 30000
    if v_limit <= 0  or v_limit >= 30000:
        SharedMethods.print_message("ERROR: Invalid threshold. Please reenter a voltage threshold between 0 - 30000","31")
        return False

    br_list_input = []
    
    if option_select not in ["0","1","2","3","4"]:
        SharedMethods.print_message("ERROR: Contact Support. Issue in post_processing.py -->low_voltage_analysis","31")
        return False

    # read the branch name for branch filtering
    # if option 3 or 4 selected check that the selected branch file exist and read the branch file and save as br_list_input
    if option_select in ["3","4"]:
        # prepare the list file
        print("\nCheck Branch List File...")
        
        branch_list = text_input + ".txt"
        if not os.path.isfile(branch_list): # if the branch list file exist
           SharedMethods.print_message(f"ERROR: Branch list file {branch_list} does not exist. Exiting...","31")
           return False

        # reading the branch list file     
        with open(branch_list) as fbrlist:
            for index, line in enumerate(fbrlist):
                br_list_input.append(line[:50].strip())
        print(br_list_input)
    
    # read the times for time window filtering if option 2 or 4 selected
    if option_select in ["2","4"]:
        # User defined time windows extraction
        time_start = SharedMethods.time_input_process(time_start,2)
        time_end = SharedMethods.time_input_process(time_end,2)

        if time_start == False or time_end == False:
            return False

    # details for filtering (branch and time) are saved as time_info_sum
    time_info_sum = [option_select, time_start, time_end, br_list_input]
    #print(time_info_sum)

    # check the list file
    if not SharedMethods.check_and_extract_lst_file(simname):
        return False

    filename = simname + ".osop.lst"
    # define essential list to be updated
    train_info = ["VISION ID","BHTPBANK"] # train basic information 
    train_e =[]

    branch_lookup = {} # dictionary data type
    u_branch_lookup = {} #dictonary data type for umean useful branch recognition
    
    # analysis list file
    lst_data_reading_process(filename,train_e,train_info,branch_lookup,u_branch_lookup)
    # this saves all train step info in train_e =[] which is used for outputs in later stages

    #Adding Branch and Time filter after reading the list file and before running low voltage summary loop, 10/10/2025
    
    # filter by time when option select is 2
    if time_info_sum[0] == "2":
        time_filtered_train_e = []
        print("Sorting the data within the selected time window...")
        
        #go through the train step list row by row and filter by line
        for row in train_e:
            if time_info_sum[1] <= row[1] <= time_info_sum[2]:
                time_filtered_train_e.append(row)

        # intermediate step to copy the time filtered list
        sorted_train_e = copy.deepcopy(time_filtered_train_e)

        # train_e is used for output so overwrite train_e with the filtered list and 
        # keep the output function common between filter (no filter) options
        train_e = copy.deepcopy(sorted_train_e)
    
    # filter by branch name when option is 3
    if time_info_sum[0] == "3":
        branch_filtered_train_e = []
        branch_id = []

        print("Sorting the data within the selected branches...")
        
        # get OSLO ID for branch input
        for item in br_list_input:
            branch_id.append(u_branch_lookup.get(item))

        # filter trian step list row by row by branch names     
        for row in train_e:
            if row[12] in branch_id:
                branch_filtered_train_e.append(row)

        # intermediate step to copy the branch filtered list
        sorted_train_e = copy.deepcopy(branch_filtered_train_e)

        # train_e is used for output so overwrite train_e with the filtered list and 
        # keep the output function common between filter (no filter) options
        train_e = copy.deepcopy(sorted_train_e)

    # filter by time and branch name when option is 4
    if time_info_sum[0] == "4":
        time_filtered_train_e = []
        time_branch_filtered_train_e = []
        branch_id = []
        
        print("Sorting the data within the selected time window...")
        for row in train_e:
            if time_info_sum[1] <= row[1] <= time_info_sum[2]:
                time_filtered_train_e.append(row)
        
        print("Sorting the data within the selected branches...")
        # get OSLO ID for branch input
        for item in br_list_input:
            branch_id.append(u_branch_lookup.get(item))
            
        for row in time_filtered_train_e:
            if row[12] in branch_id:
                time_branch_filtered_train_e.append(row)
        
        # intermediate step to copy the time and branch filtered list
        sorted_train_e = copy.deepcopy(time_branch_filtered_train_e)
        # train_e is used for output so overwrite train_e (currently full train steps) with the filtered list and 
        # keep the output function common between filter (no filter) options
        train_e = copy.deepcopy(sorted_train_e)

    # run the low voltage summary loop which is shown below
    # trian_e used as the input for low voltage summary loop
    # train_e is the whole step results for trains if option 1 is selected
    # train_e is filtered if option 2, 3, 4 is selected
    low_voltage_sum(simname,train_e,v_limit,branch_lookup,u_branch_lookup,time_info_sum,text_input, time_increment)
    
    return True

# used in selection 2 low voltage analysis output
# 2nd module to check and output low votlage summary grouped by branches instead of trains
# low voltage summarise loop, containing train sum and branch sum subloops
# creates 3 output files: Train details, Branch Summary and Train summary
# if train_e is filetered before this function in low_voltage_analysis(); will create filtered results
def low_voltage_sum(simname, train_e,v_limit,branch_lookup,u_branch_lookup,time_info_sum,branch_name, time_increment):
    # select the output data

    print("Finding out information below threshold...")
    vsorted_train_e = []        # where train results filtered by voltage is stored

    # for each row in train_e filter all results under the set voltage
    for row in train_e:
        # 29/10/2024 added check of voltage to be above 0v to filter out results of train in Neutral Section
        if 0 < row[5] < v_limit:
            vsorted_train_e.append(row)

    vsorted_train_e = copy.deepcopy(vsorted_train_e)

    # list data sorting with train No.
    vsorted_train_e.sort(key=lambda row: (row[0], row[1]), reverse=False)

    # replace branch ID to branch Name from OSLO
    for row in range(len(vsorted_train_e)):
        vsorted_train_e[row][12] = branch_lookup.get(vsorted_train_e[row][12])
     
    # write information to a text file

    #run function to give a summary of the lowest voltage recorded on each branch
    branch_sum = get_branch_summary(vsorted_train_e)

    #run function to give a summary of the lowest voltage recorded on each train
    train_sum = get_train_summary(vsorted_train_e, time_increment)

    print("Data Extraction Completed. Writing to text file...")

    # add different names for different filter options
    if time_info_sum[0] == "1":
        csvname = simname

    if time_info_sum[0] == "2":
        csvname = simname + '_tftr'

    if time_info_sum[0] == "3":
        csvname = simname + '_bftr'

    if time_info_sum[0] == "4":
        csvname = simname + '_tbftr'

    #write list of low all voltage instances (train steps)
    with open(csvname + '_T_steps_below_' + str(int(v_limit))+'.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile) # create the csv writer
        lock = 0
        row = 1

        header = ["VO_ID", "T_STEP", "TIME", "V_Re", "V_Im", "V_T", "I_Re", "I_Im", "I_T", "P_Re", "P_Im", "P_T", "BRANCH", "DELTA", "E_TE", "PERC%", "DIS_GONE", "INS_SPD", "AV_SPD"]
        writer.writerow(header)
        row = 2

        for items in vsorted_train_e:
            writer.writerow(items)
            row = row + 1   

    #write train low voltage summary to csv
    with open(csvname + '_Train_below_' + str(int(v_limit))+'.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile) # create the csv writer
        lock = 0
        row = 1

        header = ["Train No", "Train Min V", "Time below Threashold", "No. of instances", "VO_ID", "T_STEP", "TIME", "V_Re", "V_Im", "V_T", "I_Re", "I_Im", "I_T", "P_Re", "P_Im", "P_T", "BRANCH", "DELTA", "E_TE", "PERC%", "DIS_GONE", "INS_SPD", "AV_SPD"]
        writer.writerow(header)
        row = 2

        for items in train_sum:
            writer.writerow(items)
            row = row + 1  

    #write branch low voltage summary to csv
    with open(csvname+'_branch_below_' + str(int(v_limit))+'.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile) # create the csv writer
        lock = 0
        row = 1

        header = ["BRANCH", "Min Train V on branch", "No. of instances", "VO_ID", "T_STEP", "TIME", "V_Re", "V_Im", "V_T", "I_Re", "I_Im", "I_T", "P_Re", "P_Im", "P_T", "BRANCH", "DELTA", "E_TE", "PERC%", "DIS_GONE", "INS_SPD", "AV_SPD"]
        writer.writerow(header)
        row = 2

        for items in branch_sum:
            writer.writerow(items)
            row = row + 1  
    return

#for selection 2
#define function to give a summary of the low voltage occurances in a branch. 
def get_branch_summary(data):

  branch_dict = {}

  for row in data:
    branch_name = row[12]
    v_t = row[5]
    detail_in = row

    if branch_name not in branch_dict:
      branch_dict[branch_name] = {"count": 0, "min_v_t": v_t,"in":detail_in}
    
    branch_dict[branch_name]["count"] += 1
    if v_t < branch_dict[branch_name]["min_v_t"]:
        branch_dict[branch_name]["min_v_t"] = v_t
        branch_dict[branch_name]["in"] = detail_in

  summary = []
  for branch, info in branch_dict.items():
    line = [branch, info["min_v_t"], info["count"]]
    for item in info["in"]:
        line.append(item)

    summary.append(line)

  return summary

#for selection 2
#define function to give a summary of the low voltage occurances of the train. 
def get_train_summary(data, time_increment):

  train_dict = {}

  for row in data:
    train_name = row[0]
    v_t = row[5]
    detail_in = row

    if train_name not in train_dict:
      train_dict[train_name] = {"count": 0, "time": 0,"min_v_t": v_t,"in":detail_in}
    
    train_dict[train_name]["count"] += 1
    
    #25/02/2025 add new column to show total time under threashold, assumes 5 seconds steps
    train_dict[train_name]["time"] += time_increment

    #if the voltage of the current row is smaller than the voltage stored for this train, replace the lowest voltage with current value 
    #and replace the details with currewnt row
    if v_t < train_dict[train_name]["min_v_t"]:
        train_dict[train_name]["min_v_t"] = v_t
        train_dict[train_name]["in"] = detail_in

  summary = []
  for train, info in train_dict.items():
    line = [train, info["min_v_t"], info["time"], info["count"]]
    for item in info["in"]:
        line.append(item)
        
    summary.append(line)

  return summary


#======================================================================================
# selection 4 umeanuseful
def umean_useful(simname, time_start, time_end, option_select, text_input,time_increment):
    br_list_input = []
    # branch_name = ""

    if option_select not in ["0","1","2"]:
        SharedMethods.print_message("ERROR: Contact Support. Issue in post_processing.py --> umean_useful.","31")
        return False
    
    if option_select == "0":
        SharedMethods.print_message("ERROR: Please Select an Option to Continue.","31")
        return False

    print("\nCheck Branch List File...")
    # branch_name = input()
    branch_list = text_input + ".txt"
    if not os.path.isfile(branch_list): # if the branch list file exist
        SharedMethods.print_message(f"ERROR: Branch list file {branch_list} does not exist. Please Enter the correct branch file name.","31")
        return False

    # reading the branch list file     
    with open(branch_list) as fbrlist:
        for index, line in enumerate(fbrlist):
            br_list_input.append(line[:50].strip())
    print(br_list_input)

    # check if empty branh list
    if not br_list_input:
        SharedMethods.print_message("ERROR: Empty Branch List...Please provide valid branch list.","31")
        return False
    
    if option_select == "2":
        # User defined time windows extraction
        time_start = SharedMethods.time_input_process(time_start,2)
        time_end = SharedMethods.time_input_process(time_end,2)
        
        if time_start == False or time_end == False:
            return False
    
    time_info_sum = [option_select, time_start, time_end, br_list_input]
    
    # check the list file
    if not SharedMethods.check_and_extract_lst_file(simname):
        return False

    filename = simname + ".osop.lst"
    # define essential list to be updated
    train_info = ["VISION ID","BHTPBANK"] # train basic information 
    train_e =[]
    branch_lookup = {} # dictionary data type
    u_branch_lookup = {} #dictonary data type for umean useful branch recognition

    # analysis list file
    lst_data_reading_process(filename,train_e,train_info,branch_lookup,u_branch_lookup)

    # check if branch list exist in the model
    if not any(item in u_branch_lookup for item in br_list_input):
        SharedMethods.print_message("ERROR: All input branch does not exist in the model","31")
        return False

    # List Train Information
    umean_useful_process(train_e,br_list_input,u_branch_lookup,time_info_sum,text_input,time_increment)

    return True

# Umean useful calculation process
def umean_useful_process(train_e,br_list_input,u_branch_lookup,time_info_sum,branch_name,time_increment):
    print("Umean useful Calculation Start:")
    time_increase = int(time_increment)
    # create umeanuseful list file
    umean_train_vs = {} # dictionary type to save the total voltage sum
    umean_train_time = {} # ditctionary type to save the total time sum
    branch_id = [] # branch list integer ID
    
    umean_zone = [] # 1d list
    umeanuseful_train = [] #list type

    # get OSLO ID for branch input
    for item in br_list_input:
        branch_id.append(u_branch_lookup.get(item))
    
    # calculate umean useful (Umean zone consider the selected time windows, Umean train consider the whole period)
    if time_info_sum[0] == "2": 
        output_name = 'umeanuseful_result_'+branch_name+'_'+str(time_info_sum[1])+"-"+str(time_info_sum[2])+'.csv'
        for row in range(len(train_e)):
            #print(train_e[row][12],train_e[row][1])
            # umean zone: save all pantograph voltage point in a list within time window
            if (train_e[row][12] in branch_id) and (time_info_sum[1] <= train_e[row][1]) and (train_e[row][1] <= time_info_sum[2]):
                umean_zone.append(train_e[row][5])

            # umean train:
            if (train_e[row][12] in branch_id) and (train_e[row][14]>0):
                train_id = train_e[row][0]
                if train_id not in umean_train_vs:
                    umean_train_vs[train_id] = train_e[row][5]
                    umean_train_time[train_id] = 1
                else:
                    umean_train_vs[train_id] = train_e[row][5] + umean_train_vs.get(train_id)
                    umean_train_time[train_id] += 1
    else:
        output_name = 'umeanuseful_result_'+branch_name+'_full.csv'
        for row in range(len(train_e)):
            # umean zone: save all pantograph voltage point in a list
            if train_e[row][12] in branch_id:
                umean_zone.append(train_e[row][5])
                
            # umean train:
            # data format now: umean_train = {Train ID: [Sum of Volt]}
            # data format now: Umean_train_list = [Train ID, UV, TimeSpan]
            if (train_e[row][12] in branch_id) and (train_e[row][14]>0):
                train_id = train_e[row][0]
                if train_id not in umean_train_vs:
                    umean_train_vs[train_id] = train_e[row][5]
                    umean_train_time[train_id] = 1
                else:
                    umean_train_vs[train_id] = train_e[row][5] + umean_train_vs.get(train_id)
                    umean_train_time[train_id] += 1
    

    #print(umean_zone[0])
    #print(umean_train_list[0])
                
    #print(umean_train_vs) = sum / item no
    umeanuseful_zone = round(sum(umean_zone)/len(umean_zone)/1000, 2)

    #print(umean_train) = sum / time step no
    for train_index, volt in umean_train_vs.items():
        umeanuseful_train.append([train_index, \
                                  round(volt/umean_train_time.get(train_index)/1000,2)])

    #print(umeanuseful_train)

    # sort umean useful train in decesending order
    umeanuseful_train.sort(key=lambda row: (row[1]), reverse=False)

    # # adding addtional information about the train
    for row in range(len(umeanuseful_train)):
        # umeanuseful_train[row][1] = str(umeanuseful_train[row][1]) + " kV"
        # umeanuseful_train[row].append(str(umean_train_time.get(umeanuseful_train[row][0])*5)+" s")
        umeanuseful_train[row].append(str(umean_train_time.get(umeanuseful_train[row][0])*time_increase))
        
    #print(umeanuseful_train)

    print("U mean useful Calculation Completed")
    print(f"U mean zone is {umeanuseful_zone} kV")
    print(f"U mean train is {umeanuseful_train[0][1]} kV")

    with open(output_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile) # create the csv writer
        lock = 0
        row = 1
        writer.writerow(["Umean useful zone (in kV)"])
        row = row + 1
        writer.writerow([umeanuseful_zone])
        row = row + 1
        writer.writerow([""])
        row = row + 1
        writer.writerow(["Umean useful train list (in ascending order)"])
        row = row + 1
        writer.writerow(["VISION ID","Umean(train) (kV)","Traction Time (s)"])
        row = row + 1
        writer.writerows(umeanuseful_train)

#=================================================================================
# define list data process
def lst_data_reading_process(filename,train_e,train_info,branch_lookup,u_branch_lookup):
    #define essential variables
    lst_section = ""  # list section ID
    ins_sec = 0     # instant second
    ins_time = ""   # instant time

    # open text file to get the total line information (best way i can think of)
    # although it require reading the file twice
    print("Analysing lst file....")
    with open(filename) as fp:
        total_line = sum(1 for line in enumerate(fp))

    print("Extracting information from lst file....")
    print("")
    # open .osop.lst file
    with open(filename) as fp:

        for index, line in enumerate(fp):
            # decide which section the code is looking
            if line[:50].strip() == '':
                continue
            if line[:7].strip() == "NNODE":
                lst_section = "NNODE"
            if line[:7].strip() == "NFEED":
                lst_section = "NFEED"
            if line[:7].strip() == "NLINK":
                lst_section = "NLINK"
            if line[:7].strip() == "NFIXC":
                lst_section = "NFIXC"
            if line[:7].strip() == "NSTATV":
                lst_section = "NSTATV"
            if line[:7].strip() == "NMOTA":
                lst_section = "NMOTA"
            if line[:7].strip() == "NTRANS":
                lst_section = "NTRANS"
            if line[:7].strip() == "NMETER":
                lst_section = "NMETER"
            if line[8:12].strip() == "XRLS":
                lst_section = "XRLS"
            if line[:7].strip() == "NMETER":
                lst_section = "NMETER"
            if line[18:32].strip() == "LINE  SECTION":
                lst_section = "LINESECTION"
            if line[:7].strip() == "NBAND":
                lst_section = "NBAND"
            if line[11:17].strip() == "DBNAME":
                lst_section = "DBNAME"
            if line[:7].strip() == "INCSEC":
                lst_section = "INCSEC"
                ins_sec = int(line[8:14].strip()) # get current time steps
                ins_time = line[20:28].strip()  # get current time (day data not implemented)
            if line[:7].strip() == "TRAIN":
                lst_section = "TRAIN"
            if line[:14].strip() == "Run completed.":
                lst_section = ""

            # excute action
            lst_data_action(line,lst_section,ins_sec,ins_time,train_e,train_info,branch_lookup,u_branch_lookup)

            SharedMethods.text_file_read_progress_bar(index, total_line)

# Action on the data list based on the section selection
def lst_data_action(line, lst_section, ins_sec, ins_time, train_e,train_info,branch_lookup,u_branch_lookup):
    if lst_section == "NNODE":
        #print(line.rstrip()) # remove training space
        return

    if lst_section == "NFEED":
        return
    
    if lst_section == "NLINK":  # branch ID vs branch Name lookup table
        if line[:7].strip() == "NLINK":
            return
        elif line[:7].strip()== "":
            return
        else:
            branch_lookup[int(line[:8].strip())] = line[8:14].strip()
            u_branch_lookup[line[8:14].strip()] = int(line[:8].strip())
    
    if lst_section == "NFIXC":
        return
    
    if lst_section == "NSTATV":
        return
    
    if lst_section == "NMOTA":
        return
    
    if lst_section == "NTRANS":
        return
    
    if lst_section == "NMETER":
        return
    
    if lst_section == "XRLS":
        return
    
    if lst_section == "NMETER":
        return
    
    if lst_section == "LINESECTION":
        return
    
    if lst_section == "NBAND":
        return
    
    if lst_section == "DBNAME": # add train electrical information (BHTPBANK list)
        if line[11:17].strip() == "DBNAME":
            return
        
        words = line.strip().split() # split the line into words based on space
        if len(words) == 4:
            train_info.append([int(words[0]),words[1]])
        else:
            train_info.append([int(words[0]),"NOT_USED"])      
    
    if lst_section == "INCSEC":
        return
    
    if lst_section == "TRAIN":  # processing train information by timestep
        if line[:7].strip() == "TRAIN":
            return
        else:
            # get related varible
            index = int(line[:7].strip())
            ins_vr = float(line[8:15].strip())
            ins_vi = float(line[15:23].strip())
            ins_va = math.sqrt(ins_vr**2 + ins_vi**2)
            ins_ir = float(line[27:34].strip())
            ins_ii = float(line[34:42].strip())
            ins_ia = math.sqrt(ins_ir**2 + ins_ii**2)
            ins_pr = ins_vr*ins_ir
            ins_pi = ins_vi*ins_ii
            ins_pa = math.sqrt(ins_pr**2 + ins_pi**2)
            
            dis_gone = float(line[123:131].strip())
            bran_num = int(line[57:63].strip())
            delta = float(line[63:70].strip())

            ins_speed = float(line[72:79].strip())
            av_speed = float(line[80:88].strip())
            te_used = float(line[90:99].strip())
            te_perc = float(line[103:109].strip())

##            train_e = ["VO_ID","T_STEP","TIME","V_Re","V_Im","V_T","I_Re","I_Im","I_T", \
##               "P_Re","P_Im","P_T","BRANCH","DELTA","TE/BE","PERC%","DIS_GONE", \
##               "INS_SPD","AV_SPD"]  # For Information Only
            train_e.append([index,ins_sec,ins_time, \
                            ins_vr,ins_vi,ins_va,ins_ir,ins_ii,ins_ia, \
                            ins_pr,ins_pi,ins_pa,bran_num,delta,te_used,te_perc, \
                            dis_gone,ins_speed,av_speed])
    
    if lst_section == "":
        return

# Check if the script is run as the main module
if __name__ == "__main__":
    # Add your debugging code here
    simname = "BEL013"  # Provide a simulation name or adjust as needed
    main_option = "2"  # Adjust as needed
    time_start = "0150000"  # Adjust as needed
    time_end = "0235955"  # Adjust as needed
    option_select = "4"  # Adjust as needed
    text_input = "BranchList"  # Adjust as needed
    low_v = 488  # Adjust as needed
    high_v = None  # Adjust as needed
    time_step = None  # Adjust as needed

    # Call your main function with the provided parameters
    main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step)
