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
SimulationName.lst.txt: list file auto generated when run button is clicked. This obviously requires that the error via check layout is eliminated before doing this model check.
Used Input:
simname: to locate the text file for checking
option_select: See description.
Expected Output:
Several .csv file and .txt file saved in the root folder.
Description:
This script defines 3 options in the main() function to generate some summary output from a simulation model.
In lst_data_read(), the ***.lst.txt file was read line by line and depending on the section header, it saves related information in various list.
In summary_check_option(), the branches are cross checked against VISION model to generate a detailed summary. It output various .csv files contains various summary information.
In connection_info_built(), the node and branch network is automatically created by the third party package Network X. This could generate various output information for connectivity. Two summary network connection summaries are created.
In plot_connection(), again NetworkX is used to create auto generated node map. Note that the generation is fully automatic, and position is random allocated each time. So the generated output is different for each run.
Other functions logic is relatively straightforward


"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
# V1.1 (Jieming Ye 07/2024) - Handle Neutral Section Scenario properly
# V2.0 (Jieming Ye 01/2025) - Change the way to generate AC model connection plot
#=================================================================
# Set Information Variable
# N/A
#=================================================================

import sys
import os
import csv
import math
import copy

import networkx as nx
import matplotlib.pyplot as plt

from vision_oslo_extension.shared_contents import SharedMethods

def main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):

    #User Interface - Welcome message:
    print("")
    print("OSLO Model Check - - - > ")
    print("")

    print("This programme was developed to check a working model and generate a connection report")
    print("Software error message should be cleared before using this programme")
    print("Please contact support if unexpected exit happens")
    print("")    

    #define the file name and check if the file exist or not
    # get simulation name name from input
    print(f"The simulation name is {simname}.")
    # simname = input()
    filename = simname + ".lst.txt"

    if not SharedMethods.check_existing_file(filename): # if the lst.txt file exist
        SharedMethods.print_message(f"ERROR: Your can generate the lst file by VISION - NIE - Run Dataprep.","31")
        return False

    if not main_menu(simname, filename, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):
        return False

    return True

# main function to be called
def main_menu(simname, filename, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):
    # user input selection
    # print("\nPlease select from the list what you want to do:(awaiting input)")
    # print("1: Model verficiation report.")
    # print("2: Connection Report")
    # print("3: Connection Plot")

    # text_input is deemed to be the sub-option under this function.

    option = option_select

    if option not in ["0","1","2","3","sp"]:
        SharedMethods.print_message("ERROR: Contact Support. Error in model_check.py --> main_menu","31")
        return False
    
    if option == "3" and text_input == "0":
        SharedMethods.print_message("ERROR: Please select an option to proceed.","31")
        return False
    
    #define essential variables

    result = lst_data_read(filename)
    if result == False:
        return False
    else:
        branch_list,branch_line_list,sp_list,trans_list,branch_list_t,errorwarning_list = result

    if option == "1":
        if not summary_check_option(simname,branch_list,branch_line_list,branch_list_t,sp_list,trans_list,errorwarning_list):
            return False

    if option == "2":
        sp_connect = connection_info_built(simname,branch_line_list,sp_list,option_select,branch_list,branch_list_t)

    if option == "3":
        if text_input == "3": # DC random plot
            plot_connection_random(simname,branch_list,branch_line_list,branch_list_t,sp_list,trans_list,errorwarning_list)
        else:
            if not plot_connection(simname,text_input,branch_list,branch_line_list,branch_list_t,sp_list,trans_list,errorwarning_list):
                return False
        
    if option == "sp": #special for average power load
        sp_connect = connection_info_built(simname,branch_line_list,sp_list,option_select,branch_list,branch_list_t)
        return sp_connect
    
    return True


#================Required for all: Reading Informaiton==================================
# processing the list data:
def lst_data_read(filename):
    #define essential variables
    section_flag = ""   # Identify the section
    section_id = 0  # section Id by default

    branch_list = [] # branch basic info
    branch_line_list = []   # branch info with route section id
    trans_list = [] # transformer basic info added v1.2
    branch_list_t = [] # branch list with transformers added as branches added v1.2
    sp_list = []    # list to store supply point information
    errorwarning_list = [] # list to save error warning message

    # open text file to get the total line information (best way i can think of)
    # although it require reading the file twice
    print("Analysing LST file....")
    with open(filename) as fp:
        total_line = sum(1 for line in enumerate(fp))

    print("Extracting information from LST file....")
    print("")
    # open lst file
    with open(filename) as fp:

        for index, line in enumerate(fp):
            if line[:4].strip() == "***":
                errorwarning_list.append(line)
                continue
            if line[:4]== "    ":
                continue

            # Get Header Info
            section_flag = line[:6].strip()    # Get the line header (assume 6 digits should be enough)
            if section_flag == "*ELECT":
                section_id = 1
                continue
            elif section_flag == "*BRANC":
                section_id = 2
                continue
            elif section_flag == "*SUPPL":
                section_id = 3
                continue
            elif section_flag == "*METER":
                section_id = 6
                continue 
            elif section_flag == "*TRANS":
                section_id = 5
                continue
            elif section_flag == "*LINES":
                section_id = 4
                continue
            elif section_flag == "*END O":
                section_id = 0

            # excute action
            lst_data_action(line,section_id,branch_list,branch_line_list,sp_list,trans_list)

            SharedMethods.text_file_read_progress_bar(index, total_line)
    
    print("100 % completed.")
    print("LST Processing Completed. Data Processing...")
    # combine transfomrer list and branch list into a new list
    branch_list_t = copy.deepcopy(branch_list)
    for lists in trans_list:
        branch_list_t.append([len(branch_list_t)+1,lists[1],lists[3],lists[5],lists[2],"0","1",lists[7],lists[8],"0","Transformer"])

    return branch_list,branch_line_list,sp_list,trans_list,branch_list_t,errorwarning_list

# Action on the list based on the Header selection
def lst_data_action(line,section_id,branch_list,branch_line_list,sp_list,trans_list):
    if section_id == 0: # no information process required
        return

    if section_id == 1: # Electrical traction data section
        return
    
    if section_id == 2: #  branch list
        
        info1 = line[:5].strip()  # Branch Name
        info2 = line[5:10].strip()  # Branch Start Node ID
        info3 = line[10:15].strip()  # Branch End Node ID
        info3a = line[15:16].strip() # Branch Type (added in new version)
        info4 = line[17:25].strip()  # Branch Start Distance (always 0)
        info5 = line[25:33].strip()  # Branch End Distance / Branch Length
        info6 = line[33:41].strip()  # Branch Resistance
        info7 = line[41:49].strip()  # Branch Reactance
        info8 = line[49:57].strip()  # Branch Susceptance
        info9 = line[57:80].strip()  # Comment
        
        branch_list.append([len(branch_list)+1,info1,info2,info3,info3a,info4,info5,info6,info7,info8,info9])      #create branch list
        
        return
    
    if section_id == 3: #  Supply Points List
        
        info1 = line[:5].strip()  # Suppy Point Name
        info2 = line[5:10].strip()  # OSLO node energised
        info3 = line[10:20].strip()  # No Load Voltage
        info4 = line[20:30].strip()  # Phase angle in degree
        info5 = line[30:40].strip()  # Output resistance
        info6 = line[40:52].strip()  # Output reactance
        info7 = line[52:90].strip()  # Comment        

        sp_list.append([len(sp_list)+1,info1,info2,info3,info4,info5,info6,info7])

        return
    
    if section_id == 4: #  Lines/branches cross reference table
        
        info1 = line[:10].strip()  # Route Section ID
        info2 = line[10:25].strip()  # Route section start location
        info3 = line[25:40].strip()  # Route Section end location
        info4 = line[40:50].strip()  # Branch included
        info5 = line[50:65].strip()  # Branch_Start_Location(Relative_to_Line_Origin)
        info6 = line[65:80].strip()  # Branch / lines same direction

        if info6 == "0":
            info6 = "Stub_Fed"
        elif info6 == "+1":
            info6 = "Branch/Line_Same_Direction"
        elif info6 == "-1":
            info6 = "Branch/Line_Oppo_Direction"

        for lists in branch_list:
            if lists[1] == info4:
                branch_line_list.append([lists[0],lists[1],lists[2],lists[3],lists[4],lists[5],lists[6],\
                    lists[7],lists[8],lists[9],lists[10],info1,info2,info3,info5,abs(int(info3)-int(info2)),info6])

        return

    #added transformer reading ability v1.2
    
    if section_id == 5: #  Transformer list
        
        info1 = line[:5].strip()  # Transformer Name
        info2 = line[5:6].strip() # Type of Transformer
        #print("T info",info2)

        if info2 == "A" or info2 =="N": #Determine if this is the first line (transformer information are listed in 2 lines)
            #print("first",info1)       #For development 
            info3 = line[7:12].strip()  #Primary Winding Node
            info4 = line[12:21].strip() #Primary Winding Voltage 
            info5 = line[21:26].strip() #Secondary Winding Node
            info6 = line[26:36].strip() #Secondary Winding Voltage

            trans_list.append([len(trans_list)+1,info1,info2,info3,info4,info5,info6]) # write to trans_list
                        
            # trans_list_a.append([len(trans_list_a)+1,info1,info2,info3,info4,info5,info6]) # write to trans_list_a

        else:                           #This will be in the second line
            #print("second",info1)      #For development
            info8 = line[8:15].strip()  #Transformer Resistance
            info9 = line[15:25].strip() #Transformer Reactance
            trans_list[len(trans_list)-1] = trans_list[len(trans_list)-1] + [info8, info9]

        return

    if section_id == 6: # Metering points section
        return        
    
    if section_id == "ZZ":
        print("CIF file reading completed")
        return
    
    if section_id == "":
        return

# module to check branch information
def check_branch_info(branch_line_list,branch_list_t):
    for lists in branch_list_t:
        if lists[4] == "F":
            branch_line_list.append([lists[0],lists[1],lists[2],lists[3],lists[4],lists[5],lists[6],\
                        lists[7],lists[8],lists[9],lists[10],"","","","","","Cables/ATF"])
        if lists[4] == "N":
            branch_line_list.append([lists[0],lists[1],lists[2],lists[3],lists[4],lists[5],lists[6],\
                        lists[7],lists[8],lists[9],lists[10],"","","","","","GridTranx"])
        if lists[4] == "A":
            branch_line_list.append([lists[0],lists[1],lists[2],lists[3],lists[4],lists[5],lists[6],\
                        lists[7],lists[8],lists[9],lists[10],"","","","","","AutoTranx"])
     
    return branch_line_list

#==========================OPTION 1: OSLO Information Listing=========================
# option 1 to check the summary
def summary_check_option(simname,branch_list,branch_line_list,branch_list_t,sp_list,trans_list,errorwarning_list):

    # branch checking process
    print("\nBranch Summary Cross Checking...")
    branch_line_list = check_branch_info(branch_line_list,branch_list_t)

    node_connected_branch = []
    # added in v2.0 to give node connection summary 
    print("\nNode Branch Connection Check...")
    for branch in branch_list_t:
        line = [branch[2],branch[1],'S']
        node_connected_branch.append(line)
        line = [branch[3],branch[1],'E']
        node_connected_branch.append(line)

    # sort the data
    sorted_branch_line = sorted(branch_line_list, key=lambda row:row[0], reverse =False)
    sorted_node_connected_branch = sorted(node_connected_branch, key=lambda row: (row[0], row[2]), reverse=False)
    sorted_branch = sorted(branch_list_t, key=lambda row:row[0], reverse =False) #test branch_list_t
    sorted_sp = sorted(sp_list, key=lambda row:row[0], reverse =False)
    sorted_trans = sorted(trans_list, key=lambda row:row[0], reverse =False)

    #======================================
    with open(simname + '_branch_detail.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile) # create the csv writer
        lock = 0
        row = 1
        writer.writerow(["BranchID","Branch_Name","Start_Node","End_Node","Type","Start_Node_Dis", \
                        "End_Node_Dis","Branch_Resistance","Branch_Reactance","Branch_Susceptance","Comment", \
                        "VISION_Line_Section_ID","VISION_LS_Start_Dis","VISION_LS_End_Dis", \
                        "Branch_Start_Location(Relative_to_Line_Origin)","VISION_Line_Length","Direction"])
        row = row + 1
        writer.writerows(sorted_branch_line)

    #============================================
    with open(simname + '_node_connected_branch.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile) # create the csv writer
        lock = 0
        row = 1
        writer.writerow(["Node ID","Connected Branch ID","Branch Start/End"])
        row = row + 1
        writer.writerows(sorted_node_connected_branch)

    #============================================
    with open(simname + '_branch.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile) # create the csv writer
        lock = 0
        row = 1
        writer.writerow(["BranchID","Branch_Name","Start_Node","End_Node","Type","Start_Node_Dis", \
                        "End_Node_Dis","Branch_Resistance","Branch_Reactance","Branch_Susceptance","Comment"])
        row = row + 1
        writer.writerows(sorted_branch)
    
    #================================================
    with open(simname + '_supply_point.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile) # create the csv writer
        lock = 0
        row = 1
        writer.writerow(["No","SP_Name","SP_Node_ID","No-load_Volt(kV)","Phase_Angle(deg)", \
                        "Output_Resistance","Output_Reactance","Comment"])
        row = row + 1
        writer.writerows(sorted_sp)
            
    #==================================================
    with open(simname + '_transformer.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile) # create the csv writer
        lock = 0
        row = 1
        writer.writerow(["No","Trans_Name","Type","In_Node","In_Voltage","Out_Node","Out_Voltage", \
                        "Output_Resistance","Output_Reactance"])
        row = row + 1
        writer.writerows(sorted_trans)

    #====================================================
    with open(simname + '_error_warning.txt', 'w') as fw:
        fw.write("Error and Warning Summary\n")

        for items in errorwarning_list:
            fw.write(f"{items}\n") # print out
    
    return True
     
#==========================OPTION 2: Connection Summary=========================
# option 2 to genearte various connection map
def connection_info_built(simname,branch_line_list,sp_list,option_select,branch_list,branch_list_t):
    connection_sum = []  # list to process node connection information
    sp_connection_sum = [] # saving node
    sp_connection_sum_branch = [] # saving branch

    # Use NetworkX library
    # Create an empty graph including trans sp evertying
    G = nx.MultiGraph()
    # Add edges without adding nodes explicitly
    for item in branch_list_t:
        # add at 07/2024 so that neutral section is not deemed as a connection
        if item[7] == 'NEUTRAL':
            if item[2] == item [3]:
                print(f"Neutral Section {item[1]} is bypassed.")
                G.add_edge(item[2], item[3], label = item[1])
        else:
            G.add_edge(item[2], item[3], label = item[1])

    print("\nConnection Summary...")
    # Get connected components of the graph
    connected_components = list(nx.connected_components(G))
    for index, connection in enumerate(connected_components):
        connection_sum.append([index+1]+list(connection))

    # Supply Points Node connection added in V1.2
    print("\nSupply Points Connection Summary...")
    for index, item in enumerate(sp_list):
        # SP connected nodes
        sp_line = set()
        # SP connected branch
        connected_branch = set()

        sp = item[1]
        node = item[2]
        for component in connected_components:
            if node in component:
                sp_line.update(component)
                # check all edges in edges
                for edge in G.edges:
                    if edge[0] in component or edge[1] in component:
                        edge_data = G.get_edge_data(*edge)
                        connected_branch.add(edge_data['label'])
                               
        if sp_line:
            sp_line = list(sp_line)
            sp_line = sorted(sp_line,reverse =False)
            sp_line.remove(node)
            sp_line.insert(0, node)
        else: # if it is an empty set which means connect to nothing
            sp_line = [sp,"NOT CONNECTED"]
        
        sp_connection_sum.append([index+1,sp]+sp_line)

        
        if connected_branch:
            connected_branch = list(connected_branch)
            connected_branch = sorted(connected_branch,reverse =False)
            connected_branch.insert(0,node)
        else:
            connected_branch = [sp, "NOT CONNECTED"]
        
        sp_connection_sum_branch.append([index+1,sp]+connected_branch)

    
    # sort the data (sort based on first element of each row)
    sorted_sp_c = sorted(sp_connection_sum, key=lambda row:row[0], reverse =False)
    sorted_connection_sum = sorted(connection_sum, key=lambda row:row[0], reverse =False)
    sorted_sp_branch_sum = sorted(sp_connection_sum_branch, key=lambda row:row[0], reverse =False)

    if option_select == "2":
        with open(simname + '_node_connection_summary.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile) # create the csv writer
            lock = 0
            row = 1
            writer.writerow(["No","Node_ID"])
            row = row + 1
            writer.writerows(sorted_connection_sum)
        
        
        with open(simname + '_supply_point_connected_nodes.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile) # create the csv writer
            lock = 0
            row = 1
            writer.writerow(["No","SP_Name","SP_Node_ID","Connected_Node_ID"])
            row = row + 1
            writer.writerows(sorted_sp_c)
        
        with open(simname + '_supply_point_connected_branches.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile) # create the csv writer
            lock = 0
            row = 1
            writer.writerow(["No","SP_Name","SP_Node_ID","Connected_Branch_ID"])
            row = row + 1
            writer.writerows(sorted_sp_branch_sum)
    
    return sorted_sp_c

#===========================Option 3: Plotting =======================================
def plot_connection(simname,option,branch_list,branch_line_list,branch_list_t,sp_list,trans_list,errorwarning_list):

    # Create a directed graph
    G = nx.MultiDiGraph()
    G_full = nx.MultiDiGraph()
    
    print("Analysing the OSLO Information...")
    for item in branch_list_t:
        # Check for the neutral section condition
        # if not (item[7] == 'NEUTRAL' and item[2] != item[3]):
        # JY: the neutral section can be listed easily via the bulk grid editing feature. not required to be shown in the plot anymore from RN29
        if not (item[7] == 'NEUTRAL'):
            G.add_node(item[2])
            G.add_node(item[3])
            # G_full is reserve for future use. All branches as saved seperatedly
            G_full.add_node(item[2])
            G_full.add_node(item[3])
            G_full.add_edge(item[2], item[3], branch_name = item[1], branch_type = item[4])
            # Check if the edge already exists; if it does, modify the branch name, else add the edge
            if G.has_edge(item[2], item[3]):
                G.edges[item[2], item[3], 0]['branch_name'] += f"/{item[1]}"
            else:
                G.add_edge(item[2], item[3], branch_name=item[1], branch_type=item[4])


    # supply point nodes:
    sp_node = [item[2] for item in sp_list]

    print("Analysing the connection logic...")
    # function of finding the connection logic level
    def find_connection_logic_level(G,checked_nodes,sp,lines_max_sum):
        max_grid = 1
        level = 0
        sp_connection_logic = []
        sp_connection_logic.append([sp])
        checked_nodes.append(sp)
        while True:
            # empty list to store new nodes
            new_nodes = []
            for node in sp_connection_logic[level]:
                # Search all edges connected to the node
                for edge in G.out_edges(node, data=True):
                    if edge[1] not in checked_nodes:
                        # add to new nodes list
                        new_nodes.append(edge[1])
                        checked_nodes.append(edge[1])
                for edge in G.in_edges(node, data=True):
                    if edge[0] not in checked_nodes:
                        # add to new nodes list
                        new_nodes.append(edge[0])
                        checked_nodes.append(edge[0])
            # if no new nodes found, break
            if new_nodes == []:
                break
            # search next level
            else:
                sp_connection_logic.append(new_nodes)
                level = level + 1

                if len(new_nodes) > max_grid:
                    max_grid = len(new_nodes)
        
        # store the max grid number
        lines_max_sum.append(max_grid)

        return lines_max_sum,checked_nodes,sp_connection_logic


    # find connection logic level
    checked_nodes = []
    lines_max_sum = []
    connection_logic = []

    for sp in sp_node:
        # find number of connected nodes
        lines_max_sum,checked_nodes,sp_connection_logic = find_connection_logic_level(G,checked_nodes,sp,lines_max_sum)
        connection_logic.append(sp_connection_logic)
        
    # for nodes that are not connected
    for node in G.nodes():
        if node not in checked_nodes:
            lines_max_sum,checked_nodes,sp_connection_logic = find_connection_logic_level(G,checked_nodes,node,lines_max_sum)
            connection_logic.append(sp_connection_logic)
                
    # assign the grid position based on connection logic
    pos = {}
    grid_spacing = 10
    x, y = 0, 0

    for index, group in enumerate(connection_logic):
       
        for level, nodes in enumerate(group):
            for number, node in enumerate(nodes):
                
                pos[node] = (x, y)
                y = y + grid_spacing

            x = x + grid_spacing
            y = y - (number+1) * grid_spacing

        y = y + lines_max_sum[index] * grid_spacing
        x = x - (level+1) * grid_spacing
            
    # Draw the graph
    print("Matlibplot Plotting...")
    # plt.figure(figsize=(16.5, 11.7))  # A3 size
    # Compute layout bounds
    x_values = [coord[0] for coord in pos.values()]
    y_values = [coord[1] for coord in pos.values()]

    x_range = max(x_values) - min(x_values) + grid_spacing
    y_range = max(y_values) - min(y_values) + grid_spacing

    # Define base size per grid cell (adjustable)
    cell_size = 0.1  # inches per grid unit (adjust as needed)
    fig_width = x_range * cell_size
    fig_height = y_range * cell_size / 2.5 # Adjust height for better ratio

    # Apply some minimum and maximum size limits if needed (A3 - A0*2 size)
    fig_width = max(16.5, min(fig_width, 46.8*2))
    fig_height = max(11.7, min(fig_height, 46.8*2))

    # Create figure with dynamic size
    plt.figure(figsize=(fig_width, fig_height))

    # Highlight supply point nodes in red
    node_colors = ['red' if node in sp_node else 'lightblue' for node in G.nodes()]
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=25,
        node_color=node_colors,
        font_size=10,
        font_color='black',
        edge_color='grey',  # Grey edges
        connectionstyle="arc3,rad=0.1",  # Adjust for multiple edges
    )

    # Add edge type labels
    edge_labels = {
        (u, v, k): f"{data['branch_type']}" for u, v, k, data in G.edges(keys=True, data=True)
    }

    # draw labels
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        label_pos=0.2,
        font_size=6,
        font_color='red',
        bbox=dict(facecolor='none', edgecolor='none'), # no background and no border
        connectionstyle="arc3,rad=0.1",  # Adjust for multiple edges
    )

    # add edge name labels if option is 2
    if option == "2":
        edge_labels = {
            (u, v, k): f"{data['branch_name']}" for u, v, k, data in G.edges(keys=True, data=True)
        }

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            label_pos=0.5,
            font_size=6,
            font_color='green',
            bbox=dict(facecolor='none', edgecolor='none'), # no background and no border
            connectionstyle="arc3,rad=0.1",  # Adjust for multiple edges
        )

    # Save the plot as a picture format (e.g., PNG)
    print("Saving the plot...")
    index = "1"
    filename = simname + "_Auto_Plot_" + index + ".png"
    while os.path.isfile(filename):
        index = str(int(index) + 1)
        filename = simname + "_Auto_Plot_" + index + ".png"
    
    plt.savefig(filename, format="png", dpi=300)  # dpi sets the resolution (dots per inch)

    return True


# option 3 to plot things: now reserved for DC random plot to be refined in future
def plot_connection_random(simname,branch_list,branch_line_list,branch_list_t,sp_list,trans_list,errorwarning_list):
    
    print("Plotting and Saving....")
    # Create an empty graph
    G = nx.Graph()

    # Add edges without adding nodes explicitly
    for item in branch_list_t:
        # add at 07/2024 so that neutral section is not deemed as a connection
        if item[7] == 'NEUTRAL':
            if item[2] == item [3]:
                G.add_edge(item[2], item[3])
        else:
            G.add_edge(item[2], item[3])

    # supply point nodes:
    sp_node = []
    for item in sp_list:
        sp_node.append(item[2])

    # Get connected components of the graph
    connected_components = list(nx.connected_components(G))
    
    # Define a node color list where nodes in nodes_to_draw_in_red are red and others are default color
    node_colors = ['red' if node in sp_node else 'skyblue' for node in G.nodes()]
    
    # Set the figure size to A3 dimensions (11.69 x 16.53 inches)
    plt.figure(figsize=(16.53,11.69))

    # Draw the graph
    nx.draw(G, node_size=25,node_color=node_colors, with_labels=True,font_size = 6, edge_color='gray')

    # Save the plot as a picture format (e.g., PNG)
    index = "1"
    filename = simname + "_Auto_Plot_" + index + ".png"
    while os.path.isfile(filename):
        index = str(int(index) + 1)
        filename = simname + "_Auto_Plot_" + index + ".png"
    
    plt.savefig(filename, format="png", dpi=300)  # dpi sets the resolution (dots per inch)

    # plt.show()

    return

# programme running
if __name__ == "__main__":
    # Add your debugging code here
    simname = "test_model_AC"  # Provide a simulation name or adjust as needed
    main_option = "2"  # Adjust as needed
    time_start = "0070000"  # Adjust as needed
    time_end = "0080000"  # Adjust as needed
    option_select = "3"  # Adjust as needed
    text_input = "2"  # Adjust as needed
    low_v = None  # Adjust as needed
    high_v = None  # Adjust as needed
    time_step = None  # Adjust as needed

    # Call your main function with the provided parameters
    main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step)

