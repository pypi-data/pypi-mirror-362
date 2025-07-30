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
All mentioned in section 3.6 depending on the selected option.
Expected Output:
Different text file with different suffix. Following OSLO manual.
Description:
This script defines 14 default OSLO result extraction as defined in OSLO manual.
For each function, it processes the user input and format it into proper .opc file format. Then it creates a .bat file which is runnable in Windows environment. Note that the default osop.exe is included in the package. However, this makes the normal testing difficult to achieve without setting up proper testing configuration file. The reason is the command osop is a dedicated command from osop.exe, which is not default runnable Windows command.
However, user can double click the .bat file to validate if it works for its purpose or not.

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
#=================================================================
# Set Information Variable
# N/A
#=================================================================

# from shared_contents import SharedMethods
from vision_oslo_extension.shared_contents import SharedMethods


def main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):

    #User Interface - Welcome message:
    print("")
    print("VISION OSLO Default Extraction - - - > ")
    print("")   

    # get simulation name name from input
    print("Checking Result File...")
    # simname = input()

    if not SharedMethods.check_oofresult_file(simname):
        return False
    
    if option_select == '0':
        SharedMethods.print_message("ERROR: Please select an Option to proceed.","31")
        return False
    
    if not main_menu(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):
        return False

    return True


#============Main Class: For Multiple Extraction================
def main_menu(simname, option, time_start, time_end, option_select, text_input, low_v,high_v, time_step):


    # # user input selection
    # print("\nPlease select from the list what you want to do:(awaiting input)")
    # print("1: Listing of electrical file")
    # print("2: Snapshot")
    # print("3: Individual train step output")
    # print("4: Maximum currents and minimum and maximum voltages")
    # print("5: Train high voltage summary")
    # print("6: Train low voltage summary")
    # print("7: Average MW and MVAr demoands in supply points, metering points, static VAr compensators and motor alternators")
    # print("8: Feeder step output")
    # print("9: Branch step output")
    # print("10: Transformer step output")
    # print("11: Smoothed feeder currents")
    # print("12: Smoothed branch currents")
    # print("13: Supply point persistent currents (development in progress)")
    # print("14: Output to data files")
    # print("15: One stop extraction - For AC Average Power Spreadsheet")
    # print("16: One stop extraction - For DC Smoothed Current Spreadsheet")
    # print("0: Exit the programme")
    
    option = option

    if option not in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"]:
        SharedMethods.print_message("ERROR: Contact Support. Error in oslo_extraction.py --> main_menu","31")
        return False


    if option == "0":
        SharedMethods.print_message("ERROR: Contact Support. Error in Option GUI (oslo_extraction.py --> main_menu)","31")
        return False

    if option == "1":
        if not list_extract(simname, time_start, time_end, option_select):
            return False
        
    elif option == "2":
        if not snapshot(simname, time_start):
            return False

    elif option == "3":
        if not train_step(simname, time_start, time_end, option_select, text_input):
            return False

    elif option == "4":
        if not min_max(simname):
            return False
        
    elif option == "5":
        if not train_highv(simname, option_select, high_v):
            return False

    elif option == "6":
        if not train_lowv(simname, option_select, low_v):
            return False

    elif option == "7":
        if not average_demand(simname, time_start, time_end, option_select, text_input, time_step):
            return False

    elif option == "8":
        if not feeder_step(simname, time_start, time_end, option_select, text_input):
            return False

    elif option == "9":
        if not branch_step(simname, time_start, time_end, option_select, text_input):
            return False

    elif option == "10":
        if not tranx_step(simname, time_start, time_end, option_select, text_input):
            return False

    elif option == "11":
        if not feeder_smooth(simname, option_select, text_input, time_step):
            return False

    elif option == "12":
        if not branch_smooth(simname, option_select, text_input, time_step):
            return False

    elif option == "13":
        if not persist_current(simname):
            return False

    elif option == "14":
        if not output_data(simname):
            return False

    print("")
    print("oslo extraction loop completed. Check information above")
    print("")
   
    return True

#=============Option 1 List Extraction==========================
def list_extract(simname, time_start, time_end, option_select):

    print("List Input File Process" )
    print(f"\nOption selected --> Option {option_select}")
    # print("1: List Input File" )
    # print("2: List Input File From Start to End")
    # print("3: List Input File Header Only")
    # print("0: Exit the Programme")

    option = option_select

    if option not in ["1","2","3","0"]:
        SharedMethods.print_message("ERROR: Contact Support. oslo_extraction.py-->list_extract","31")
        return False

    # define the default osop command
        
    opcname = simname + ".opc"
    
    if option == "1":
        # prepare the OPC file
        with open(opcname,"w") as fopc:
            fopc.writelines("LIST INPUT FILE\n")
        # Running the OSOP extraction
        if not SharedMethods.osop_running(simname):
            return False

    elif option == "2":
        # User defined time windows extraction
        time_start = SharedMethods.time_input_process(time_start,1)
        time_end = SharedMethods.time_input_process(time_end,1)

        if time_start == False or time_end == False:
            return False
        
        # prepare the OPC file
        with open(opcname,"w") as fopc:
            fopc.writelines("LIST INPUT FILE FROM "+time_start+" TO "+time_end+"\n")
        # Running the OSOP extraction
        if not SharedMethods.osop_running(simname):
            return False
        
    elif option == "3":
        # prepare the OPC file
        with open(opcname,"w") as fopc:
            fopc.writelines("LIST INPUT FILE HEADER ONLY\n")
        # Running the OSOP extraction
        if not SharedMethods.osop_running(simname):
            return False

    return True

#=============Option 2 Snapshot==========================      
def snapshot(simname, time_start):

    time = SharedMethods.time_input_process(time_start,1)

    if time == False:
        return False

    # define the default osop command
        
    opcname = simname + ".opc"

    with open(opcname,"w") as fopc:
        fopc.writelines("SNAPSHOT AT "+time+"\n")

    if not SharedMethods.osop_running(simname):
        return False
       
    return True

#=============Option 3 Train Step Output==========================
def train_step(simname, time_start, time_end, option_select, text_input):

    # print("\nPlease select the option:(awaiting input)")
    # print("1: Single Train Step Output")
    # print("2: Multiple Train Step Output:")
    # print("   A text file named as ""TrainList"" is required")
    # print("3: Multiple Train Step Output:")
    # print("   Manually Input one by one")
    # print("0: Exit the Programme")
    print(f"\nOption selected --> Option {option_select}")

    option = option_select

    if option not in ["1","2","3","0"]:
         SharedMethods.print_message("ERROR: Contact Support. oslo_extraction.py-->train_step","31")
         return False

    # User defined time windows extraction
    time_start = SharedMethods.time_input_process(time_start,1)
    time_end = SharedMethods.time_input_process(time_end,1)

    if time_start == False or time_end == False:
        return False

    if option == "1":
        print(f"\nThe VISION train ID (1-9999): {text_input}")
        train_id = int(text_input)
        if not train_step_one(simname,train_id,time_start,time_end):
            return False
    
    elif option == "2":
        print("\nProsessing trains listed in TrainList.txt")        

        train_list = "TrainList.txt"

        text_input = SharedMethods.file_read_import(train_list,simname)

        if text_input == False:
            return False

        # processing the list
        for items in text_input:
            train_step_one(simname,int(items),time_start,time_end)

    elif option == "3":
        while True:   
            print("\nPlease enter the VISION train ID (1-9999) or 0 to Finish")
            finish = input()
            if finish == "0": break
            train_step_one(simname,int(finish),time_start,time_end)
           
    return True

def train_step_one(simname,train_id,time_start,time_end):
    
    # define the default osop command
        
    opcname = simname + ".opc"

    if 1 <= len(str(train_id)) <= 3:
        train_no = format(train_id,'03d')
    elif 4 <= len(str(train_id)) <= 5:
        train_no = format(train_id,'05d')
    else:
        SharedMethods.print_message(f"ERROR: Error train step output for train {train_id}: invalid train No. (1-5 digits)","31")
        return False

    with open(opcname,"w") as fopc:
        fopc.writelines("TRAIN "+train_no+" STEPS FROM "+time_start+" TO "+time_end+"\n")

    if not SharedMethods.osop_running(simname):
        SharedMethods.print_message(f"ERROR: Error when extracting train step output for train {train_id}.","31")
        return False

    #rename the file
    old_name = simname + ".osop.ds1"
    new_name = simname + "_train_"+ train_no + ".osop.ds1"

    SharedMethods.file_rename(old_name,new_name)
        
    return True

#=============Option 4 Min Max Value==========================      
def min_max(simname):

    print("\nMinimum and Maximum Values will be extracted...")

    # define the default osop command
        
    opcname = simname + ".opc"

    with open(opcname,"w") as fopc:
        fopc.writelines("MINMAX VALUES REQUIRED\n")

    if not SharedMethods.osop_running(simname):
        return False

    return True

#=============Option 5 High Voltage Summary==========================      
def train_highv(simname, option_select, high_v):

    print(f"\nThe 4 digits threshold in XX.X kV format {high_v} kV")
    threshold = high_v

    # define the default osop command
        
    opcname = simname + ".opc"

    with open(opcname,"w") as fopc:
        fopc.writelines("TRAIN VOLTS MAX "+threshold+" KV\n")

    if not SharedMethods.osop_running(simname):
        return False

    #rename the file
    old_name = simname + ".osop.vlt"
    new_name = simname + "_maxtime.osop.vlt"

    SharedMethods.file_rename(old_name,new_name)
       
    return True

#=============Option 6 Low Voltage Summary==========================      
def train_lowv(simname, option_select, low_v):

    print(f"\nThe 4 digits threshold in XX.X kV format {low_v} kV")
    threshold = low_v

    print("Low Voltage Summary" )
    print(f"\nOption selected --> Option {option_select}")

    option = option_select

    if option not in ["1","2","0"]:
        SharedMethods.print_message("ERROR: Contact Support. oslo_extraction.py-->train_lowv","31")
        return False

    # define the default osop command
        
    opcname = simname + ".opc"

    if option == "1":
        with open(opcname,"w") as fopc:
            fopc.writelines("TRAIN VOLTS MIN "+threshold+" KV\n")

        if not SharedMethods.osop_running(simname):
            return False

        old_name = simname + ".osop.vlt"
        new_name = simname + "_mintime.osop.vlt"

        SharedMethods.file_rename(old_name,new_name)
    else:
        with open(opcname,"w") as fopc:
            fopc.writelines("TRAIN VOLTS MIN "+threshold+" KV DETAILED OUTPUT\n")

        if not SharedMethods.osop_running(simname):
            return False

        old_name = simname + ".osop.vlt"
        new_name = simname + "_mindetail.osop.vlt"

        SharedMethods.file_rename(old_name,new_name)
          
    return True

#=============Option 7 average demand==========================      
def average_demand(simname, time_start, time_end, option_select, text_input, time_step):

    # print("\nPlease select the option:(awaiting input)")
    # print("1: Single Feeder Output")
    # print("2: Multiple Feeder Output:")
    # print("   A text file named as ""FeederList"" is required")
    # print("3: Multiple Feeder Output:")
    # print("   Manually input one by one")
    # print("0: Exit the Programme")

    print("Average Power Demand" )
    print(f"\nOption selected --> Option {option_select}")

    option = option_select

    if option not in ["1","2","3","0"]:
        SharedMethods.print_message("ERROR: Contact Support. oslo_extraction.py-->average_demand","31")
        return False

    # User defined time windows extraction
    time_start = SharedMethods.time_input_process(time_start,1)
    time_end = SharedMethods.time_input_process(time_end,1)

    if time_start == False or time_end == False:
        return False

    # User defined time windows extraction
    print(f"\nThe time windows (in minutes) for average analysis (max 2 digits) {time_step} min.")

    # time_step = input()
    time = time_step.rjust(2)

    if option == "1":
        print(f"\nThe Supply Point Name(maximum 4 digits): {text_input}")
        feeder_id = text_input
        if not feeder_avg_one(simname,feeder_id,time_start,time_end,time):
            return False
    elif option == "2":
        print("\nProsessing feeders listed in FeederList.txt")        
        # prepare the list file
        feeder_list = "FeederList.txt"

        text_input = SharedMethods.file_read_import(feeder_list,simname)

        if text_input == False:
            return False

        # processing the list
        for items in text_input:
            #print(items)
            feeder_avg_one(simname,items,time_start,time_end,time)

    elif option == "3":
        while True:   
            print("\nPlease enter the Supply Point Name(maximum 4 digits) or 0 to Finish")
            finish = input()
            if finish == "0": break
            feeder_avg_one(simname,finish,time_start,time_end,time)
           
    return True

def feeder_avg_one(simname,feeder_id,time_start,time_end,time):
    
    # define the default osop command
        
    opcname = simname + ".opc"

    if len(feeder_id) < 1 or len(feeder_id) > 4:
        SharedMethods.print_message(f"ERROR: Error feeder output for feeder {feeder_id}: Invalid feeder ID (max 4 digit)","31")
        return False

    feeder = feeder_id.rjust(4) # right justified 4 digits

    with open(opcname,"w") as fopc:
        fopc.writelines("POWER CALCS EVERY "+time+" MINUTES FROM "+time_start+" TO "+time_end+" FOR 01 ITEMS\n")
        fopc.writelines("           "+feeder+"\n")
    if not SharedMethods.osop_running(simname):
        SharedMethods.print_message(f"ERROR: Error when extracting feeder output for feeder {feeder}.","31")
        return False

    #rename the file
    old_name = simname + ".osop.pwr"
    new_name = simname + "_"+ feeder + ".osop.pwr"

    SharedMethods.file_rename(old_name,new_name)
        
    return True

#=============Option 8 Feeder Step Output==========================
def feeder_step(simname, time_start, time_end, option_select, text_input):

    # print("\nPlease select the option:(awaiting input)")
    # print("1: Single Feeder Step Output")
    # print("2: Multiple Feeder Step Output:")
    # print("   A text file named as ""FeederList"" is required")
    # print("3: Multiple Feeder Step Output:")
    # print("   Manually input one by one")
    # print("0: Exit the Programme")

    print("Feeder Step Output" )
    print(f"\nOption selected --> Option {option_select}")

    option = option_select

    if option not in ["1","2","3","0"]:
        SharedMethods.print_message("ERROR: Contact Support. oslo_extraction.py-->feeder_step","31")
        return False

    # User defined time windows extraction
    time_start = SharedMethods.time_input_process(time_start,1)
    time_end = SharedMethods.time_input_process(time_end,1)

    if time_start == False or time_end == False:
        return False

    if option == "1":
        print(f"\nThe Supply Point Name(maximum 4 digits): {text_input}")
        feeder_id = text_input
        if not feeder_step_one(simname,feeder_id,time_start,time_end):
            return False
    elif option == "2":
        print("\nProsessing feeders listed in FeederList.txt")        
        # prepare the list file
        feeder_list = "FeederList.txt"

        text_input = SharedMethods.file_read_import(feeder_list,simname)

        if text_input == False:
            return False

        # processing the list
        for items in text_input:
            #print(items)
            feeder_step_one(simname,items,time_start,time_end)

    elif option == "3":
        while True:   
            print("\nPlease enter the Supply Point Name(maximum 4 digits) or 0 to Finish")
            finish = input()
            if finish == "0": break
            feeder_step_one(simname,finish,time_start,time_end)
           
    return True

def feeder_step_one(simname,feeder_id,time_start,time_end):
    
    # define the default osop command
        
    opcname = simname + ".opc"

    if len(feeder_id) < 1 or len(feeder_id) > 4:
        SharedMethods.print_message(f"ERROR: Error feeder output for feeder {feeder_id}: Invalid feeder ID (max 4 digit)","31")
        return False

    feeder = feeder_id.ljust(4) # left justified 4 digits

    with open(opcname,"w") as fopc:
        fopc.writelines("FEEDER STEPS FROM "+time_start+" TO "+time_end+" FOR 01 ITEMS\n")
        fopc.writelines("           "+feeder+"\n")
    if not SharedMethods.osop_running(simname):
        SharedMethods.print_message(f"ERROR: Error when extracting feeder step output for feeder {feeder}.","31")
        return False

    #rename the file
    old_name = simname + ".osop.d4"
    new_name = simname + "_"+ feeder + ".osop.d4"

    SharedMethods.file_rename(old_name,new_name)
        
    return True

#=============Option 9 Branch Step Output==========================
def branch_step(simname, time_start, time_end, option_select, text_input):

    # print("\nPlease select the option:(awaiting input)")
    # print("1: Single Branch Node Step Output")
    # print("2: Multiple Branch Node Step Output:")
    # print("   A text file named as ""BranchNodeList"" is required")
    # print("3: Multiple Branch Node Step Output:")
    # print("   Manually input one by one")
    # print("0: Exit the Programme")

    print("Branch Step Output" )
    print(f"\nOption selected --> Option {option_select}")

    option = option_select

    if option not in ["1","2","3","0"]:
        SharedMethods.print_message("ERROR: Contact Support. oslo_extraction.py-->branch_step","31")
        return False

    # User defined time windows extraction
    time_start = SharedMethods.time_input_process(time_start,1)
    time_end = SharedMethods.time_input_process(time_end,1)

    if time_start == False or time_end == False:
        return False

    if option == "1":
        print(f"\nThe Branch Node Name(Format:XXXX/X): {text_input}")
        branch_id = text_input
        if not branch_step_one(simname,branch_id,time_start,time_end):
            return False
    elif option == "2":
        print("\nProsessing branches listed in BranchNodeList.txt")        
        # prepare the list file
        branch_list = "BranchNodeList.txt"
        text_input = SharedMethods.file_read_import(branch_list,simname)

        if text_input == False:
            return False
        
        # processing the list
        for items in text_input:
            #print(items)
            branch_step_one(simname,items,time_start,time_end)

    elif option == "3":
        while True:   
            print("\nPlease enter the Branch Node Name(Format:XXXX/X) or 0 to Finish")
            finish = input()
            if finish == "0": break
            branch_step_one(simname,finish,time_start,time_end)
           
    return True

def branch_step_one(simname,branch_id,time_start,time_end):
    
    # define the default osop command
        
    opcname = simname + ".opc"

    if len(branch_id) <= 6:
        if branch_id[-2:] in ['/E','/S']:
            branch = branch_id[:len(branch_id)-2].ljust(4)+branch_id[-2:]
        else:
            SharedMethods.print_message(f"ERROR: Error branch step output for branch {branch_id}: Wrong Format","31")
            return False
    else:       
        SharedMethods.print_message(f"ERROR: Error branch step output for branch {branch_id}: Wrong Format","31")
        return False

    with open(opcname,"w") as fopc:
        fopc.writelines("BRANCH STEPS FROM "+time_start+" TO "+time_end+" FOR 01 ITEMS\n")
        fopc.writelines("           "+branch+"\n")
    if not SharedMethods.osop_running(simname):
        SharedMethods.print_message(f"ERROR: Error when extracting branch step output for branch {branch}.","31")
        return False

    #rename the file
    old_name = simname + ".osop.d4"
    new_name = simname + "_"+ branch[:4]+"-"+ branch[-1:]+ ".osop.d4"

    SharedMethods.file_rename(old_name,new_name)
        
    return True

#=============Option 10 Transformer Step Output==========================
def tranx_step(simname, time_start, time_end, option_select, text_input):

    # print("\nPlease select the option:(awaiting input)")
    # print("1: Single Transformer Step Output")
    # print("2: Multiple Transformer Step Output:")
    # print("   A text file named as ""TransformerList"" is required")
    # print("3: Multiple Transformer Step Output:")
    # print("   Manually input one by one")
    # print("0: Exit the Programme")

    print("Transformer Step Output" )
    print(f"\nOption selected --> Option {option_select}")

    option = option_select

    if option not in ["1","2","3","0"]:
        SharedMethods.print_message("ERROR: Contact Support. oslo_extraction.py-->tranx_step","31")
        return False

    # User defined time windows extraction
    time_start = SharedMethods.time_input_process(time_start,1)
    time_end = SharedMethods.time_input_process(time_end,1)

    if time_start == False or time_end == False:
        return False

    if option == "1":
        print(f"\nThe Transformer Name(maximum 4 digits): {text_input}")
        tranx_id = text_input
        if not tranx_step_one(simname,tranx_id,time_start,time_end):
            return False
    elif option == "2":
        print("\nProsessing tranx listed in TransformerList.txt")        
        # prepare the list file
        tranx_list = "TransformerList.txt"
        text_input = SharedMethods.file_read_import(tranx_list,simname)

        if text_input == False:
            return False

        # processing the list
        for items in text_input:
            #print(items)
            tranx_step_one(simname,items,time_start,time_end)

    elif option == "3":
        while True:   
            print("\nPlease enter the Supply Point Name(maximum 4 digits) or 0 to Finish")
            finish = input()
            if finish == "0": break
            tranx_step_one(simname,finish,time_start,time_end)
           
    return True

def tranx_step_one(simname,tranx_id,time_start,time_end):
    
    # define the default osop command
        
    opcname = simname + ".opc"

    if len(tranx_id) < 1 or len(tranx_id) > 4:
        SharedMethods.print_message(f"ERROR: Error tranx output for feeder {tranx_id}: Invalid tranx ID (max 4 digit)","31")
        return False

    tranx = tranx_id.ljust(4) # right justified 4 digits

    with open(opcname,"w") as fopc:
        fopc.writelines("TRANSFORMER STEPS FROM "+time_start+" TO "+time_end+" FOR 01 ITEMS\n")
        fopc.writelines("           "+tranx+"\n")
    if not SharedMethods.osop_running(simname):
        SharedMethods.print_message(f"ERROR: Error when extracting transformer step output for transformer {tranx}.","31")
        return False

    #rename the file
    old_name = simname + ".osop.d4"
    new_name = simname + "_"+ tranx + ".osop.d4"

    SharedMethods.file_rename(old_name,new_name)
        
    return True

#=============Option 11 Smoothed Feeder Current==========================
def feeder_smooth(simname, option_select, text_input, time_step):

    # print("\nPlease select the option:(awaiting input)")
    # print("1: Single Feeder Smoothed Current Output")
    # print("2: Multiple Feeder Smoothed Current Output:")
    # print("   A text file named as ""FeederList"" is required")
    # print("3: Multiple Feeder Smoothed Current Output:")
    # print("   Manually input one by one")
    # print("0: Exit the Programme")

    print("Feeder Smoothed Output" )
    print(f"\nOption selected --> Option {option_select}")

    option = option_select

    if option not in ["1","2","3","0"]:
        SharedMethods.print_message("ERROR: Contact Support. oslo_extraction.py-->feeder_smooth","31")
        return False

    # print("\nPlease select the analysis option:(awaiting input)")
    # print("1: Normal direction of real power flow")
    # print("2: Reverse direction of real power flow")

    # option1 = input()
    option1 = "all"

    # User defined time windows extraction
    print(f"\nThe time steps analysied for (max 3 digits): {time_step} steps")

    time = time_step.rjust(3)

    if option == "1":
        print(f"\nThe Supply Point Name(maximum 4 digits): {text_input}")
        feeder_id = text_input
        if not feeder_smooth_one(simname,feeder_id,time,option1):
            return False
    elif option == "2":
        print("\nProsessing feeders listed in FeederList.txt")        
        # prepare the list file
        feeder_list = "FeederList.txt"

        text_input = SharedMethods.file_read_import(feeder_list,simname)

        if text_input == False:
            return False

        # processing the list
        for items in text_input:
            #print(items)
            feeder_smooth_one(simname,items,time,option1)

    elif option == "3":
        while True:   
            print("\nPlease enter the Supply Point Name(maximum 4 digits) or 0 to Finish")
            finish = input()
            if finish == "0": break
            feeder_smooth_one(simname,finish,time,option1)
           
    return True

def feeder_smooth_one(simname,feeder_id,time,option1):
    
    # define the default osop command
        
    opcname = simname + ".opc"

    if len(feeder_id) < 1 or len(feeder_id) > 4:
        SharedMethods.print_message(f"ERROR: Error feeder output for feeder {feeder_id}: Invalid feeder ID (max 4 digit)","31")
        return False

    feeder = feeder_id.rjust(4) # right justified 4 digits

    # if option1 == "1":
    #     add = ""
    # else:
    #     add = " (R)"
    
    add = ""
    with open(opcname,"w") as fopc:
        fopc.writelines("FEEDER AMPS OVER "+time+" STEPS FOR 01 ITEMS"+add+"\n")
        fopc.writelines("           "+feeder+"\n")
    if not SharedMethods.osop_running(simname):
        SharedMethods.print_message(f"ERROR: Error when extracting feeder smooth output for feeder {feeder}.","31")
        return False

    #rename the file
    old_name = "fort.12"
    new_name = feeder + "_normal_fort.12"

    SharedMethods.file_rename(old_name,new_name)

    add = " (R)"
    with open(opcname,"w") as fopc:
        fopc.writelines("FEEDER AMPS OVER "+time+" STEPS FOR 01 ITEMS"+add+"\n")
        fopc.writelines("           "+feeder+"\n")
    if not SharedMethods.osop_running(simname):
        SharedMethods.print_message(f"ERROR: Error when extracting feeder reverse smooth output for feeder {feeder}.","31")
        return False

    #rename the file
    old_name = "fort.12"
    new_name = feeder + "_reverse_fort.12"

    SharedMethods.file_rename(old_name,new_name)
        
    return True

#=============Option 12 Branch Smoothed Output==========================
def branch_smooth(simname, option_select, text_input, time_step):

    # print("\nPlease select the option:(awaiting input)")
    # print("1: Single Branch Node Smoothed Current Output")
    # print("2: Multiple Branch Node Smoothed Current Output:")
    # print("   A text file named as ""BranchNodeList"" is required")
    # print("3: Multiple Branch Node Smoothed Current Output:")
    # print("   Manually input one by one")
    # print("0: Exit the Programme")

    print("Branch Smoothed Output" )
    print(f"\nOption selected --> Option {option_select}")

    option = option_select

    if option not in ["1","2","3","0"]:
        SharedMethods.print_message("ERROR: Contact Support. oslo_extraction.py-->branch_smooth","31")
        return False

    # User defined time windows extraction
    print(f"\nThe time steps analysied for (max 3 digits): {time_step} steps")

    # time_step = input()

    time = time_step.rjust(3)

    if option == "1":
        print(f"\nThe Branch Node Name(Format:XXXX/X): {text_input}")
        branch_id = text_input
        if not branch_smooth_one(simname,branch_id,time):
            return False
    elif option == "2":
        print("\nProsessing branches listed in BranchNodeList.txt")        
        # prepare the list file
        branch_list = "BranchNodeList.txt"

        text_input = SharedMethods.file_read_import(branch_list,simname)

        if text_input == False:
            return False

        # processing the list
        for items in text_input:
            #print(items)
            branch_smooth_one(simname,items,time)

    elif option == "3":
        while True:   
            print("\nPlease enter the Branch Node Name(Format:XXXX/X) or 0 to Finish")
            finish = input()
            if finish == "0": break
            branch_smooth_one(simname,finish,time)
           
    return True

def branch_smooth_one(simname,branch_id,time):
    
    # define the default osop command
        
    opcname = simname + ".opc"

    if len(branch_id) <= 6:
        if branch_id[-2:] in ['/E','/S']:
            branch = branch_id[:len(branch_id)-2].ljust(4)+branch_id[-2:]
        else:
            SharedMethods.print_message(f"ERROR: Error branch step output for branch {branch_id}: Wrong Format","31")
            return False
    else:       
        SharedMethods.print_message(f"ERROR: Error branch step output for branch {branch_id}: Wrong Format","31")
        return False

    with open(opcname,"w") as fopc:
        fopc.writelines("BRANCH AMPS OVER "+time+" STEPS FOR\n")
        fopc.writelines(branch+"\n")
    if not SharedMethods.osop_running(simname):
        SharedMethods.print_message(f"ERROR: Error when extracting branch smooth output for branch {branch}.","31")
        return False

    #rename the file
    old_name = simname + ".osop.mxn"
    new_name = simname + "_"+ branch[:4]+"-"+ branch[-1:]+ ".osop.mxn"

    SharedMethods.file_rename(old_name,new_name)
        
    return True

#=============Option 13 in progress==========================      
def persist_current(simname):

    print("\nMinimum and Maximum Values will be extracted...")

    # define the default osop command
        
    opcname = simname + ".opc"

    with open(opcname,"w") as fopc:
        fopc.writelines("MINMAX VALUES REQUIRED\n")

    if not SharedMethods.osop_running(simname):
        return False

    return True

#=============Option 14 Output Data==========================      
def output_data(simname):

    print("\nOutput d1 and d3 file...")

    # define the default osop command
        
    opcname = simname + ".opc"

    with open(opcname,"w") as fopc:
        fopc.writelines("DATA FILE OUTPUT\n")

    if not SharedMethods.osop_running(simname):
        return False

    return True

#==========================================================================

# Check if the script is run as the main module
if __name__ == "__main__":
    # Add your debugging code here
    simname = "StraightLine1"  # Provide a simulation name or adjust as needed
    main_option = "6"  # Adjust as needed
    time_start = "0070000"  # Adjust as needed
    time_end = "0080000"  # Adjust as needed
    option_select = "1"  # Adjust as needed
    text_input = "1"  # Adjust as needed
    low_v = '.488'  # Adjust as needed
    high_v = None  # Adjust as needed
    time_step = None  # Adjust as needed

    # Call your main function with the provided parameters
    main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step)

