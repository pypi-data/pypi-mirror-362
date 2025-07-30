#
# -*- coding: utf-8  -*-
#=================================================================
# Created by: Jieming Ye
# Created on: Nov 2022
# Last Modified: 07/02/2023
#=================================================================
# Copyright (c) 2024 [Jieming Ye]
#
# This Python source code is licensed under the 
# Open Source Non-Commercial License (OSNCL) v1.0
# See LICENSE for details.
#=================================================================
"""
Pre-requisite: 
BHTPBANK file.
Used Input:
text_input: to locate the BHTPBANK file.
time_step: to record the car number information entered by the user.
Expected Output:
Detailed calculation csv file, error list and variable plots.
Description:
This script defines the bhtpbank file checking process and output various plots for the traction profile.
It reads formatted data to various nested list as TE, BE, I, etc and check if there is any value outside the normal value range.
It is relatively straightforward to read following main() function flow. Subfunctions are defined to perform specific tasks.


"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version - migrated from previous v1.4
#=================================================================
# Set Information Variable
# N/A
#=================================================================

# Default
import os
import math
import csv

# Third Party
import matplotlib.pyplot as plt
from vision_oslo_extension.shared_contents import SharedMethods

def main(sim_name, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):
    # text input = bhtpbank name
    # time_step  = car number

    #User Interface - Welcome message:
    print("")
    print("BHTPBANK Checking Process - - - > ")
    print("")

    # system printing control enable ANSI code
    os.system("")    

    bhtpname = text_input

    # option 3 -- "1": do not interative plot
    # option 4 -- "2": keep interactive plot
    if option_select == "0":
        SharedMethods.print_message("ERROR: Please select an option to proceed.","31")
        return False
    
    if option_select not in ["1","2"]:
        SharedMethods.print_message("ERROR: Error in bhtpbank_check.py. Please contact Support.","31")
        return False

    if not os.path.isfile(bhtpname): # if the bhtpbank file exist
       SharedMethods.print_message(f"ERROR: BHTPBANK file {bhtpname} does not exist. Exiting...","31")
       return False

    #define the car number of the bhtpbank
    print(f"Please enter the NUMBER OF CARS of {bhtpname}:(RANGE:1-20)(awaiting input)")
    carnumber = int(time_step)

    if (carnumber <= 0) or (carnumber > 20):
        SharedMethods.print_message("ERROR: Invalid Car Number. Please Re-enter a number between 1-20. Exiting...","31")
        return False

    print("\nChecking Process Initiated...")

    # Create Essential Data Set
    # Level 0: voltage entry [V1,V2,V3,...]
    # Level 1: data entry e.g. [d1,d2,d3...] under V1
    # Level 2: percetage entry e.g [0, 100] under d1
    vol_list = [] # data list saving voltage list

    #date format: list = [[d1,d2,d3..],[d1,d2,d3...],[...],...]
    speed_list = [] # nested speed for voltage
    TE_list = [] # nested tractive effort for voltage
    Re_I_list = [] # nested real current for voltage
    Im_I_list = [] # nested imag current for voltage
    
    TE_list_p1 = [] # nested list for first percentage
    Re_I_list_p1 = [] # nested real current for first percentage
    Im_I_list_p1 = [] # nested imag current for first percentage
    TE_list_p2 = [] # nested list for 2nd percentage
    Re_I_list_p2 = [] # nested real current for 2nd percentage
    Im_I_list_p2 = [] # nested imag current for 2nd percentage

    # define for braking part
    vol_list_b = [] # data list saving voltage list

    #date format: list = [[d1,d2,d3..],[d1,d2,d3...],[...],...]
    speed_list_b = [] # nested speed for voltage
    TE_list_b = [] # nested tractive effort for voltage
    Re_I_list_b = [] # nested real current for voltage
    Im_I_list_b = [] # nested imag current for voltage
    
    TE_list_p1_b = [] # nested list for first percentage
    Re_I_list_p1_b = [] # nested real current for first percentage
    Im_I_list_p1_b = [] # nested imag current for first percentage
    TE_list_p2_b = [] # nested list for 2nd percentage
    Re_I_list_p2_b = [] # nested real current for 2nd percentage
    Im_I_list_p2_b = [] # nested imag current for 2nd percentage

    warning_sum = [] # summary of warning message
  
    vo_index = -1 # votlage index (level 0 index)

    vol = False # Flag if reading voltage line
    spe = False # Flag if reading speed line
    pec = 0 # pecentage line indicator

    regen = False # default regen data available flag
    brake_flag = False # Flag if reading/checking braking effort part
    BE_flag = False # confirm checking TE or BE part
  

    # Open the bhtpbank and read data
    with open(bhtpname) as fp:
        for index, line in enumerate(fp):
            # decide which section the code is looking            
            if line[:2].strip() == 'DB':
                bhtpbank = line[2:10].strip()
                bhtpcomment = line[10:].strip()
            if line[:3].strip() == '  M':
                continue
            if line[:3].strip() == 'REG':
                regen = True
            if line[:1].strip() == '*':
                continue
            if line[:3].strip() == 'VOL':
                vo_index = vo_index + 1 # go to the next voltage entry    
                pec = 0
                vol = True
            if line[:3].strip() == 'SPE':
                pec = 0
                spe = True
                vol = False
            if line[:3].strip() == '':
                spe = False
                pec = pec + 1
            if line[:15].strip() == 'END OF TRACTIVE':
                brake_flag = True
                vo_index = -1
                continue
            if line[:11].strip() == 'END OF DATA':
                break

            # excute data list
            if brake_flag == False:
                list_data_action(line,vol_list,speed_list,TE_list,Re_I_list,Im_I_list, \
                    TE_list_p1,Re_I_list_p1,Im_I_list_p1,TE_list_p2,Re_I_list_p2,Im_I_list_p2, \
                        vo_index,vol,spe,pec)
            else:
                list_data_action(line,vol_list_b,speed_list_b,TE_list_b,Re_I_list_b,Im_I_list_b, \
                    TE_list_p1_b,Re_I_list_p1_b,Im_I_list_p1_b,TE_list_p2_b,Re_I_list_p2_b,Im_I_list_p2_b, \
                        vo_index,vol,spe,pec)
    # showing information summary
    print(f"Summary: Checking {bhtpname}: {carnumber} Car traction profile.")
    print(f"         bhtpbank comment with '{bhtpcomment}'.")
    if regen == True:
        print("         Regenerative Braking is available.")
    else:
        print("         Regenerative Braking is NOT available.")

    print("BHTPBANK Reading Completed. Processing Calculation...")

    # checking auxiliary 
    aux_list = [] # auxiliary for each voltage level
    aux_power_check(Re_I_list,Re_I_list_p1,vol_list,speed_list,aux_list,warning_sum,carnumber,BE_flag)
    
    total_I_list =[]
    total_current(total_I_list,Re_I_list,Im_I_list)

    effi_list = []
    mech_list = [] # mechnical power
    ele_list = [] # electric power
    ele_traction_list = [] # electrical power for traction
    # use real current here for efficiency calculaion Re_I_list
    effi_calculation(effi_list,mech_list,ele_list,ele_traction_list,TE_list,Re_I_list,Re_I_list_p1,vol_list,speed_list,aux_list,BE_flag)
    effi_check(effi_list,vol_list,warning_sum,BE_flag)

    TE_check(TE_list,vol_list,speed_list,warning_sum)

    # check if braking data is available
    if len(TE_list_b) == 0:
        brake_flag = False

    if brake_flag == True:
        
        BE_flag = True
        print("Braking part is available. Checking electrical braking data...")

        BE_check(TE_list_b,vol_list_b,speed_list_b,warning_sum)

        aux_list_b = [] # auxiliary for each voltage level under regen
        aux_power_check(Re_I_list_b,Re_I_list_p1_b,vol_list_b,speed_list_b,aux_list_b,warning_sum,carnumber,BE_flag)

        effi_list_b = []
        mech_list_b = [] # mechnical power
        ele_list_b = [] # electric power
        ele_traction_list_b = [] # electrical power for traction
        # use real current here for efficiency calculaion Re_I_list
        effi_calculation(effi_list_b,mech_list_b,ele_list_b,ele_traction_list_b,TE_list_b,Re_I_list_b,Re_I_list_p1_b,vol_list_b,speed_list_b,aux_list_b,BE_flag)
        effi_check(effi_list_b,vol_list_b,warning_sum,BE_flag)
    
    # writing data to CSV file ready for excel creator

    csv_file_generate(vol_list,speed_list,TE_list,Re_I_list,Re_I_list_p1,Im_I_list,Im_I_list_p1, \
        vol_list_b,speed_list_b,TE_list_b,Re_I_list_b,Re_I_list_p1_b,Im_I_list_b,Im_I_list_p1_b,brake_flag,bhtpname)

    # test
    #print(Re_I_list_p1_b)
    #print(effi_list_b)
    # plotting output
    print("Plotting Comparison Graphs...")
    print("Plotting Tractive Effort vs Speed...") 
    plt.figure(0)
    for index, value in enumerate(vol_list):       
        plt.plot(speed_list[index],TE_list[index], 'o-', markersize = 3,label = str(value)+' V')
    plt.title("Maximum Tractive Effort")
    plt.xlabel("Speed (km/h)")
    plt.ylabel("Tractive Effort (kN)")
    plt.grid()
    plt.legend()
    plt.savefig('Tractive Effort.png')

    print("Plotting Real Current vs Speed...") 
    plt.figure(1)
    for index, value in enumerate(vol_list):       
        plt.plot(speed_list[index],Re_I_list[index], 'o-', markersize = 3,label = str(value)+' V')
    plt.title("Real Current (traction + auxiliary)")
    plt.xlabel("Speed (km/h)")
    plt.ylabel("Real Current (A)")
    plt.grid()
    plt.legend()
    plt.savefig('Real Current.png')

    print("Plotting Absolute Current vs Speed...") 
    plt.figure(2)
    for index, value in enumerate(vol_list):       
        plt.plot(speed_list[index],total_I_list[index], 'o-', markersize = 3,label = str(value)+' V')
    plt.title("Absolute Current (traction + auxiliary)")
    plt.xlabel("Speed (km/h)")
    plt.ylabel("Absolute Current (A)")
    plt.grid()
    plt.legend()
    plt.savefig('Absolute Current.png')

    print("Plotting Traction Efficiency vs Speed...") 
    plt.figure(3)
    for index, value in enumerate(vol_list):       
        plt.plot(speed_list[index],effi_list[index], 'o-', markersize = 3,label = str(value)+' V')
    plt.title("Traction Efficiency")
    plt.xlabel("Speed (km/h)")
    plt.ylabel("Traction Efficiency")
    plt.grid()
    plt.legend()
    plt.savefig('Traction Efficiency.png')

    print("Plotting Maximum Real Current vs Voltage...")
    max_current = []
    for index, value in enumerate(vol_list):
        max_current.append(max(total_I_list[index]))
    plt.figure(4)
    plt.plot(vol_list,max_current, 'o-', markersize = 3,label = 'maximum current')
    plt.title("Maximum Current vs Voltage (current limitation curve)")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Absolute Current (A)")
    plt.grid()
    plt.legend()
    plt.savefig('Current Limitation Curve.png')

    print("Plotting Maximum Active Power vs Voltage...")
    max_power = []
    for index, value in enumerate(vol_list):
        max_power.append(max(Re_I_list[index])*value/1000)
    plt.figure(5)
    plt.plot(vol_list,max_power, 'o-', markersize = 3,label = 'maximum power')
    plt.title("Maximum Active Power vs Voltage (power limitation curve)")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Active Power (kW)")
    plt.grid()
    plt.legend()
    plt.savefig('Power Limitation Curve.png')

    if brake_flag == True:
        print("Plotting Braking Effort vs Speed...") 
        plt.figure(6)
        for index, value in enumerate(vol_list_b):       
            plt.plot(speed_list_b[index],TE_list_b[index], 'o-', markersize = 3,label = str(value)+' V')
        plt.title("Maximum Electrical Braking Effort")
        plt.xlabel("Speed (km/h)")
        plt.ylabel("Electrical Braking Effort (kN)")
        plt.grid()
        plt.legend()
        plt.savefig('Electrical Braking Effort.png')

        print("Plotting Regen Real Current vs Speed...") 
        plt.figure(7)
        for index, value in enumerate(vol_list_b):       
            plt.plot(speed_list_b[index],Re_I_list_b[index], 'o-', markersize = 3,label = str(value)+' V')
        plt.title("Maximum Regen Real Current")
        plt.xlabel("Speed (km/h)")
        plt.ylabel("Regen Current (A)")
        plt.grid()
        plt.legend()
        plt.savefig('Regen Current.png')

        print("Plotting Regen Efficiency vs Speed...") 
        plt.figure(8)
        for index, value in enumerate(vol_list_b):       
            plt.plot(speed_list_b[index],effi_list_b[index], 'o-', markersize = 3,label = str(value)+' V')
        plt.title("Regenerative Efficiency")
        plt.xlabel("Speed (km/h)")
        plt.ylabel("Regenerative Efficiency")
        plt.grid()
        plt.legend()
        plt.savefig('Regen Efficiency.png')

    # show the figure
    if option_select == "2":
        plt.show(block = True) # keep interactive window open until process finsihed.

    # warning message
    if len(warning_sum) != 0:
        with open('Warning Summary.txt','w') as fw:
            fw.write("Warning Summary:\n")
            fw.write('\n'.join(warning_sum))
        print("Summary of WARNING is written to a text file...")
        SharedMethods.print_message("WARNING: Unexpected value occurs.Please check screen output for detail ! Warning Summary.txt was saved !","33")
        
    print("\nProcessing Completed.")
    
    return True

# check error
def TE_check(TE_list,vol_list,speed_list,warning_sum):
    print("Tractive Effort Checking Process...")
    for index, value in enumerate(vol_list):
        if len(TE_list[index]) > 20:
            text = f'ERROR: Traction data at {value} V has more than 20 speed entries.'
            SharedMethods.print_message(text,"31")
            warning_sum.append(text)

    # check TE votlage levels, added in v1.4
    if len(vol_list) > 10:
        text = 'ERROR: TE has more than 10 voltage entires. Maximum Storage Exceeded'
        SharedMethods.print_message(text,"31")
        warning_sum.append(text)
    return

def BE_check(TE_list_b,vol_list_b,speed_list_b,warning_sum):
    print("Braking Effort Checking Process...")
    for index, value in enumerate(vol_list_b):
        if TE_list_b[index][0] != 0:
            text = f'ERROR: Braking effort at {value} V for 0 speed is Non-Zero.'
            SharedMethods.print_message(text,"31")
            warning_sum.append(text)
        for index1, value1 in enumerate(speed_list_b[index]):
            if TE_list_b[index][index1] < 0:
                text = 'WARNING: Braking effort at {} V for {} km/h is NEGATIVE.' \
                    .format(value,value1)
                SharedMethods.print_message(text,"33")
                warning_sum.append(text)
    return

# auxiliary power check
def aux_power_check(Re_I_list,Re_I_list_p1,vol_list,speed_list,aux_list,warning_sum,carnumber,BE_flag):
    if BE_flag == False:
        print("Auxiliary Power Checking Process...") 
    else:
        print("Auxiliary Power Checking Process of Electric Braking...") 
        
    for index, value in enumerate(vol_list):
        aux_list.append(value*Re_I_list[index][0]*Re_I_list_p1[index][0]/100/1000)

    diff = max(aux_list) - min(aux_list) # calculate the difference of aux
    if diff > 5:
        if BE_flag == False:
            text = 'WARNING: Traction Part: stationary auxiliary power is not consistent at different voltage levels !'
        else:
            text = 'WARNING: Braking Part: stationary auxiliary power is not consistent at different voltage levels !'
        SharedMethods.print_message(text,"33")
        warning_sum.append(text)
#    else:
#        print('\033[1;0m') # color control warning message reset
#        print("\nStationary auxiliary power at different voltage levels is consistent (difference < 5 kW). Check PASS!")
#        print('\033[1;33m') # color control warning message Yellow
    
    # define the aux per car threshold and do the checking (only do for TE part)
    if BE_flag == False:
        for index, value in enumerate(vol_list): # checking aux power per car
            percar = aux_list[index]/carnumber
            if (percar < 20) or (percar > 40):
                text = 'WARNING: Auxiliary power per car {:.2f} kW outside the normal range (20-40 kW) at {} V' \
                    .format(percar,value)
                SharedMethods.print_message(text,"33")
                warning_sum.append(text)

    for index, value in enumerate(vol_list): # value = votage
        cur = [] # auxiliary current for difference speed (same voltage level)
        for index2, value2 in enumerate(Re_I_list[index]): # value2 = Current
            cur.append(value2*Re_I_list_p1[index][index2]/100)
        
        diff = max(cur)-min(cur)
        if diff > 5:
            print('\033[1;33m') # color control warning message Yellow
            if BE_flag == False:
                text = f"WARNING: Traction part: auxiliary power at {value} V is not consistent at different speeds!"
            else:
                text = f"WARNING: Braking part: auxiliary power at {value} V is not consistent at different speeds!"
            SharedMethods.print_message(text,"33")
            warning_sum.append(text)

            for index3, value3 in enumerate(cur): # value3 = aux current
                print("{:.2f} kW at speed {} km/h." \
                    .format(value*value3/1000,speed_list[index][index3]))
    
    if BE_flag == False:
        SharedMethods.print_message("Stationary Auxiliary Power at Different Voltage Levels:","33")
        for index, value in enumerate(vol_list):
            print(f"{aux_list[index]:.2f} kW at {value:.0f} V")
        
        print(f"Minimum stationary auxiliary power per car is {min(aux_list) / carnumber:.2f} kW")
        print(f"Maximum stationary auxiliary power per car is {max(aux_list) / carnumber:.2f} kW")
    
    return

# efficiency check
def effi_check(effi_list,vol_list,warning_sum,BE_flag):
    if BE_flag == False:       
        print("Traction Efficiency Checking Process...") 
        for index, value in enumerate(vol_list):
            if max(effi_list[index]) > 0.95:
                text = "WARNING: Maximum traction efficiency is {:.3f} at voltage level {} V!" \
                    .format(max(effi_list[index]),value)
                SharedMethods.print_message(text,"33")
                warning_sum.append(text)
    else:
        print("Regen Efficiency Checking Process...")
        for index, value in enumerate(vol_list):
            if max(effi_list[index]) > 0.95:
                text = "WARNING: Maximum regen efficiency is {:.3f} at voltage level {} V!" \
                    .format(max(effi_list[index]),value)
                SharedMethods.print_message(text,"33")
                warning_sum.append(text)
    return

def total_current(total_I_list,Re_I_list,Im_I_list):
    for index, lst in enumerate(Re_I_list):
        total_I_list.append([])
        for index2, value in enumerate(Re_I_list[index]):
            data = math.sqrt(value*value + Im_I_list[index][index2]*Im_I_list[index][index2])
            total_I_list[index].append(data)
    return

def effi_calculation(effi_list,mech_list,ele_list,ele_traction_list,TE_list,total_I_list,total_I_list_p1,vol_list,speed_list,aux_list,BE_flag):
    
    for index, value in enumerate(vol_list):
        effi_list.append([])
        mech_list.append([])
        ele_list.append([])
        ele_traction_list.append([])
        for index2, value2 in enumerate(total_I_list[index]):
            data1 = TE_list[index][index2]*speed_list[index][index2]/3.6 # calculate mechnical power N*km/h/3.6
            data2 = value*value2/1000 # electrical power V * I/1000
            aux = data2*total_I_list_p1[index][index2]/100 # total power * percentage at 0 percent of mechanical
#            if aux_list[index] >= 0:
#                data3 = data2 - aux_list[index] # power for traction, total electrical power - auxiliary power
#            else:
#                data3 = data2 # For comparision purpose only               
            if aux >= 0:
                data3 = data2 - aux # power for traction, total electrical power - auxiliary power
            else:
                data3 = data2 # For comparision purpose only
            
            mech_list[index].append(data1)
            if BE_flag == False:
                ele_list[index].append(data2)
                ele_traction_list[index].append(data3)
                if data3 == 0:
                    effi_list[index].append(0.0)
                else:
                    effi_list[index].append(data1/data3) # mechanical / electrical
            else:
                ele_list[index].append(-data2)
                ele_traction_list[index].append(-data3)
                if data1 == 0:
                    effi_list[index].append(0.0)
                else:
                    effi_list[index].append(-data3/data1) # electrical / mechanical

    return
        
def csv_file_generate(vol_list,speed_list,TE_list,Re_I_list,Re_I_list_p1,Im_I_list,Im_I_list_p1, \
        vol_list_b,speed_list_b,TE_list_b,Re_I_list_b,Re_I_list_p1_b,Im_I_list_b,Im_I_list_p1_b,brake_flag,bhtpname):
    
    with open(bhtpname+'.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile) # create the csv writer
        lock = 0
        row = 1

        writer.writerow(['Summary of Current / Power Limitation Profile'])
        row = row + 1
        writer.writerow(['','Voltage','Maximum Current (A)','Maximum Power (kW)'])
        row = row + 1

        for index, item in enumerate(vol_list):
            tempI = max(Re_I_list[index])
            tempP = tempI*item/1000
            data = ['',str(item),str(tempI),str(tempP)]
            writer.writerow(data)
            row = row + 1
        
        data = ['Maximum','','=max(C3:C'+str(row-1)+')','=max(D3:D'+str(row-1)+')']
        writer.writerow(data)
        row = row + 1

        writer.writerow('')
        row = row + 1

        writer.writerow(['Please copy the below information in the excel creator to modify:'])
        row = row + 1
        writer.writerow('')
        row = row + 1

        header1 = ['Speed(km/h)','TE(kN)','Current Real(A)','%','Current Imag(A)','%','Total Current(A)', \
            'Mech Power (kW)','Ele Power (kW)','Efficiency','Traction Power(kW)','Traction Efficiency', \
                'Aux Power'] # for bhtpbank file creator v5.7
        header2 = ['Speed(km/h)','BE(kN)','Current Real(A)','%','Current Imag(A)','%','Total Current(A)', \
            'Mech Power (kW)','Ele Power (kW)','Efficiency','E Braking Power(kW)','Regen Efficiency', \
                'Aux Power']

        for index,item in enumerate(vol_list):
            writer.writerow(['Voltage',str(item)])
            lock = row
            row = row + 1
            writer.writerow(header1)
            row = row + 1
            for index1, item1 in enumerate(speed_list[index]):
                equ1 = '=sqrt(C'+str(row)+'^2+E'+str(row)+'^2)' # equation for total current
                equ2 = '=A'+str(row)+'*B'+str(row)+'/3.6' # equation for mechanical power
                equ3 = '=G'+str(row)+'*B'+str(lock)+'/1000' # equation for ele power
                equ4 = '=if(I'+str(row)+'=0,0,H'+str(row)+'/I'+str(row)+')' # efficiency
                equ5 = '=I'+str(row)+'-M'+str(row) # equation for traction power                
                equ6 = '=if(K'+str(row)+'=0,0,H'+str(row)+'/K'+str(row)+')' # traction efficiency
                equ7 = '=C'+str(row)+'*D'+str(row)+'/100'+'*B'+str(lock)+'/1000' # equation for aux power
                data_row = [str(item1),str(TE_list[index][index1]),str(Re_I_list[index][index1]), \
                    str(Re_I_list_p1[index][index1]),str(Im_I_list[index][index1]),str(Im_I_list_p1[index][index1]), \
                        equ1,equ2,equ3,equ4,equ5,equ6,equ7]
                writer.writerow(data_row)
                row = row + 1
            writer.writerow('')
            row = row + 1
        
        if brake_flag == True:
            writer.writerow(['Braking Effort'])
            row = row + 1
            for index,item in enumerate(vol_list_b):
                writer.writerow(['Voltage',str(item)])
                lock = row
                row = row + 1
                writer.writerow(header2)
                row = row + 1
                for index1, item1 in enumerate(speed_list_b[index]):
                    equ1 = '=if(C'+str(row)+'<0,-sqrt(C'+str(row)+'^2+E'+str(row)+'^2),sqrt(C'+str(row)+'^2+E'+str(row)+'^2))' # equation for total current
                    equ2 = '=A'+str(row)+'*B'+str(row)+'/3.6' # equation for mechanical power
                    equ3 = '=if(C'+str(row)+'<0,-G'+str(row)+'*B'+str(lock)+'/1000,G'+str(row)+'*B'+str(lock)+'/1000)' # equation for ele power
                    equ4 = '=if(H'+str(row)+'=0,0,I'+str(row)+'/H'+str(row)+')' # efficiency
                    equ5 = '=if(C'+str(row)+'<0,I'+str(row)+'+M'+str(row)+',I'+str(row)+'-M'+str(row)+')' # equation for traction power                
                    equ6 = '=if(H'+str(row)+'=0,0,K'+str(row)+'/H'+str(row)+')' # traction efficiency
                    equ7 = '=C'+str(row)+'*D'+str(row)+'/100'+'*B'+str(lock)+'/1000' # equation for aux power
                    data_row = [str(item1),str(TE_list_b[index][index1]),str(Re_I_list_b[index][index1]), \
                        str(Re_I_list_p1_b[index][index1]),str(Im_I_list_b[index][index1]),str(Im_I_list_p1_b[index][index1]), \
                            equ1,equ2,equ3,equ4,equ5,equ6,equ7]
                    writer.writerow(data_row)
                    row = row + 1
                writer.writerow('')
                row = row + 1
    
    return

# train information sort and output
# #speed_list,TE_list,Re_I_list,Im_I_list,vo_index,da_index,p_index,vol,spe    
def list_data_action(line,vol_list,speed_list,TE_list,Re_I_list,Im_I_list, \
    TE_list_p1,Re_I_list_p1,Im_I_list_p1,TE_list_p2,Re_I_list_p2,Im_I_list_p2, \
        vo_index,vol,spe,pec):
    if vol == True:
        data = int(line[8:].strip()) # get the value of voltage
        vol_list.append(data)
        speed_list.append([])
        TE_list.append([])
        Re_I_list.append([])
        Im_I_list.append([])
        TE_list_p1.append([])
        Re_I_list_p1.append([])
        Im_I_list_p1.append([])
        TE_list_p2.append([])
        Re_I_list_p2.append([])
        Im_I_list_p2.append([])
    
    if spe == True:
        data = float(line[5:15].strip()) # get the value of speed
        speed_list[vo_index].append(data)
        data = float(line[20:30].strip()) # get the value of TE
        TE_list[vo_index].append(data)
        data = float(line[40:50].strip()) # get the value of Real Current
        Re_I_list[vo_index].append(data)
        data = float(line[50:].strip()) # get the value of Imag Current
        Im_I_list[vo_index].append(data)

    if pec == 1:
        data = float(line[:10].strip()) # get the value of TE percentage
        TE_list_p1[vo_index].append(data)
        data = float(line[10:20].strip()) # get the value of Real perc
        Re_I_list_p1[vo_index].append(data)
        data = float(line[20:].strip()) # get the value of Imag perc
        Im_I_list_p1[vo_index].append(data)

    if pec == 2:
        data = float(line[:10].strip()) # get the value of TE percentage
        TE_list_p2[vo_index].append(data)
        data = float(line[10:20].strip()) # get the value of Real perc
        Re_I_list_p2[vo_index].append(data)
        data = float(line[20:].strip()) # get the value of Imag perc
        Im_I_list_p2[vo_index].append(data)

    return

# programme running
if __name__ == '__main__':
    # Add your debugging code here
    simname = "DC000"  # Provide a simulation name or adjust as needed
    main_option = "2"  # Adjust as needed
    time_start = "0070000"  # Adjust as needed
    time_end = "0080000"  # Adjust as needed
    option_select = "2"  # Adjust as needed
    text_input = "LOEM360Z"  # Adjust as needed
    low_v = None  # Adjust as needed
    high_v = None  # Adjust as needed
    time_step = "4"  # Adjust as needed

    # Call your main function with the provided parameters
    main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step)
