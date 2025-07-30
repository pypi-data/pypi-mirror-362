#
# -*- coding: utf-8  -*-
#=================================================================
# Created by: Jieming Ye
# Created on: May 2025
# Last Modified: May 2025
#=================================================================
# Copyright (c) 2025 [Jieming Ye]
#
# This Python source code is licensed under the 
# Open Source Non-Commercial License (OSNCL) v1.0
# See LICENSE for details.
#=================================================================
"""
Pre-requisite: 

Used Input:
BatchConfiguration.csv: Configuration file that saves the batch simulation settings
Expected Output:
Runned simulation in various folder
Description:
This script allow running simulation multiple times unattended

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
#
#=================================================================
# Set Information Variable
# N/A
#=================================================================

import os
import re
import csv
from pywinauto import Application
from pywinauto.keyboard import send_keys
from pywinauto.findwindows import find_windows
from pywinauto.findwindows import ElementAmbiguousError
from pywinauto.win32functions import IsWindow
import time

from vision_oslo_extension.shared_contents import SharedMethods

def main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):

    #User Interface - Welcome message:
    print("")
    print("Batch Running Programm - - - >")
    print("")

    #define the file name and check if the file exist or not
    control_file = text_input + ".csv"

    maximum_running_time = 86400 # 24 hours in seconds

    if not SharedMethods.check_existing_file(control_file): # if the control file
        return False

    control = precheck_control_file(control_file) # read the control file

    if control ==[]:
        SharedMethods.print_message("ERROR: No valid control set found. Batch Run Terminated...","31")
        return False

    if not create_simulation_folder(control): # create the simulation folder
        return False
    
    # run the simulation in each folder
    if not run_simulation(control,maximum_running_time):
        return False
    
    return True

def precheck_control_file(control_file):
    """
    Read the control file, do some pre-checking and return the valid control set
    """
    with open(control_file, 'r') as file:
        reader = csv.reader(file)
        control = list(reader)

    total_set = len(control) - 1  # Exclude header
    print(f"Total simulation number in the control file: {total_set}")

    valid_control = []

    for i in range(total_set):
        # control [i][0] = simulation name
        # control [i][1] = simulation number
        # control [i][2] = OSLO run command Y/N
        # control [i][3] = Battery run command Y/N
        # control [i][4] = OSLO run control file
        # control [i][5] = Battery run control file

        print(f"********** Checking Control Set {i + 1}: ***********")
        valid = True  # Assume the control set is valid
        simfilename = control[i + 1][0] + ".vvw"
        if not SharedMethods.check_existing_file(simfilename):  # Check if the simulation file exists
            valid = False
        
        # check if simulator number is a positive integer and not zero
        try:
            sim_number = int(control[i + 1][1])
            if sim_number <= 0:
                SharedMethods.print_message("WARNING: Simulation number should be a positive integer. Not valid control set. Ignored...","33")
                valid = False
        except ValueError:
            SharedMethods.print_message("WARNING: Simulation number should be a positive integer. Not valid control set. Ignored...","33")
            valid = False

        if control[i + 1][2] == "Y":
            oclfilename = control[i + 1][0] + ".ocl"
            extraolso = control[i + 1][4]
            if not SharedMethods.check_existing_file(oclfilename):
                valid = False
            if not SharedMethods.check_existing_file(extraolso):
                valid = False
            
            if control[i + 1][3] == "Y":
                extrabatoslo = control[i + 1][5]
                if not SharedMethods.check_existing_file(extrabatoslo):
                    valid = False
        else:
            SharedMethods.print_message("WARNING: OSLO running is NOT enabled.","33")
            if control[i + 1][3] == "Y":
                SharedMethods.print_message("WARNING: Battery run Y is not valid without OSLO run Y. Not valid control set. Ignored...","33")
                valid = False
        
        if valid == False:
            SharedMethods.print_message("WARNING: Not valid control set. Ignored...","33")
        else:
            valid_control.append(control[i + 1])
    
    return valid_control

def create_simulation_folder(control):
    """
    Create the simulation folder and copy the simulation files
    """
    print("\nPreparing simulation folders...")

    for i in range(len(control)):

        print("*****************************")
        foldername = f'{control[i][0]}_{i+1}'

        filename = f'{control[i][0]}.vvw'
        newfilename = f'{control[i][0]}_{i+1}.vvw'
        if not SharedMethods.copy_file_to_subfolder(foldername, filename, newfilename):
            return False
        if control[i][2] == "Y":
            oclfilename = f'{control[i][0]}.ocl'
            newfilename = f'{control[i][0]}_{i+1}.ocl'
            if not SharedMethods.copy_file_to_subfolder(foldername, oclfilename, newfilename):
                return False
            extraolso = control[i][4]
            if not SharedMethods.copy_file_to_subfolder(foldername, extraolso, "extra.oslo"):
                return False
            
        if control[i][3] == "Y":
            extrabatoslo = control[i][5]
            if not SharedMethods.copy_file_to_subfolder(foldername, extrabatoslo, "extra.bat.oslo"):
                return False
        
    return True

def run_simulation(control,maximum_running_time):
    """
    Run the simulation in each folder
    """
    print("\nRunning simulation...")

    for i in range(len(control)):
        # initialize
        oslorun = False
        batteryrun = False
        sim_number = int(control[i][1])
        foldername = f'{control[i][0]}_{i+1}'
        simname = f'{control[i][0]}_{i+1}.vvw'

        # check the control set
        if control[i][2] == "Y":
            oslorun = True
            if control[i][3] == "Y":
                batteryrun = True

        print(f"********** Running simulation in {foldername}...")

        # open the file within the folder
        current_path = os.getcwd() 
        sim_path = os.path.join(current_path, foldername, simname)

        # open the simulation file and set the windows to front focus
        try:
            os.startfile(sim_path)
        except Exception as e:
            SharedMethods.print_message(f"WARNING: Error opening file {sim_path}: {e}. Jump to next control set...","33")
            continue

        # wait for the simulation to open and set the window to front focus
        time.sleep(3) # wait 5 seconds for the simulation to open

        retries = 5
        # # get regex pattern for the first 50 characters of the simulation path
        # # This is to ensure that the path is not too long for the regex pattern
        # # NOTE this is not a perfect solution, but it is a workaround for the long path issue
        # # Escape sim_path for regex use
        # escaped_path = re.escape(sim_path[:50]) # get the first 50 characters of the simulation path

        # program allows 5*5 times 25 seconds to open the simulation
        while retries > 0:
            try:
                app = Application(backend='win32').connect(title_re=f'^VISION - ') # expect the title to be like "VISION - <path to the file>"
                app_window = app.window(title_re=f'^VISION - ')
                app_window.set_focus()
                break

            # if more than one VISION window is opened, it will raise an exception as ElementAmbiguousError, allow this exception to continue
            except ElementAmbiguousError:
                SharedMethods.print_message("WARNING: More than one VISION window found. Application will use the top level window...","33")
                break # break the while loop

            # other exceptions, such as the file not found or the application not responding
            except Exception as e:
                SharedMethods.print_message(f"WARNING: Unable to link the application: {e}. Retrying after 5 seconds...","33")
                time.sleep(5)
                retries -= 1
            
        if retries == 0:
            SharedMethods.print_message(f"ERROR: Unable to activate window for {simname} after multiple retries. Jumping to next control set...","31")
            continue # continue to the next control set

        print(f"Simulation {simname} application linked successfully.")

        # app window has been set to focus if the code reaches here
        time.sleep(0.5)
        # Bring the setup simulation dialog to the front
        send_keys('%(rf)')  # Alt + R, then F
        time.sleep(0.5)

        # if any warning happens, the application will pop up a warning window
        try:
            warning_dlg = app.window(title="VISION")
            warning_dlg.wait('visible', timeout=2)
            warning_dlg.set_focus()
            send_keys('%(y)')  # Alt + Y
        
        except Exception as e:
            pass

        # wait for the "Setup Simulation" dialog to appear
        try:
            # wait for the "Setup Simulation" dialog to appear
            sim_dlg = app.window(title="Setup Simulation")  # adjust if needed
            sim_dlg.wait('visible', timeout=10)

            # press down key to select the simulation
            # press down key time the same as sim_number
            for _ in range(sim_number):
                send_keys('{DOWN}')

            # press tab key to select the simulation control
            send_keys('{TAB}')
            # press down key three times to select the batch run
            send_keys('{DOWN 3}')

            # check the OSLO checkbox state
            checkbox = sim_dlg.child_window(title="Run &OSLO", class_name="Button")

            # if OSLO is run, press the button the check the checkbox
            if oslorun:
                if checkbox.get_check_state() != 1: # check if the checkbox is not checked
                    # focus the check box and send space key
                    checkbox.set_focus()
                    send_keys('{SPACE}')  # check the checkbox
            
            # provision for application RN-29
                try:
                    if batteryrun:
                        # check the Battery checkbox state
                        battery_checkbox = sim_dlg.child_window(title="Run &Battery Train", class_name="Button")
                        if battery_checkbox.get_check_state() != 1:
                            battery_checkbox.set_focus()
                            send_keys('{SPACE}')
                    else:
                        # uncheck the Battery checkbox
                        battery_checkbox = sim_dlg.child_window(title="Run &Battery Train", class_name="Button")
                        if battery_checkbox.get_check_state() == 1:
                            battery_checkbox.set_focus()
                            send_keys('{SPACE}')
                except Exception as e:
                    pass # this is to avoid the error if the Battery checkbox is not found, which is normal if the OSLO is not run

            else:
                # uncheck the OSLO checkbox
                if checkbox.get_check_state() == 1:
                    checkbox.set_focus()
                    send_keys('{SPACE}')

        except Exception as e:
            SharedMethods.print_message(f"ERROR: Failed to setup control: {e}. Continue to the next one.","31")
            # close the application
            app_window.close()
            time.sleep(5)
            continue # continue to the next control set
        
        # if the code reaches here, it means the "Setup Simulation" dialog is opened and the controls are set correctly
        time.sleep(1)
        # start running the simulation by alt + R
        send_keys('%(r)')  # Alt + R

        retries = 5
        # ensure the sim_dlg has been closed. If not, enter alt + R again after 1 second, maximum 5 times
        # this is to avoid user accidentally leaving the "Setup Simulation" dialog open
        while retries > 0:
            # check if the "Setup Simulation" dialog is still open
            if sim_dlg.exists(timeout=1):
                SharedMethods.print_message("WARNING: Setup Simulation dialog still open. Retrying after 1 second...","33")
                time.sleep(1)
                sim_dlg.set_focus()  # ensure the dialog is focused
                send_keys('%(r)')  # Alt + R
                retries -= 1
            else:
                break

        # programe allows 10*5=50 seconds for dataprep4 if another windows "simname - VISION Simulator" is lunched or not
        simulation_finished = False
        simulation_success = False
        time.sleep(0.5)
        retries = 10
        while retries > 0:
            try:
                # check if the new window is opened
                simulator_handles = find_windows(title=f'{foldername} - VISION Simulator')
                if simulator_handles: # simualtor process started
                    simulator_handle = simulator_handles[0]
                    break
                else:
                    # try to see if the another VISION warning window pop up blocked the process
                    try:
                        # try to check if any errors and warnings from windows title pops up
                        # this will happen if the simulation contains errors and cannot be run
                        status = app.window(title_re="Errors and Warnings")
                        if status.exists(timeout=1):
                            simulation_finished = True
                            break
                        
                        # try to check if another simulaiton finish or signalling berthing warnings pops up
                        # this will happen if the simulation is too fast to finish
                        status = app.window(title="VISION")
                        if status.exists(timeout=1):
                            status.set_focus()
                            # Get all Static text controls (common for message dialogs)
                            static_texts = status.children(class_name="Static")
                            # Search for the one that contains the expected message
                            for static in static_texts:
                                if static.window_text() == "Simulation finished.": # this only happens if the simulatoin is too fast to finish
                                    simulation_finished = True
                                    simulation_success = True
                                    break # break the message checking loop
                            if simulation_finished:
                                break
                            
                            # reaching here means this is the pre simulation warning window (this indicate initlaization error of simulator4)
                            send_keys('{ENTER}')
                            time.sleep(5) # this is to wait the dataprep4 stage.
                            continue # continue to the next loop to check if the simulator window is opened
                    except Exception as e:
                        print(f"{e}")
                        pass
                    # continue the process
                    SharedMethods.print_message("WARNING: Simulator window not started. Retrying after 5 seconds...","33")
                    time.sleep(5)
                    retries -= 1
            except Exception as e:
                SharedMethods.print_message("WARNING: Unexpected happens. Retrying after 5 seconds...","33")
                time.sleep(5)
                retries -= 1

        if not simulation_finished:
            if retries == 0:
                SharedMethods.print_message(f"ERROR: Unable to activate window for {simname} after multiple retries. Jumping to next control set...","31")
                # close the application
                app_window.close()
                time.sleep(5)
                continue # continue to next control set
            
            print(f"Simulation {simname} started successfully...")
            SharedMethods.print_message(f"\nWARNING: Simulation {simname} now recorded in another console. This monitor will wait until the simulation finished...","33")
            time.sleep(0.5) 
            # minimize the application windows app_window
            app_window.minimize()
            # start the timer
            simtime = 0

            # wait unntil the simulator_handle disappread (simulation finished)
            while IsWindow(simulator_handle):
                time.sleep(5)
                simtime += 5
                if simtime > maximum_running_time:
                    SharedMethods.print_message(f"ERROR: Simulation {simname} running time exceeded the 24 hours. Process terminated...","31")
                    # close the application
                    app_window.close()
                    time.sleep(5)
                    return False

                # if the app_windows is closed by people arbitrarily, stop the process
                if not app_window.exists(timeout=1):
                    SharedMethods.print_message(f"ERROR: Simulation {simname} closed by User. Process terminated...","31")
                    # close the simulator handle if it still exists
                    if IsWindow(simulator_handle):
                        simulator_app = Application(backend='win32').connect(handle=simulator_handle)
                        simulator_app.window(handle=simulator_handle).close()
                    return False

        # if the code reaches here, it means the simulator window has been closed.
        # check if another VISION window pop up
        try:
            status = app.window(title="VISION")
            if status.exists(timeout=5):
                status.set_focus()
                # Get all Static text controls (common for message dialogs)
                static_texts = status.children(class_name="Static")
                # Search for the one that contains the expected message
                simulation_success = False
                for static in static_texts:
                    if static.window_text() == "Simulation finished.":
                        simulation_success = True
                        break
                # if the window contents is text "Simulation finished"
                if simulation_success:
                    # check if the simulation folder contains the file "FatalSimulatorError.log" 
                    if not SharedMethods.folder_file_check(foldername, "FatalSimulatorError.log",False):
                        SharedMethods.print_message(f"\nINFO: Simulation {simname} finished successfully...","32")
                    else:
                        SharedMethods.print_message(f"\nERROR: Simulation {simname} terminated due to fatal error...","31")
                else:
                    SharedMethods.print_message(f"\nERROR: Simulation {simname} terminated due to errors...","31")
                send_keys('{ENTER}')
                time.sleep(0.5)
        except Exception as e:
            SharedMethods.print_message(f"WARNING: Simulation {simname} terminated unexpected: {e}...","33")
            time.sleep(0.5)
            pass

        # close the application
        app_window.close()
        time.sleep(5)

    return True

# programme running
if __name__ == "__main__":
    # Add your debugging code here
    simname = "test"  # Provide a simulation name or adjust as needed
    main_option = "2"  # Adjust as needed
    time_start = "0070000"  # Adjust as needed
    time_end = "0080000"  # Adjust as needed
    option_select = "3"  # Adjust as needed
    text_input = "BatchControl"  # Adjust as needed
    low_v = None  # Adjust as needed
    high_v = None  # Adjust as needed
    time_step = None  # Adjust as needed

    # Call your main function with the provided parameters
    main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step)

