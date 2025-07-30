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
cif file.
CIF_selection.csv
Used Input:
text_input: to locate the cif file for checking.
option_select: to define the option selected in subfunction.
Expected Output:
Several .csv files or new CIF files depending on the option selected.
Description:
This script defines the CIF file reading process and filter out services which is not needed.
In cif_data_action(),it saves information into various list to be converted to a panda dataframe later. The readable_format() function is relatively straightforward to follow. Note that due to the size of the output file, saving to excel format is deemed to be super slow.
In cif_remove_process(), it opens two file simultaneously, one original CIF, one new CIF. It reads individual train text data into a lines_to_read list, and process this list based on the removal principle and if the trains are needed, the outputs are output to the new CIF file.
In cif_remove_diesel(), it analysing the CR header within the lines_to_read list. Each mode change within CR header line will trigger the termination of a train and generate a new train info using the CR header line information plus the common information in BS, BX line. It manipulates the LT, LO header line information to fit the standard CIF format.
Other functions logic is relative straightforward.

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
# V1.1 (Jieming Ye) - Retain AA record as used in CIF import process
# V1.2 (Jieming Ye) 03/10/2024 - Add function to remove specific TIPLOC
# V1.3 (Jieming Ye) 27/11/2024 - Add function to remove specific platforms
#=================================================================
# Set Information Variable
# N/A
#=================================================================

import pandas as pd
import os

from vision_oslo_extension.shared_contents import SharedMethods


def main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):

    #User Interface - Welcome message:
    print("")
    print("Common Interface File (CIF) Processor - - - > ")
    print("")

    filename = text_input
    if not SharedMethods.check_existing_file(filename):
        return False

    # user input selection
    # 1: Output to readable format.
    # 2: Filter out Diesel Services
    # 3: Filter out services by TIPLOC
    # 4: Filter out by TOC
    # 5: Filter out by Train No in CIF
    # 6: Remove specific TIPLOC from CIF
    # 7: Remove specific platform and TIPLOC combination

    option = option_select

    if option not in ["0","1","2","3","4","5","6","7"]:
        SharedMethods.print_message("ERROR: Error in cif_prepare.py. Consult Support....","31")
        return False
    
    if option == "0":
        SharedMethods.print_message("ERROR: Plese select an option to Continue.","31")
        return False
    
    elif option == "1":
        result = readable_format(filename,option)

    elif option == "2":
        cif_remove_process(filename,option,None)

    else:
        file_select = 'CIF_selection.csv'
        if not SharedMethods.check_existing_file(file_select):
            return False
        
        selection_list = selection_reading(file_select,option)
        # option 3: select all services pass thourgh selected TIPLOC list, hence
        # need to covert the TIPLOC list to a train list
        if option == "3": # filter by TIPLOC
            result = readable_format(filename,option) # get timetable dataframe
            selection_list = find_train_number(result,selection_list)

        # option 7: combination of TIPLOC and platform, hence need to append TIPLOC to 
        # platform selection list.
        if option == "7":
            selection_list = selection_list_append_same_lenth_info(file_select,selection_list,option)

        cif_remove_process(filename,option,selection_list)
       
    return True

# Action on the CIF based on the Header selection
def cif_data_action(line,header_record,train_info,timetable_info,change_info,TIPLOC_lookup,train_id):
    if header_record == "HD":
        #print(line.rstrip()) # remove training space
        return

    if header_record == "TI": # TIPLOC insert record
        return
    
    if header_record == "TA":  # TIPLOC amend record
        return

    if header_record == "TD": # TIPLOC delete record
        return
    
    if header_record == "AA": # Assocated records
        return
    
    if header_record == "BS": #  Basic schedule record
        
        info1 = (line[2:3].strip() or None)   # Transaction Type
        info2 = (line[3:9].strip() or None)   # Train UID
        info3 = (line[9:15].strip() or None)   # Dates run from
        info4 = (line[15:21].strip() or None)   # Dates run to
        info5 = (line[21:22].strip() or None)   # Monday
        info6 = (line[22:23].strip() or None)   # Tuesday
        info7 = (line[23:24].strip() or None)   # Wednesday
        info8 = (line[24:25].strip() or None)   # Thursday
        info9 = (line[25:26].strip() or None)   # Friday
        info10 = (line[26:27].strip() or None)   # Saturday
        info11 = (line[27:28].strip() or None)   # Sunday
        info12 = (line[28:29].strip() or None)   # Bank Holiday
        info13 = (line[29:30].strip() or None)   # Train Status
        info14 = (line[30:32].strip() or None)   # Train Category
        # 03/10/2024 Append a single quote mark to aviod scientifit number shown in Excel -> not quite work
        # info15 = (" " + line[32:36].strip()) if line[32:36].strip() else None   # Train Identity
        info15 = (line[32:36].strip() or None)   # Train Identity
        info16 = (line[36:40].strip() or None)   # Headcode
        info17 = (line[40:41].strip() or None)   # Course Indicator
        info18 = (line[41:49].strip() or None)   # Train service code
        info19 = (line[49:50].strip() or None)   # Business Sector
        info20 = (line[50:53].strip() or None)   # Power Type
        info21 = (line[53:57].strip() or None)   # Timing Load
        info22 = (line[57:60].strip() or None)   # Speed
        info23 = (line[60:66].strip() or None)   # Operating Chars
        info24 = (line[66:67].strip() or None)   # Train Class
        info25 = (line[67:68].strip() or None)   # Sleepers
        info26 = (line[68:69].strip() or None)   # Reservations
        info27 = (line[69:70].strip() or None)   # Connect Indicator
        info28 = (line[70:74].strip() or None)   # Catering Code
        info29 = (line[74:78].strip() or None)   # Service Branding
        info30 = (line[78:79].strip() or None)   # Spare
        info31 = (line[79:80].strip() or None)   # STP Indicator
        train_info.append([train_id,info1,info2,info3,info4,info5,info6,info7,info8, \
                           info9,info10,info11,info12,info13,info14,info15,info16,info17,info18, \
                           info19,info20,info21,info22,info23,info24,info25,info26,info27,info28, \
                           info29,info30,info31])
        #print(train_info[train_id-1])
        
        return
    
    if header_record == "BX":
        info1 = (line[6:11].strip() or None)  # UIC code
        info2 = (line[11:13].strip() or None)  # ATOC Code
        info3 = (line[13:14].strip() or None)  # Applicable Tiemtable Code
        info4 = (line[14:22].strip() or None)  # Retail Service ID
        train_info[train_id-1] += [info1,info2,info3,info4,0,0,0]
        #print(train_info[train_id-1])
        
        return
    
    if header_record == "LO":
        info1 = (line[2:9].strip() or None)  # TIPLOC Location        
        train_info[train_id-1][37] = TIPLOC_lookup.get(info1,info1) # origin
        
        hour = line[10:12].strip()
        minute = line[12:14].strip()
        if line[14:15].strip() == "H":
            sec = "30"
        else:
            sec = "00"

        info2 = None  # Arrival Time
        info3 = hour+":"+minute+":"+sec  # Scheduled depature time
        info4 = info3 # Time
        info5 = (line[19:22].strip() or None) # Platform
        info6 = (line[22:25].strip() or None) # Line
        info7 = None # Path
        info8 = (line[29:41].strip() or None)  # Activity
        info9 = (line[25:27].strip() or None)  # Engineering Allowance
        info10 = (line[27:29].strip() or None)  # Pathing Allowance
        info11 = (line[41:43].strip() or None)  # Performance Allowance

        timetable_info.append([train_id,info1,TIPLOC_lookup.get(info1,info1),info2, \
                               info3,info4,info5,info6,info7,info8,info9,info10,info11])
        return
    
    if header_record == "LI":
        
        info1 = (line[2:9].strip() or None)  # TIPLOC Location

        if line[15:19].strip() == "":
            info2 = None  # Arrival Time
            
            hour = line[20:22].strip()
            minute = line[22:24].strip()
            if line[24:25].strip() == "H":
                sec = "30"
            else:
                sec = "00"
            info3 = hour+":"+minute+":"+sec  # Scheduled Passing Time
        else:   
            hour = line[10:12].strip()
            minute = line[12:14].strip()
            if line[14:15].strip() == "H":
                sec = "30"
            else:
                sec = "00"
            info2 = hour+":"+minute+":"+sec  # Scheduled Arrival Time

            hour = line[15:17].strip()
            minute = line[17:19].strip()
            if line[19:20].strip() == "H":
                sec = "30"
            else:
                sec = "00"
            info3 = hour+":"+minute+":"+sec  # Scheduled Depature Time
                 
        info4 = info3 # Time
        info5 = (line[33:36].strip() or None)  # Platform
        info6 = (line[36:39].strip() or None)  # Line
        info7 = (line[39:42].strip() or None)  # Path
        info8 = (line[42:54].strip() or None)  # Activity
        info9 = (line[54:56].strip() or None)  # Engineering Allowance
        info10 = (line[56:58].strip() or None)  # Pathing Allowance
        info11 = (line[58:60].strip() or None)  # Performance Allowance

        timetable_info.append([train_id,info1,TIPLOC_lookup.get(info1,info1),info2, \
                               info3,info4,info5,info6,info7,info8,info9,info10,info11])
        return
    
    if header_record == "CR":
        change_no = train_info[train_id-1][36] + 1
        info1 = (line[2:9].strip() or None)   # Location
        info2 = (line[10:12].strip() or None)   # Train Category
        info3 = (line[12:16].strip() or None)   # Train Identity
        info4 = (line[16:20].strip() or None)   # Headcode
        info5 = (line[20:21].strip() or None)   # Course Indicator 
        info6 = (line[21:29].strip() or None)   # Train service code
        info7 = (line[29:30].strip() or None)   # Business Sector
        info8 = (line[30:33].strip() or None)   # Power Type
        info9 = (line[33:37].strip() or None)   # Timing Load
        info10 = (line[37:40].strip() or None)   # Speed
        info11 = (line[40:46].strip() or None)   # Operating Chars
        info12 = (line[46:47].strip() or None)   # Train Class
        info13 = (line[47:48].strip() or None)   # Sleepers
        info14 = (line[48:49].strip() or None)   # Reservations
        info15 = (line[49:50].strip() or None)   # Connect Indicator
        info16 = (line[50:54].strip() or None)   # Catering Code
        info17 = (line[54:58].strip() or None)   # Service Branding
        info18 = (line[58:62].strip() or None)   # Traction Class
        info19 = (line[62:67].strip() or None)   # UIC Code
        info20 = (line[67:75].strip() or None)   # Retailer Service ID
        change_info.append([train_id,info1,TIPLOC_lookup.get(info1,info1),info2,info3,info4, \
                            info5,info6,info7,info8,info9,info10,info11,info12,info13,info14, \
                            info15,info16,info17,info18,info19,info20])
        
        train_info[train_id-1][36] = change_no
        train_info[train_id-1] += [TIPLOC_lookup.get(info1,info1),info8]
        return
    
    if header_record == "LT":
        info1 = (line[2:9].strip() or None)  # TIPLOC Location
        train_info[train_id-1][38] = TIPLOC_lookup.get(info1,info1) # Destination

        hour = line[10:12].strip()
        minute = line[12:14].strip()
        if line[14:15].strip() == "H":
            sec = "30"
        else:
            sec = "00"

        info2 = hour+":"+minute+":"+sec  # Scheduled Arrival Time
        info3 = None  # Scheduled depature time
        info4 = info2 # Time
        info5 = (line[19:22].strip() or None) # Platform
        info6 = None # Line
        info7 = (line[22:25].strip() or None) # Path
        info8 = (line[25:37].strip() or None) # Activiey
        info9 = None # Engineering Allowance
        info10 = None # Pathing Allowance
        info11 = None # Peformance Allowance

        timetable_info.append([train_id,info1,TIPLOC_lookup.get(info1,info1),info2, \
                               info3,info4,info5,info6,info7,info8,info9,info10,info11])
        return
    
    if header_record == "ZZ":
        print("CIF file reading completed")
        return
    
    
    if header_record == "":
        return

# output data in excel
def readable_format(filename,option):
    #define essential variables
    header_record = ""   # Line ID
    train_id = 0   # Train ID

    # define essential list to be updated
    train_info = [] # train basic information
    timetable_info = []
    change_info = []

    TIPLOC_lookup = SharedMethods.get_tiploc_library()
    if TIPLOC_lookup == False:
        TIPLOC_lookup == {}

    # open text file to get the total line information (best way i can think of)
    # although it require reading the file twice
    print("Analysing CIF file....")
    with open(filename) as fp:
        total_line = sum(1 for line in enumerate(fp))

    print("Extracting information from CIF file....")
    print("")
    # open CIF file
    with open(filename) as fp:

        for index, line in enumerate(fp):
            # Get Header Info
            header_record = line[:2].strip()    # Get the Header Code
            if header_record == "BS":
                train_id = train_id + 1

            # excute action
            cif_data_action(line,header_record,train_info,timetable_info,change_info,TIPLOC_lookup,train_id)

            # print processing information
            SharedMethods.text_file_read_progress_bar(index, total_line)

    # Find the maximum length of the nested lists
    max_length = max(len(x) for x in train_info)

    columns = ['Train_ID','Type','UID','Date_Runs_from','Date_Runs_to', \
               'Mon','Tue','Wed','Thr','Fri','Sat','Sun','BH','Status', \
               'Category','Identity','Headcode','Course_Indicator','Service_Code', \
               'Business_Sector','Power_Type','Timing_Load','Speed','Operating_Code', \
               'Seating_Class','Sleepers','Resevations','Connection','Catering_Code', \
               'Service_Branding','Spare','STP_Indicator','UIC_Code','ATOC_Code', \
               'Applicable_Code','Retail_Service_ID','Info_Change','Origin','Destination']
    add = max_length - len(columns)
    for i in range(1, int(add/2)+1):
        columns.append(f'Location{i}')
        columns.append(f'Power_Type{i}')
    
    # Convert nested list to DataFrame
    df_sum = pd.DataFrame(train_info, columns=columns)

    columns = ['Train_ID','TIPLOC','Location', \
               'Category','Identity','Headcode','Course_Indicator','Service_Code', \
               'Business_Sector','Power_Type','Timing_Load','Speed','Operating_Code', \
               'Seating_Class','Sleepers','Resevations','Connection','Catering_Code', \
               'Service_Branding','Traction_Class','UIC_Code','Retail_Service_ID']
    
    df_change = pd.DataFrame(change_info, columns=columns)

    columns = ['Train_ID','TIPLOC','Location','Arrival Time','Depature/Passing Time', \
               'Time(A/D)','Platform','Line','Path','Activity','Engineering Allowance', \
               'Pathing Allowance','Performance Allowance'] 
    df_timetable = pd.DataFrame(timetable_info, columns=columns)

    # checking CIF information
    df_list = information_list(df_sum,df_timetable,TIPLOC_lookup)

    if option == "3":
        return df_timetable
    else:
        # Write DataFrame to Excel
        # write data to excel / overwrite the existing one

        print("Saving train summary information to csv...")
        csv_file = filename + '_CIF_Summary.csv'
        # Write DataFrame to CSV
        df_list.to_csv(csv_file, index=False)

        print("Saving train summary information to csv...")
        csv_file = filename + '_CIF_Detail.csv'
        # Prepending a tab character '\t' to ensure Excel treats it as text
        df_sum['Identity'] = df_sum['Identity'].apply(lambda x: f'\t{x}' if isinstance(x, str) and 'E' in x else x)
        # Write DataFrame to CSV
        df_sum.to_csv(csv_file, index=False)

        print("Saving train changeEnroute information to csv...")
        csv_file = filename + '_CIF_ChangeEnRoute.csv'
        df_change['Identity'] = df_change['Identity'].apply(lambda x: f'\t{x}' if isinstance(x, str) and 'E' in x else x)
        # Write DataFrame to CSV
        df_change.to_csv(csv_file, index=False)
        
        print("Saving train timetable information to csv...")
        csv_file = filename + '_CIF_Timetable.csv'
        # Write DataFrame to CSV
        df_timetable.to_csv(csv_file, index=False)

        return True

# generate unique list
def information_list(df_sum,df_timetable,TIPLOC_lookup):
    # get teh unique list
    tiploc_list = sorted(df_timetable['TIPLOC'].dropna().unique())
    # Create a dictionary to store the location information
    loc_list = []
    for tiploc in tiploc_list:
        loc_list.append(TIPLOC_lookup.get(tiploc, tiploc))
    toc_list = sorted(df_sum['ATOC_Code'].dropna().unique())
    dep_list = sorted(df_sum['Origin'].dropna().unique())
    des_list = sorted(df_sum['Destination'].dropna().unique())

    # Determine the length of the longest list
    max_length = max(len(tiploc_list), len(loc_list), len(toc_list), len(dep_list), len(des_list))

    # Assuming df is your DataFrame
    df_sum['Mon'] = df_sum['Mon'].astype(int)  # Convert the values in 'Mon' column to integers
    df_sum['Tue'] = df_sum['Tue'].astype(int)
    df_sum['Wed'] = df_sum['Wed'].astype(int)
    df_sum['Thr'] = df_sum['Thr'].astype(int)
    df_sum['Fri'] = df_sum['Fri'].astype(int)
    df_sum['Sat'] = df_sum['Sat'].astype(int)
    df_sum['Sun'] = df_sum['Sun'].astype(int)

    # Create a dictionary to store the lists
    data = {
        'TIPLOC_all': tiploc_list + [None] * (max_length - len(tiploc_list)),
        'Location_all': loc_list + [None] * (max_length - len(loc_list)),
        'ATOC_Code_all': toc_list + [None] * (max_length - len(toc_list)),
        'Origin_all': dep_list + [None] * (max_length - len(dep_list)),
        'Destination_all': des_list + [None] * (max_length - len(des_list)),
        'Monday_services': [df_sum['Mon'].sum()] + [None] * (max_length-1),
        'Tuesday_services': [df_sum['Tue'].sum()] + [None] * (max_length-1),
        'Wednesday_services': [df_sum['Wed'].sum()] + [None] * (max_length-1),
        'Thursday_services': [df_sum['Thr'].sum()] + [None] * (max_length-1),
        'Friday_services': [df_sum['Fri'].sum()] + [None] * (max_length-1),
        'Saturday_services': [df_sum['Sat'].sum()] + [None] * (max_length-1),
        'Sunday_services': [df_sum['Sun'].sum()] + [None] * (max_length-1)
    }

    # Create a new DataFrame from the dictionary
    new_df = pd.DataFrame(data)

    return new_df

    # excel_file = filename + '_CIF_Detail.xlsx'
    # with pd.ExcelWriter(excel_file, engine='openpyxl', mode='w') as writer:
    #     print("Saving train summary information to excel...(This takes time...)")
    #     df_sum = df_sum.astype(str)
    #     df_sum.to_excel(writer, sheet_name="Summary", index=False)
    #     print("Saving train change information to excel...")
    #     df_change = df_change.astype(str)
    #     df_change.to_excel(writer, sheet_name="ChangeInfo", index=False)

    #     print("Excel Saving.....(This takes time if your timetable is big)")

    # with pd.ExcelWriter(excel_file, engine='openpyxl', mode='w') as writer:
    #     print("Saving train timetable information to excel...")
    #     df_timetable = df_timetable.astype(str)
    #     df_timetable.to_excel(writer, sheet_name="Timetable", index=False)

    #     print("Excel Saving.....(This takes a while if your timetable is big)")

# append addtional (same length) information to the existing list (new list must be a even number)
def selection_list_append_same_lenth_info(file_select,selection_list,option):
    new_list = []

    if option == "7":
        i = 3 # append forth column: TIPLOC Removed
        old = "Platform"
        new = "TIPLOC"

    df = pd.read_csv(file_select, usecols=[i], dtype=str)
    append_list = df.iloc[:, 0].tolist()

    # Remove NaN values from the selection list
    append_list = [item for item in append_list if pd.notna(item)]

    old_count = len(selection_list)
    new_count = len(append_list)

    # matching the information
    if old_count < new_count: # append_list is longer
        for index, item in enumerate(append_list):
            if index < old_count:
                new_item = [selection_list[index],append_list[index]]
                new_list.append(new_item)
    else: # selection_list is longer
        for index, item in enumerate(selection_list):
            if index < new_count:
                new_item = [selection_list[index],append_list[index]]
                new_list.append(new_item)
            else:
                SharedMethods.print_message(f"WARNING: {old} {item} has no {new} assigned. Removal of this {old} will be ignored...","33")

    return new_list

# read CIF_select csv file
def selection_reading(file_select,option):
    if option == "3":
        i = 0 # first column:TIPLOC Selected
    elif option == "4":
        i = 1 # second column: TOC Selected
    elif option == "5":
        i = 2 # third column: Train Selected
    elif option == "6":
        i = 3 # forth column: TIPLOC Removed
    elif option == "7":
        i = 4 # fifth column: Platform removed
    else:
        return False

    df = pd.read_csv(file_select, usecols=[i], dtype={4: str}) # platform needs to be read as string due to UPG format
    selection_list = df.iloc[:, 0].tolist()

    # Remove NaN values from the selection list
    selection_list = [item for item in selection_list if pd.notna(item)]

    return selection_list

# find corrosponding train number with TIPLOC
def find_train_number(result,selection_list):
    df = result # timetable dataframe
    
    # Filter the DataFrame for rows where TIPLOC is in selection_list
    selected_df = df[df['TIPLOC'].isin(selection_list)]

    # Extract unique Train IDs from the filtered DataFrame
    unique_train_ids = selected_df['Train_ID'].unique().tolist()

    return unique_train_ids 

# remove diesel services   
def cif_remove_process(filename,option,select_list):
    
    # find the new file name
    name = os.path.basename(filename)
    name1 = name.split('.')
    # Only the first part of the file name (before the dot)
    newname = name1[0] if name1 else name

    if option == "2":
        filename_new = f'{newname}_Op2_NoDT.cif'
    elif option == "3":
        filename_new = f'{newname}_Op3_TIPLOC.cif'
    elif option == "4":
        filename_new = f'{newname}_Op4_TOC.cif'
    elif option == "5":
        filename_new = f'{newname}_Op5_Train.cif'
    elif option == "6":
        filename_new = f'{newname}_Op6_CrTT1.cif'
    elif option == "7":
        filename_new = f'{newname}_Op7_CrTT2.cif'
    else:
        filename_new = f'{newname}_No.cif'

    # open text file to get the total line information (best way i can think of)
    # although it require reading the file twice
    print("Analysing CIF file....")
    with open(filename) as fp:
        total_line = sum(1 for line in enumerate(fp))

    print("Selecting information from CIF file....")
    print("")
    # open CIF file
    train_id = 0
    flag = False
    flagCR = False
    lines_to_read = []
    with open(filename, 'r') as fp, open(filename_new, 'w') as fp2:

        for index, line in enumerate(fp):
            header_record = line[:2].strip()    # Get the Header Code
            
            if header_record == "HD": # write down first line
                fp2.write(line)

            if header_record == "AA": # write down Association record
                fp2.write(line)

            if header_record in ["BS","ZZ"]: # Process previous train, contain ZZ so process the last train
                flag = True
                if option == "2":
                    cif_remove_diesel(fp2,lines_to_read,flagCR) # process previous train
                elif option == "3":
                    cif_remove_train(fp2,lines_to_read,train_id,select_list) 
                elif option == "4":
                    cif_remove_toc(fp2,lines_to_read,select_list)
                elif option == "5":
                    cif_remove_train(fp2,lines_to_read,train_id,select_list)
                elif option == "6":
                    cif_remove_location(fp2,lines_to_read,train_id,select_list)
                elif option == "7":
                    cif_remove_platform_info(fp2,lines_to_read,select_list)
                               
                flagCR = False # refresh the flag for new train

                lines_to_read = []
                train_id = train_id + 1
            
            if header_record == "CR": # if there is information change en route.
                flagCR = True
            
            if flag == True:
                lines_to_read.append(line)

            # print processing information
            SharedMethods.text_file_read_progress_bar(index, total_line)
        
        # cif finish marker
        line = "ZZ" + " " * 78 + "\n"
        fp2.write(line)
    return True

# each train jounery decision - Remove of Diesel services: Split Train when there is a mode change enroute
def cif_remove_diesel(fp2,lines_to_read,flagCR):

    if len(lines_to_read) <= 2:
        return
    
    # check initial power type
    power = lines_to_read[0][50:53].strip()   # Power Type 
    if power in ["D","DEM","DMU","ED"]: # refresh the flag for new train
        flagselect = False
    else:
        flagselect = True
    
    if flagCR == False: # if there is no change en route
        if flagselect == False: # if it starts with Diesel
            return
        else: # if it starts with electric
            for line in lines_to_read:
                fp2.write(line)
    
    else: # if there is a change en route
        new_lines = []
        mode = False # mode now, False if Diesel
        mode_change = False # power mode change at CR record
        preCR = False # if the previous line is CR record
        header = lines_to_read[0][:30] # first 30 charater: properties of trains
        add = None # addtional BX information
        crline = None # CR Line Info

        for line in lines_to_read:
            header_record = line[:2].strip()
            
            if header_record == "BS":
                if flagselect == True: # if it starts with electric
                    mode = True
                    new_lines.append(line)
                continue

            if header_record == "BX":
                add = line
                if mode == True:
                    new_lines.append(line)
                continue

            if header_record == "LO":
                if mode == True:
                    new_lines.append(line)
                continue

            if header_record == "LI":
                if preCR == False: # if the reprevious line is not CR
                    if mode == True: # if is is still electric
                        new_lines.append(line)
                else:
                    if mode == True: # if it is electric
                        if mode_change == True: # and also if it changes from d to e
                            # start a new train
                            templine = header + crline + '\n'
                            new_lines.append(templine)
                            if add is not None:
                                new_lines.append(add)
                            if line[15:20].strip() == "": # no departure time then use passing time
                                templine = "LO" + line[2:10] + line[20:25] + line[20:25] + "         TB                                                 \n"
                            else:
                                templine = "LO" + line[2:20] + "         TB                                                 \n"
                            new_lines.append(templine)
                            # reset flag
                            mode_change = False
                            preCR= False
                        else: # if the change is from e to e
                            new_lines.append(line)
                            mode_change = False
                            preCR= False
                            
                    else: # if it is disel now 
                        if mode_change == True: # and also if it changes from e to d
                            # finish the line
                            if line[15:20].strip() == "": # no departure time then use passing time
                                templine = "LT" + line[2:10] + line[20:25] + line[20:25] + "     TF                                                     \n"
                            else:
                                templine = "LT" + line[2:20] + "     TF                                                     \n"
                            new_lines.append(templine)
                            # reset flag
                            mode_change = False
                            preCR= False
                        else: # change is from d to d
                            mode_change = False
                            preCR= False

                continue

            if header_record == "CR":
                preCR = True
                power = line[30:33].strip()
                if power in ["D","DEM","DMU","ED"]:
                    if mode == True: # if the previous is e and now d
                        mode_change = True
                        crline = line[10:60]
                    mode = False
                else:
                    if mode == False: # if the previous is d and now e
                        mode_change = True
                        crline = line[10:60]
                    mode = True
                continue

            if header_record == "LT":
                if mode == True:
                    new_lines.append(line)
                continue
        
        # write to file
        for line in new_lines:
            fp2.write(line)                
    return

# remove specific toc
def cif_remove_toc(fp2,lines_to_read,select_list):

    if len(lines_to_read) <= 2:
        return
    
    if lines_to_read[1][:2].strip() != "BX":
        return
    
    # check TOC number
    toc = lines_to_read[1][11:13].strip()   # ATOC Code
    if toc in select_list or toc == "": # toc in the select
        flagselect = True
    else:
        flagselect = False
    
    if flagselect == False:
        return
    else:
        for line in lines_to_read:
            fp2.write(line)

    return

# remove specific train
def cif_remove_train(fp2,lines_to_read,train_id,select_list):

    if len(lines_to_read) <= 2:
        return

    if train_id in select_list: # train in the select
        flagselect = True
    else:
        flagselect = False
    
    if flagselect == False:
        return
    else:
        for line in lines_to_read:
            fp2.write(line)
    return

# remove specific TIPLOC for LI header
def cif_remove_location(fp2,lines_to_read,train_id,select_list):

    if len(lines_to_read) <= 2:
        return

    for line in lines_to_read:
        location = line[2:9].strip()
        if line[:2].strip() == "LI":
            if location in select_list:
                if line[10:20].strip():
                    SharedMethods.print_message(f"\nWARNING: Train {train_id} at {location} has time info, ignore removing...","33")
                    fp2.write(line)
            else:
                fp2.write(line)
        else:
            fp2.write(line)

    return

# remove specific platform infomation ([platform,TIPLOC])
def cif_remove_platform_info(fp2,lines_to_read,select_list):

    if len(lines_to_read) <= 2:
        return
    
    for line in lines_to_read:
        tiploc = line[2:9].strip()
        
        if line[:2].strip() in ["LO","LT"]:
            platform = line[19:22].strip()
            combine = [platform,tiploc]
            if combine in select_list:
                new_line = line[:19] + "   " + line[22:] # replace platform informaiton with empty space
                print(f"\nPlatform removed at: '{line}'")
                fp2.write(new_line)
            else:
                fp2.write(line)
        
        elif line[:2].strip() == "LI":
            platform = line[33:36].strip()
            combine = [platform,tiploc]
            if combine in select_list:
                new_line = line[:33] + "   " + line[36:] # replace platform informaiton with empty space
                print(f"\nPlatform removed at: '{line}'")
                fp2.write(new_line)
            else:
                fp2.write(line)
        
        else:
            fp2.write(line)

    return

# programme running
if __name__ == "__main__":
    # Add your debugging code here
    simname = "StraightLine1"  # Provide a simulation name or adjust as needed
    main_option = "1"  # Adjust as needed
    time_start = "0070000"  # Adjust as needed
    time_end = "0080000"  # Adjust as needed
    option_select = "2"  # Adjust as needed
    text_input = "May25Test.cif"  # Adjust as needed
    low_v = None  # Adjust as needed
    high_v = None  # Adjust as needed
    time_step = None  # Adjust as needed

    # Call your main function with the provided parameters
    main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step)

