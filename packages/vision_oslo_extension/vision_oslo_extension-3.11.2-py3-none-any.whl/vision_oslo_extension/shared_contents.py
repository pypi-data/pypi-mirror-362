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
N/A
Used Input:
Various
Expected Output:
Various
Description:
This script defines two shared classes of default values to be shared among various scripts.
This script also defines a SharedMethods class containing common functions to be used for various scripts such as checking the existence of files, time manipulation, etc. 

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
# V1.1 (Jieming Ye) - 2024-12-04 Bring simname to osop command
# V2.0 (Jieming Ye) - Update GitHub repository location
#=================================================================
# Set Information Variable
# N/A
#=================================================================


#import tkinter as tk
import os
import shutil
import importlib
import importlib.resources
import csv
import subprocess
import sys
import tempfile

from collections import Counter

class SharedVariables:
    # this class will store all shared varibles
    sim_variable = None # get when be called
    main_option = None # default varies
    osop_version = None # default update at gui_start.py
    
    # varible to be updated following version upgrade:
    # Replace 'your_package_name' with the actual name of your package
    package_name = 'vision_oslo_extension'
    support_name = 'support'
    data_name = 'data'

    tiploc_name = 'tiploc_library.csv'
    
    lastupdate = 'July / 2025' # date of checking all links below
    copyright = 'CopyRight @ 2025, All Rights Reserved.'

    bhtpbank_path = 'C:\\Users\\Public\\Documents\\VISION\\Resources\\bhtpbank'

    contacts = "Email: 'traction.power@networkrail.co.uk'"
    license_online = "https://raw.githubusercontent.com/NR-ESTractionPower/vo_addin/refs/heads/main/vision_oslo_extension_license.txt"
    support_online = "https://github.com/NR-ESTractionPower/vo_addin"
    issue_online = "https://github.com/NR-ESTractionPower/Vision-Oslo-Extension/issues"
    vo_issue_online = "https://github.com/NR-ESTractionPower/vision_oslo_issues/issues"

    bhtpbank_central_library = ("https://networkrail.sharepoint.com/:f:/r/sites/NRDDTDNS/Shared%20Documents/"
                                "05%20-%20Traction%20Power%20Modelling/02%20-%20Asset%20Data/"
                                "07%20-%20Rolling%20Stock/01%20-%20Master%20BHTPBANK%20Library?csf=1&web=1&e=gtytu8")

    license_file = os.path.join(importlib.resources.files(package_name), "license.txt")
    current_path = None # get current path
    admin_password = "passwordS3F3" # this is the Mac password

    file_extension = [".srt",".opf",".trp.txt",".tkp.txt",".mcl",".pd.fil",".pd.log",".egy.txt", \
                      ".rpt.txt",".idt",".idp.txt",".ckp",".jcn.txt",".scp.txt",".tfp",".mon.txt", \
                      ".lst.txt",".tco.txt",".plt.txt",".gd",".oslo.txt",".xrf",".ttp.txt",".dat", \
                      ".opa",".oof",".tra.txt",".ocl",".routes",".vcf.txt",".rte",".wrn.txt",".routes.mon.txt", \
                      ".C2V.routes.txt",".routes.itf.txt",".VVW",".vvw",".VCN",".vcn", \
                      ".icr",".xcr",".opc",".battery.txt",".traction.txt"]

class SharedMethods:
    # check if the script running in debug mode or not
    def is_debug_mode():
        # Checks if the debugger is attached by inspecting system flags
        return sys.gettrace() is not None

    # text file reading progress bar print out
    def text_file_read_progress_bar(index, total_line):
        """
        This function handles a text file only.
        It requires the index which is the current line  index and
        total_line which is the total number of lines in the file.

        It will output a progress bar in the console.
        """
        bar_length = 50
        if index % (total_line // 100) == 0: # update progress bar every 1%
            percent = int(index * 100 / total_line)
            filled = int(bar_length * percent / 100)
            bar = '=' * filled + '-' * (bar_length - filled)
            print(f"\rProgress: |{bar}| {percent}% completed", end='', flush=True)
        # print out the last line when index is the last line
        if index == total_line - 1:
            print(f"\rProgress: |{'=' * bar_length}| 100% completed", flush=True)        
        return

    # check bhtpbank file's existance in the source library
    def check_bhtpbank_from_root(filename):
        file_path = os.path.join(SharedVariables.bhtpbank_path,filename)

        if not os.path.isfile(file_path): # if the oof file does not exist
            SharedMethods.print_message(f"ERROR: Traction Profile {filename} does not exist. Checking required...","31")
            return False

        return file_path
    
    # check if a extraction file contains information or not
    def check_extraction_file_contents(filename):
        # Map file extensions to the required minimum number of lines
        min_lines_required = {
            'ds1': 18,  # More than 17 lines
            'd4': 13    # More than 12 lines
        }

        # Get the file extension (last suffix)
        file_extension = filename.split('.')[-1].lower()

        # Check if the extension is one we are handling
        if file_extension not in min_lines_required:
            SharedMethods.print_message(f"ERROR: Unsupported file type: {file_extension}","31")
            return False

        try:
            # Read all lines from the file
            with open(filename, 'r') as file:
                lines = file.readlines()
            
            # Check if the line count meets the requirement
            if len(lines) >= min_lines_required[file_extension]:
                return True
            else:
                SharedMethods.print_message(f"ERROR: Empty extraction contents: {filename}","31")
                return False
            
        except Exception as e:
            SharedMethods.print_message(f"ERROR: An error occurred while openning the file: {e}","31")
            return False

    # copy files from source folder to active entry
    def copy_example_files(filename):
        distribution = importlib.resources.files(SharedVariables.package_name)
        # Get the path to the package
        #package_path = distribution.location + "\\" + SharedVariables.package_name
        package_path = os.path.join(str(distribution), SharedVariables.support_name)

        # Get the absolute path of the file in the package location
        file_in_package = os.path.join(package_path, filename)
        current_path = os.getcwd() # get current path

        check_file = os.path.join(current_path, filename)

        if os.path.exists(check_file):
            print(f"File '{filename}' already exists in the current working directory. Skipping copy...")
        else:
            # Copy the file to the current working directory
            shutil.copy(file_in_package,current_path)
            print(f"File '{filename}' copied to the current working directory. Config as required...")

    # check data library files, return full path if found
    def check_data_files(filename):
        distribution = importlib.resources.files(SharedVariables.package_name)
        # Get the path to the package
        #package_path = distribution.location + "\\" + SharedVariables.package_name
        package_path = os.path.join(str(distribution), SharedVariables.data_name)

        # Get the absolute path of the file in the package location
        file_in_package = os.path.join(package_path, filename)

        if os.path.exists(file_in_package):
            print(f"Data file '{filename}' exist in the Data library. Reading will be done.")
            return file_in_package
        else:
            SharedMethods.print_message(f"WARNING: Data file '{filename}' does NOT exist in the Data library. Reading will be skipped.","33")
            return False

    #check existing file
    def check_existing_file(filename):
        print(f"Checking File {filename}...")

        first = filename.split('.')[0]
        if first == "":
            SharedMethods.print_message("ERROR: Select the simulation or required file to continue...","31")
            return False

        current_path = os.getcwd() # get current path
        file_path = os.path.join(current_path,filename) # join the file path
        if not os.path.isfile(file_path): # if the oof file does not exist
            SharedMethods.print_message(f"ERROR: Required file {filename} does not exist. Checking required...","31")
            return False
        return True

    # check the folder and file for summary
    def folder_file_check(subfolder,filename,required=True):
        """
        Check if a specific file exists in a given subfolder.
        Returns True if the file exists, False otherwise.
        if required is True, it will print an error message and exit if the file does not exist.
        """
        print(f"Checking File {filename} in {subfolder}...")
        current_path = os.getcwd() # get current path

        # Create the complete folder path
        folder_path = os.path.join(current_path, subfolder)
        
        # Check if the folder exists
        if not os.path.exists(folder_path):
            if required:
                SharedMethods.print_message(f"ERROR: Required folder {subfolder} does not exist. Check your Input. Exiting...","31")
            return False
        
        # file path
        file_path = os.path.join(folder_path,filename) # join the file path
        # print(file_path)
        if not os.path.isfile(file_path):
            if required:
                SharedMethods.print_message(f"ERROR: Required file {filename} does not exist at {subfolder}. Check your Input. Exiting...","31")
            return False
        return True

    # copy the file to a subfolder / if not exist, create the subfolder
    def copy_file_to_subfolder(subfolder, filename, new_filename=None):
        print(f"Copying File {filename} to {subfolder}...")
        current_path = os.getcwd()  # Get current path
        folder_path = os.path.join(current_path, subfolder)

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                print(f"Folder '{subfolder}' created.")
            except Exception as e:
                SharedMethods.print_message(f"ERROR: Error creating folder {subfolder}: {e}. Check your Input...", "31")
                return False

        # Determine the target file name
        target_filename = new_filename if new_filename else filename
        file_path = os.path.join(folder_path, target_filename)

        # Warn if the target file already exists
        if os.path.isfile(file_path):
            SharedMethods.print_message(f"WARNING: File {target_filename} already exists in {subfolder}. Overwriting...", "33")
            os.remove(file_path)

        # Copy the file
        try:
            shutil.copy(filename, file_path)
            print(f"File '{filename}' copied to subfolder successfully'.")
        except Exception as e:
            SharedMethods.print_message(f"ERROR: Error copying file {filename} to {file_path}: {e}. Check your Input...", "31")
            return False

        return True

    # check oof file
    def check_oofresult_file(simname):

        resultfile = simname + ".oof"
        if simname == "":
            SharedMethods.print_message("ERROR: Please select the simulation to Continue...","31")
            return False

        if not SharedMethods.check_existing_file(resultfile):
            return False

        return True

    # osop running       
    def osop_running(simname):
        # delete osop.exe if exist in the current folder
        if os.path.exists("osop.exe"):
            try:
                os.remove("osop.exe")
                SharedMethods.print_message("WARNING: Existing osop.exe deleted to avoid version conflict. Continue...","33")
            except Exception as e:
                SharedMethods.print_message(f"ERROR: Error deleting existing osop.exe: {e}. Check your Input...","31")
                return False

        # write command line
        cmdline = f'osop "{simname}"'
        # package_name = 'vision_oslo_extension'
        # Get the distribution object for your package
        distribution = importlib.resources.files(SharedVariables.package_name)
        # Get the path to the package
        package_path = str(distribution)

        if SharedVariables.osop_version == 1:
            package_path = os.path.join(package_path,'rn26')
        elif SharedVariables.osop_version == 2:
            package_path = os.path.join(package_path,'rn27')
        elif SharedVariables.osop_version == 3:
            package_path = os.path.join(package_path,'rn29')
        # add this for debugging version purpose. Default to RN26
        else:
            package_path = os.path.join(package_path,'rn26')

        with open("batch_run.bat","w") as fba:
            fba.writelines("@echo off\n")
            fba.writelines("set PATH=%PATH%;" + package_path + "\n")
            fba.writelines("@echo on\n")
            fba.writelines(cmdline)
        # os.system("batch_run.bat")

        if SharedMethods.is_debug_mode():
            print("OSOP EXTRACTION DOES NOT WORK IN DEBUG MODE DUE TO ENVIROMENT SETTINGS. MANUAL EXTRACT RESULT FIRST.")
            print("THIS PROCESS WILL BE IGNORED AND CONTINUED.")
            return True
        # JY 2024:10. Adjust to use subprocess to run OSOP
        # Run the batch file and capture output
        print("\rOSOP extraction running. Please wait......", end='', flush=True)

        process = subprocess.Popen("batch_run.bat", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            #print(process.returncode)
            #code 10029: when fatal error with space in the simname but no quatation mark. (this has been fixed by changing the cmdline)
            if process.returncode == 999:
                SharedMethods.print_message(f"\nERROR: Error when running the command: '{cmdline}'...","31")
                SharedMethods.print_message(f"ERROR: osop.exe return Error due to control data issues...","31")
                SharedMethods.print_message(f"ERROR: Possibly you are trying to extract something which is not modelled. Check your input or contract support...","31")
            else:
                SharedMethods.print_message(f"\nERROR: Error running command: {stderr.decode()}","31")
                SharedMethods.print_message(f"ERROR: Check OSOP VERSION configuration or contact support...","31")
            return False
        else:
            # this means the command was successful finished
            # Capture and print the last line of output for processing
            output_lines = stdout.decode().splitlines()
            # for line in output_lines:
            #     if line != '':
            #         print(line)
            if output_lines:
                last_line = output_lines[-1]
                if last_line == "Run completed.":
                    # check the simname.osop.lst file
                    if SharedMethods.check_osop_lst_file_status(simname):
                        print("\rOSOP run completed successfully.",flush=True)
                        return True
                    else:
                        SharedMethods.print_message(f"\nERROR: Warning from osop. Check OSOP VERSION configuration ...","31")
                        return False
                else:
                    SharedMethods.print_message(f"\nERROR: Error in osop.exe. Extraction Failed. Check OSOP VERSION configuration or contact support...","31")
                    return False
            else:
                SharedMethods.print_message(f"\nERROR: No output from osop.exe. Extraction Failed. Check OSOP VERSION configuration or contact support...","31")
                return False

    # check simname.osop.lst file for output status
    def check_osop_lst_file_status(simname):
        lst_file = simname + ".osop.lst"
        status = True # default status is True
        # read the lst file ine by line
        try:
            with open(lst_file, 'r') as file:
                for line in file:
                    if line[:25].strip() == "End of input card listing":
                        break
                    if line[:7].strip().lower() == "warning":
                        SharedMethods.print_message(f"WARNING: {line.strip()}","33")
                        status = False
        except Exception as e:
            SharedMethods.print_message(f"ERROR: Error reading the lst file {lst_file}: {e}.","31")
            status = False

        return status
        

    # rename files
    def file_rename(old_name,new_name):
        try:
            os.rename(old_name,new_name)
            print(f"File {new_name} successfully created. Processing Continue...")
        except FileExistsError:
            os.remove(new_name)
            os.rename(old_name,new_name)
            print(f"File {new_name} successfully replaced. Processing Continue...")
        except FileNotFoundError:
            SharedMethods.print_message(f"ERROR: File {new_name} FAILED as the OSOP extraction fail. Check Input...","31")

    # module to check 7 digit user input time
    def time_input_process(time_string,option_back):
        """
        This function processes a 7-digit time string in the format DHHMMSS.
        It returns original string if option is 1, or the total seconds if option is 2.
        It return False if the input is invalid.
        """
        print(f"Checking 7 digit time input: '{time_string}'...")

        if not len(time_string) == 7:
            SharedMethods.print_message("ERROR: Invalid time format input. Press reenter the 7 digit time.","31")
            return False

        seconds_int = 0        
        day = int(time_string[:1])
        hour = int(time_string[1:3])
        minute = int(time_string[3:5])
        second = int(time_string[5:7])

        if not 0 <= day <= 9:
            SharedMethods.print_message("ERROR: Invalid DAY input (0-9). Press reenter the 7 digit time.","31")
            return False
                
        if 0 <= hour <= 24:
            seconds_int += hour*60*60
        else:
            SharedMethods.print_message("ERROR: Invalid HOUR input (0-24). Press reenter the 7 digit time.","31")
            return False
                
        if 0 <= minute <= 60:
            seconds_int += minute*60
        else:
            SharedMethods.print_message("ERROR: Invalid MINUTE input (0-60). Press reenter the 7 digit time.","31")
            return False
                
        if 0 <= second <= 60:
            seconds_int += second
        else:
            SharedMethods.print_message("ERROR: Invalid SECOND input (0-60). Press reenter the 7 digit time.","31")
            return False

        if option_back == 1:
            return time_string
        else:
            return seconds_int

    # check the propoer life file of the model
    def check_and_extract_lst_file(simname, time_start=None, time_end=None):
        
        filename = simname + ".osop.lst"
        opcname = simname + ".opc"
        flag_time_boundary = False # default is False

        if time_start is not None and time_start is not None:
            time_start = SharedMethods.time_input_process(time_start,1)
            time_end = SharedMethods.time_input_process(time_end,1)

            if time_start and time_end: # both are valid
                flag_time_boundary = True

        # Create batch file for list command and run the batch file
        # and define the lst file name to process the information
        # generate List file
        if not os.path.isfile(filename):
            with open(opcname,"w") as fopc:
                if flag_time_boundary:
                    fopc.writelines("LIST INPUT FILE FROM "+time_start+" TO "+time_end+"\n")
                else:
                    fopc.writelines("LIST INPUT FILE\n")
            if not SharedMethods.osop_running(simname):
                return False
        else:
            lst_file_size = os.path.getsize(filename)
            if lst_file_size < 10000: # a random size (bytes) to check if lst should be redone (10000 bytes = 10 kb)
                with open(opcname,"w") as fopc:
                    if flag_time_boundary:
                        fopc.writelines("LIST INPUT FILE FROM "+time_start+" TO "+time_end+"\n")
                    else:
                        fopc.writelines("LIST INPUT FILE\n")
                if not SharedMethods.osop_running(simname):
                    return False
            else:
                SharedMethods.print_message(f"WARNING: {simname} list file extraction is SKIPPED as previously done (>10kb).","33")
                SharedMethods.print_message(f"WARNING: Manually delete the file if a new extraction is required.","33")
        
        return True
    
    # module to read the text file input    
    def file_read_import(filename,simname):
        
        if not os.path.isfile(filename): # if the file exist
            SharedMethods.print_message(f"ERROR: Required input file {filename} does not exist. Please select another option.","31")
            return False

        # reading the train list file
        text_input = []
        with open(filename) as fbrlist:
            for index, line in enumerate(fbrlist):
                item = line[:50].strip()
                if not item:
                    continue # skip the empty line

                if item in text_input:
                    SharedMethods.print_message(f"WARNING: Duplicate item '{item}' identified. This will be read again.","33")
                text_input.append(item)

        return text_input
    
    # module to convert 7 digits time to time format 
    def time_convert(time_string):
        
        #time_string = input()          
        day = int(time_string[:1])
        hour = int(time_string[1:3])
        minute = int(time_string[3:5])
        second = int(time_string[5:7])

        if not day == 0:
            day = day # to be updated to process info at a later stage
        time = str(hour) + ":" + str(minute) + ":" + str(second)        
        #debug purpose
        #print(seconds_int)
        # Return the second integer number as same used in the list file           
        return time

    # read tiploc information
    def get_tiploc_library():
        tiploc = {} # create a empty tiploc
        
        filename = SharedVariables.tiploc_name
        distribution = importlib.resources.files(SharedVariables.package_name)
        package_path = os.path.join(str(distribution), SharedVariables.data_name)

        # Get the absolute path of the file in the package location
        filepath = os.path.join(package_path, filename)
        try:
            with open(filepath,'r') as file:
                csv_reader = csv.reader(file)
                first_row = True  # Flag to identify the first row
                for row in csv_reader:
                    if first_row:
                        # Read row[1] as a string referring to the date
                        updated_date = row[1]
                        first_row = False  # Reset the flag after processing the first row
                    else:
                        # Continue the logic for subsequent rows
                        key = row[0]
                        value = row[1]
                        tiploc[key] = value
            
            print(f"\nTIPLOC Libray Last Update: {updated_date}")        
            SharedMethods.print_message("ATTENTION: Please contact support if a TIPLOC library update is needed!","33")
        except Exception as e:
            SharedMethods.print_message(f"ERROR: Reading CIF TIPLOC lookup library failed. {e}. Contact support...","31")
            return False
        
        return tiploc

    # open a file in support folder
    def open_support_file(filename):
        distribution = importlib.resources.files(SharedVariables.package_name)
        package_path = os.path.join(str(distribution), SharedVariables.support_name)
        # Get the absolute path of the file in the package location
        file_in_package = os.path.join(package_path, filename)

        # create a temp directory and copy the file there
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, filename)

        try:
            shutil.copy(file_in_package, temp_file) # copy the file to temp directory
            subprocess.Popen(['start', '', temp_file], shell=True,close_fds=True)
        except Exception as e:
            SharedMethods.print_message(f"ERROR: Error opening file with default app: {e}","31")

        return
    
    # find duplication in a list
    def find_duplicates(lst):
        # Count occurrences of each element
        counts = Counter(lst)
        # Extract elements with more than one occurrence
        duplicates = [item for item, count in counts.items() if count > 1]

        if not duplicates == []:
            SharedMethods.print_message(f"ERROR: Duplicated ID exists in the input lists: {duplicates}.","31")
            SharedMethods.print_message(f"ERROR: Please clear the duplicates before continue...","31")
            return False
        else:
            return True

    # define the running in thread mechanism    
    def launch_new_thread_or_process(import_option, sim_name, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step,cwd=None):
        # Define a dictionary mapping import_option to module names
        module_mapping = {
            "cif_prepare.py": "cif_prepare",
            "model_check.py": "model_check",
            "oslo_extraction.py": "oslo_extraction",
            "post_processing.py": "post_processing",
            "average_load.py": "average_load",
            "protection_if.py": "protection_if",
            "grid_connection.py": "grid_connection",
            "ole_processing.py": "ole_processing",
            "sfc_assess.py": "sfc_assess",
            "batch_processing.py": "batch_processing",
            "dc_summary.py": "dc_summary",
            "dc_single_end_feeding.py": "dc_single_end_feeding",
            "dc_falling_voltage_protection.py": "dc_falling_voltage_protection",
            "battery_processing.py":"battery_processing",
            "cif_output_analysis.py":"cif_output_analysis",
            "simulation_batch_run.py":"simulation_batch_run",
            "bhtpbank_check.py":"bhtpbank_check",
        }

        if cwd:
            # Change the current working directory to the specified path
            # this is compolsory for new process
            os.chdir(cwd)

        # Get the module name corresponding to import_option
        module_name = module_mapping.get(import_option)

        # Import the module
        if module_name:
            fc = importlib.import_module(f"{SharedVariables.package_name}.{module_name}")
            #from vision_oslo_extension import module_name as fc
        else:
            # Handle the case when import_option doesn't match any module
            print("Invalid import_option:", import_option)
        
        try:    
            continue_process = fc.main(sim_name, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step)
            if not continue_process:
                # Do something if the process should not continue
                # Print error message in red
                SharedMethods.print_message("ERROR: Process terminated due to captured issue. "
                                            "Please check the error history above or contact support. "
                                            "You can continue using other options...", '31')
            else:
                # Do something if the process should continue
                # Print success message in green
                SharedMethods.print_message("Action successfully completed. "
                                            "Check monitor history above and result files in your folder.", '32')
        
        except Exception as e:
            SharedMethods.print_message(f"ERROR: UNEXPECTED! PLEASE REPORT BUG AND CONTACT SUPPORT... ", '31')
            SharedMethods.print_message(f"ERROR: source code module - {import_option}: {e}","31")
    
    def print_message(message, color_code):
        os.system("")
        color_start = f'\033[1;{color_code}m'   # Start color
        color_reset = '\033[1;0m'               # Reset color
        print(color_start + message + color_reset)