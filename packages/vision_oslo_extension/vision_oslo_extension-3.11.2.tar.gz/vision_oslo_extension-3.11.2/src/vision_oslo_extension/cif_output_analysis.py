#
# -*- coding: utf-8  -*-
#=================================================================
# Created by: Jieming Ye
# Created on: Nov 2024
# Last Modified: Nov 2024
#=================================================================
# Copyright (c) 2024 [Jieming Ye]
#
# This Python source code is licensed under the 
# Open Source Non-Commercial License (OSNCL) v1.0
# See LICENSE for details.
#=================================================================
"""
Pre-requisite: 
*.C2V.routes.txt
*.routes.itf.txt
*.routes.mon.txt
Used Input:
text_input: to locate the cif file for checking.
option_select: to define the option selected in subfunction.
Expected Output:
'00_Model_Improvement_Guidance_XX.txt'
Description:


"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
#=================================================================
# Set Information Variable
# N/A
#=================================================================

import pandas as pd
import os
import sys
from contextlib import redirect_stdout
from io import StringIO
from collections import defaultdict

from vision_oslo_extension.shared_contents import SharedMethods,SharedVariables


def main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):

    #User Interface - Welcome message:
    print("")
    print("VISION CIF Import Process Output Analyser - - - > ")
    print("")

    # check the existing of three output
    print("Three default output files are required before continue. Checking...")

    file_mon = simname + ".routes.mon.txt"
    file_route = simname + ".C2V.routes.txt"
    file_itf = simname + ".routes.itf.txt"
    file_gd = simname + ".gd"
    
    if not SharedMethods.check_existing_file(file_gd):
        SharedMethods.print_message("ERROR: Model essential file not available. Go to 'File - Check Model Layout' to generate this.","31")
        return False
    if not SharedMethods.check_existing_file(file_mon):
        return False
    if not SharedMethods.check_existing_file(file_route):
        return False
    if not SharedMethods.check_existing_file(file_itf):
        return False

    # no option is given at this stage to be think about.
    option = option_select

    # if option not in ["0","1","2","3","4","5","6"]:
    #     SharedMethods.print_message("ERROR: Error in cif_output_analysis.py. Consult Support....","31")
    #     return False
    
    if option == "0":
        SharedMethods.print_message("ERROR: Plese select an option to Continue.","31")
        return False

    else:
        if not cif_output_analysis(simname,file_mon,file_route,file_itf,file_gd):
            return False
    
                   
    return True

# main process of output file reading process.
def cif_output_analysis(simname,file_mon,file_route,file_itf,file_gd):
    # get the TIPLOC and Timing Group matching dictionary (timing group: TIPLOC)
    tiploc_group_match = check_timing_markers(file_gd)
    if not tiploc_group_match:
        return False

    # check monitor output to determine
    # 1. Missing TIPLOCs to be added [tiploc1, tiploc2]
    # 2. TIPLOCS missing platform info {tiploc1:[plt1,plt2,etc],etc}
    # 3. get error information for each train [[trainID,TIPLOC,PT,TIPLOC2,PT2],[],[]...]
    result = check_monitor_output(file_mon)
    if not result:
        return False
    tiploc_missing,tiploc_platform,monitor_error = result

    # check route output to determine
    # 1. mismatch start list [train,expected, actual]
    # 2. mismatch end list [train, expected, actual]
    result = check_c2v_output(file_route,tiploc_group_match)
    if not result:
        return False
    mismatch_start,mismatch_end = result

    # check interface file to find autoroute error message
    # 1. check output related objects for each train [[train,errortype,related object]]
    # 2. tiploc used list [tiploc1, tiploc2,etc...]
    result = check_interface_file(file_itf)
    if not result:
        return False
    autoroute_error,tiploc_used = result

    # process info and prepare the report
    try:
        guidance_report_output(simname,tiploc_missing,tiploc_platform,monitor_error,mismatch_start,mismatch_end,autoroute_error,tiploc_used) 
    except Exception as e:
        SharedMethods.print_message(f"ERROR: an unexpected error occured: {e}","31")
        return False

    return True

# return the dictionary type of tiploc and timing group matching
def check_timing_markers(file_gd):
    print("Analysing model layout file...")
    # define empty dictionary
    tiploc_group_match = {}
    count = 0
    if SharedVariables.osop_version in [1,2]:
        SharedMethods.print_message("ATTENTION: 4 digits model layout file is used. Please ensure the model is compatible with CIF import process.","33")
        s1,e1,s2,e2 = 14,22,23,30
    else:
        SharedMethods.print_message("ATTENTION: 5 digits model layout file is used. Please ensure the model is compatible with CIF import process.","33")
        s1,e1,s2,e2 = 15,23,24,31

    with open(file_gd) as fp:
        for index, line in enumerate(fp):
            header = line[:8].strip()
            if header == "LOCATION":
                timing_group = line[s1:e1].strip()
                tiploc = line[s2:e2].strip()
                tiploc_group_match[timing_group] = tiploc
                count = count + 1
            else:
                continue

    print(f"Total of {count} timing groups in the model. Reading completed.")

    return tiploc_group_match

# check monitor file and save essential information
def check_monitor_output(file_mon):
    print("Analysing CIF import monitor file...")

    tiploc_missing = []
    tiploc_platform = {}
    monitor_error = []

    with open(file_mon) as fp:
        for index, line in enumerate(fp):
            header = line[:9].strip()
            if header == "warning":
                subheader = line[11:20].strip()
                if subheader == "intermedi":
                    tiploc_missing.append(line[31:38].strip())

                elif subheader == "platform":
                    tiploc = line[34:41].strip()
                    plat = line[20:23].strip()
                    if tiploc in tiploc_platform:
                        tiploc_platform[tiploc].append(plat)
                    else:
                        tiploc_platform[tiploc] = [plat]
                else:
                    continue
            elif header =="error -":
                subheader = line[20:33].strip()
                if subheader == "search failed":
                    train = line[14:19].strip()
                    tiploc1 = line[46:53].strip()
                    plt1 = line[54:57].strip()
                    tiploc2 = line[61:68].strip()
                    plt2 = line[69:72].strip()
                    monitor_error.append([train,tiploc1,plt1,tiploc2,plt2])
                else:
                    SharedMethods.print_message(f"WARNING: unrecognized error message {line} in monitor output. Ignored...","33")
            else:
                continue

    return tiploc_missing, tiploc_platform, monitor_error

# Check C2V file and save essential information
def check_c2v_output(file_route,tiploc_group_match):
    print("Analysing CIF import C2V file...")
    mismatch_start = []
    mismatch_end = []

    train = 0
    # define another variable to record the previous line due to need to check above line.
    pre_line = ""

    with open(file_route) as fp:
        for index, line in enumerate(fp):
            header = line.split(",")[0]
            
            if header == "BS":
                train = line.split(",")[1]
            elif header == "CO":
                info = line.split(",")[1]
                if info[:5] == "TRAIN":
                    start = info[6:13].strip()
                    end = info[14:21].strip()

            elif header == "T":
                pre_header = pre_line.split(",")[0]
                if pre_header == "CO":
                    actual_start = line.split(",")[1].strip()

                    # make a judegement whether there is an end mismatch
                    start_tiploc = tiploc_group_match.get(actual_start,actual_start)
                    if start != start_tiploc:
                        mismatch_start.append([train,start,start_tiploc])

            elif header == "R":
                pre_header = pre_line.split(",")[0]
                if pre_header == "T":
                    actual_end = pre_line.split(",")[1].strip()

                    # make a judegement whether there is an end mismatch
                    end_tiploc = tiploc_group_match.get(actual_end,actual_end)
                    if end != end_tiploc:
                        mismatch_end.append([train,end,end_tiploc])

            pre_line = line

    return mismatch_start,mismatch_end

# Check itf file and save essential information
def check_interface_file(file_itf):
    print("Analysing CIF import interface file...")

    autoroute_error = []
    tiploc_used = []

    # flag to indicate its reaching tiploc section
    tiploc_flag = False

    # flag to indicate the previous line train
    previous_train = ""

    with open(file_itf) as fp:
        for index, line in enumerate(fp):
            header = line[:7].strip()
            if header == "TIPLOCS":
                tiploc_flag = True
                continue
            elif header == "AUTOMAT":
                tiploc_flag = False
            
            elif header =="ERROR:":
                train_id = line.split(",")[1].strip()
                error_type = line.split(",")[2].strip()

                if error_type in ["4","12"]: # same error type. 12 was added to support LS-1 error information
                    last_section = line.split(",")[4].strip()
                    obj_from = last_section.split(" ")[2] # from XXXXX
                    obj_to = last_section.split(" ")[5][:-1] # to signal XXXXX.
                    autoroute_error.append([train_id,obj_from,obj_to,"Unable to move between two objects (timing_group/signal)"])

                elif error_type == "5":
                    if train_id != previous_train:
                        last_section = line.split(",")[3].strip()
                        obj_from = "N/A"
                        obj_to = last_section.split(" ")[10][:-1]
                        autoroute_error.append([train_id,obj_from,obj_to,"Failed to find end of route (timing group attached)"])

                elif error_type == "2":
                    if train_id != previous_train:
                        last_section = line.split(",")[3].strip()
                        obj_from = last_section.split(" ")[9][:-1]
                        obj_to = "N/A"
                        autoroute_error.append([train_id,obj_from,obj_to,"Failed to find first routing object (timing_group/signal)"])
                
                elif error_type == "3":
                    if train_id != previous_train:
                        last_section = line.split(",")[3].strip()
                        obj_from = "N/A"
                        obj_to = last_section.split(" ")[9][:-1]
                        autoroute_error.append([train_id,obj_from,obj_to,"Failed to find last routing object (timing_group/signal)"])
                    
                elif error_type == "11":
                    last_section = line.split(",")[3].strip()
                    obj_from = last_section.split(" ")[17]
                    obj_to = "N/A"
                    autoroute_error.append([train_id,obj_from,obj_to,"Route does not match template! Unknown Reason."])

                else:
                    SharedMethods.print_message(f"WARNING: Error '{line}' is not recongized. Please contact support to add it.","33")
                
                # update previous train id
                previous_train = train_id
            
            elif header =="Summary":
                break

            # process tiploc section information
            if tiploc_flag == True:
                if line.strip() != "":
                    tiploc_used.append(line[:7].strip())
                    tiploc_used.append(line[8:15].strip())
                    tiploc_used.append(line[16:23].strip())
                    tiploc_used.append(line[24:31].strip())
                    tiploc_used.append(line[32:39].strip())
                else:
                    continue

    return autoroute_error,tiploc_used

# output guidance report based on analysis
def guidance_report_output(simname,tiploc_missing,tiploc_platform,monitor_error,mismatch_start,mismatch_end,autoroute_error,tiploc_used):
    # check if a file output exist already or not and use the next one
    fileMax = 100
    fileNo = 1

    TIPLOC_lookup = SharedMethods.get_tiploc_library()
    if TIPLOC_lookup == False:
        TIPLOC_lookup == {}

    while fileNo < fileMax:
        filename = simname + "_00_Model_Improvement_Guidance_" + str(fileNo) + ".txt"
        if silent_check_existing_file(filename):
            fileNo = fileNo + 1
            filename = simname + "_00_Model_Improvement_Guidance_" + str(fileNo) + ".txt"
        else:
            break
    if fileNo == 100:
        fileNo = 1
        filename = simname + "_00_Model_Improvement_Guidance_" + str(fileNo) + ".txt"

    
    # processing monitor error to suprress repeated error
    monitor_error_output = process_errors(monitor_error) if monitor_error else []
    autoroute_error_output = process_errors(autoroute_error) if autoroute_error else []
    mismatch_start_output = process_errors(mismatch_start) if mismatch_start else []
    mismatch_end_output = process_errors(mismatch_end) if mismatch_end else []

    
    # Open a txt file and output information line by line
    with open(filename, "w") as fp:
        fp.write("Model Improvement Gudiance\n\n")

        fp.write("Please do NOT blindly follow the instruction as this is GUIDANCE only. Proceed with consideration...\n")
        fp.write("THERE ARE TOTALLY 6 POINTS TO CONSIDER AS LISTED BELOW. CHECK THEM ALL.\n")
        fp.write("\n\n")

        fp.write(f"   1: ADD THE FOLLOWING TIPLOCS TO THE VISION MODEL. COUNT = {len(tiploc_missing)}\n")
        fp.write("NOTE: These TIPLOCs exists in CIF file but not in VISION model and causing train splitting...\n")
        fp.write("NOTE: Add with caution. You might NOT want to include TIPLOCs tha only used for freight services.\n")
        fp.write("NOTE: You could consider manually reroute freight services if not many.\n")
        fp.write("      TIPLOCS  LOCATION  \n")
        
        if tiploc_missing == []:
            fp.write("      NO ISSUE.\n")
        else:
            for item in tiploc_missing:
                line = "      " + item.rjust(7) + "  "+ TIPLOC_lookup.get(item,item) + "\n"
                fp.write(line)
        
        fp.write("\n\n")
        fp.write(f"   2: ADD PLATFORM INFORMATION TO THE FOLLOWING TIPLOCS. COUNT = {len(tiploc_platform)}\n")
        fp.write("NOTE: These TIPLOCs platform information do NOT exist in VISION.\n")
        fp.write("NOTE: Add information with caution.This can support the correct routing, solving some issue from Point 3 and 4 below.\n")
        fp.write("      TIPLOCS             LOCATIONS  MISSING_PLATFORMS  \n")

        if tiploc_platform == {}:
            fp.write("      NO ISSUE.\n")
        else:
            for key, items in tiploc_platform.items():
                line = "      " + key.rjust(7) + "  "+ TIPLOC_lookup.get(key,key)[:20].rjust(20) + "  "
                for item in items:
                    line = line + item.rjust(3) + ", "                
                line = line + "\n"
                fp.write(line)
        
        fp.write("\n\n")
        fp.write(f"   3: CHECK ROUTE SECTION BETWEEN FOLLOWING TIPLOCS. COUNT = {len(monitor_error_output)}\n")
        fp.write("NOTE: No route can be found between these two timing markers.\n")
        fp.write("NOTE: Potential reasons include: wrong/missing platform information, missing junction so a route through is impossible.\n")
        fp.write("NOTE: Check the route section until the previous TIPLOC locaction from the expected route.\n")
        fp.write("      TIPLOCS  PLAT  TIPLOCS  PLAT  AFFECTED_TRAIN_NO\n")

        if monitor_error == []:
            fp.write("      NO ISSUE.\n")
        else:
            for items in monitor_error_output:
                for index, item in enumerate(items):
                    if index == 0:
                        line = "      " + item.rjust(7) + "  "
                    elif index == 1:
                        line = line + item.rjust(4) + "  "
                    elif index == 2:
                        line = line + item.rjust(7) + "  "
                    elif index == 3:
                        line = line + item.rjust(4) + "  "
                    else:
                        line = line + item.rjust(6) + ", "

                line = line + "\n"
                fp.write(line)
        
        
        fp.write("\n\n")
        fp.write(f"   4: CHECK INFRASTRUCTURE AROUND THE FOLLOWING OBJECT. COUNT = {len(autoroute_error_output)}\n")
        fp.write("NOTE: Autoroute failed around these locations.\n")
        fp.write("NOTE: Autoroute is based on TIMING GROUPS / SIGNALS !\n")
        fp.write("NOTE: In principle, the autoroute cannot find objects in the correct sequence. Potential reasons include:.\n")
        fp.write("NOTE: a: unable to move --> Ensure no duplicate object distance, Check VISION position against object distance.\n")
        fp.write("NOTE: b: Fail to find start/end of route --> Ensure no duplicate TIPLOCs distance. Or this indicate a bug in filter. Check C2V file to confirm.\n")
        fp.write("NOTE: c: Route does not match template --> Check start / end timing group ID matching TIPLOCs.\n")
        fp.write("      OBJ FROM   OBJ END                                                FAILURE_REASON  AFFECTED_TRAIN_NO\n")

        if autoroute_error == []:
            fp.write("      NO ISSUE.\n")
        else:
            for items in autoroute_error_output:
                for index, item in enumerate(items):
                    if index == 0:
                        line = "      " + item.rjust(8) + "  "
                    elif index == 1:
                        line = line + item.rjust(8) + "  "
                    elif index == 2:
                        line = line + item.rjust(60) + "  "
                    else:
                        line = line + item.rjust(6) + ", "

                line = line + "\n"
                fp.write(line)
            
        
        fp.write("\n\n")
        fp.write(f"   5: THE FOLLOWING ORIGIN MISMATCH. CONFIRM OUT OF SCOPE. COUNT = {len(mismatch_start_output)}\n")
        fp.write("NOTE: Double check the actual origin location is as expected.\n")
        fp.write("      EXPECTED             LOCATION   ACTUAL              LOCATION  AFFECTED_TRAIN\n")

        if mismatch_start == []:
            fp.write("      NO ISSUE.\n")
        else:
            for items in mismatch_start_output:
                for index, item in enumerate(items):
                    if index == 0:
                        line = "      " + item.rjust(7) + "  "
                        line = line + TIPLOC_lookup.get(item,item)[:20].rjust(20) + "  "
                    elif index == 1:
                        line = line + item.rjust(7) + "  "
                        line = line + TIPLOC_lookup.get(item,item)[:20].rjust(20) + "  "
                    else:
                        line = line + item.rjust(6) + ", "

                line = line + "\n"
                fp.write(line)
        
        fp.write("\n\n")
        fp.write(f"   6: THE FOLLOWING DESTINATION MISMATCH. CONFIRM OUT OF SCOPE. COUNT = {len(mismatch_end_output)}\n")
        fp.write("NOTE: Double check the actual destination location is as expected.\n")
        fp.write("      EXPECTED             LOCATION   ACTUAL              LOCATION  AFFECTED_TRAIN\n")

        if mismatch_end == []:
            fp.write("      NO ISSUE.\n")
        else:
            for items in mismatch_end_output:
                for index, item in enumerate(items):
                    if index == 0:
                        line = "      " + item.rjust(7) + "  "
                        line = line + TIPLOC_lookup.get(item,item)[:20].rjust(20) + "  "
                    elif index == 1:
                        line = line + item.rjust(7) + "  "
                        line = line + TIPLOC_lookup.get(item,item)[:20].rjust(20) + "  "
                    else:
                        line = line + item.rjust(6) + ", "


                line = line + "\n"
                fp.write(line)
        

        fp.write("\n\n")
        fp.write("   CIF import analysis completed. Please improve the modal and retry the importing process.\n")
        fp.write("   Contact support or please refer to CIF import guidance for detail.\n")
    

    print(f"File '{filename}' generation completed. Check your folder.")

    return True

# Wrapper to suppress output
def silent_check_existing_file(filename):
    with StringIO() as temp_stdout, redirect_stdout(temp_stdout):
        result = SharedMethods.check_existing_file(filename)
    return result

# """Process error list to group by last four elements and collect train IDs."""
def process_errors(error_list):
    grouped_data = defaultdict(list)
    for entry in error_list:
        key = tuple(entry[1:])  # Last elements as tuple
        train_id = entry[0]     # trainID
        if train_id not in grouped_data[key]:  # Check if train_id is already added
            grouped_data[key].append(train_id)
    return [[*key, *train_ids] for key, train_ids in grouped_data.items()]

# programme running
if __name__ == "__main__":
    # Add your debugging code here
    simname = "test"  # Provide a simulation name or adjust as needed
    main_option = "1"  # Adjust as needed
    time_start = "0070000"  # Adjust as needed
    time_end = "0080000"  # Adjust as needed
    option_select = "1"  # Adjust as needed
    text_input = "test.cif"  # Adjust as needed
    low_v = None  # Adjust as needed
    high_v = None  # Adjust as needed
    time_step = None  # Adjust as needed

    # Call your main function with the provided parameters
    main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step)

