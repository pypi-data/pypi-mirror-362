#
# -*- coding: utf-8  -*-
#=================================================================
# Created by: Jieming Ye
# Created on: Feb 2024
# Last Update: Feb 2024
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
N/A
Expected Output:
N/A
Description:
This script defines the base frame to be used all other pages except the first page which is defined in gui_start.py. 
This defines frame creation method, common button action and comment input action.

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
#=================================================================
# Set Information Variable
# N/A
#=================================================================

import tkinter as tk
from tkinter import filedialog
from threading import Thread
from multiprocessing import Process
from vision_oslo_extension.shared_contents import SharedMethods, SharedVariables

import os

class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def create_frame(self, fill=None, side = None, row_weights=None, column_weights=None):
        frame = tk.Frame(self)
        if fill:
            frame.pack(fill=fill,side=side)
        if row_weights:
            for i, weight in enumerate(row_weights):
                frame.rowconfigure(i, weight=weight)
        if column_weights:
            for i, weight in enumerate(column_weights):
                frame.columnconfigure(i, weight=weight)
        return frame

    def auto_excel_select(self, input):
        initial_dir = os.getcwd()
        file_path = filedialog.askopenfilename(title="Select File...", initialdir=initial_dir)
        if file_path:
            print(f"Selected file: {file_path}")
            file_name = os.path.basename(file_path)
            # Split the file name based on the last dot
            simname = '.'.join(file_name.split('.')[:-1]) if '.' in file_name else file_name
            #print(simname)
            input.set(simname)
            # update the working directory to the selected file's directory
            selected_dir = os.path.dirname(file_path)
            selected_dir = os.path.normpath(selected_dir)  # normalize the path (use "\\"" instead of windows stype "/"")
            if selected_dir != os.getcwd():
                os.chdir(selected_dir)
                SharedVariables.current_path = selected_dir
                self.controller.working_directory.set(selected_dir)
                SharedMethods.print_message(f"ATTENTION: Working directiory set to:\n{selected_dir}","33")

    def auto_file_select(self, input):
        initial_dir = os.getcwd()
        file_path = filedialog.askopenfilename(title="Select File...", initialdir=initial_dir)
        if file_path:
            print(f"Selected file: {file_path}")
            file_name = os.path.basename(file_path)
            input.set(file_name)
            # update the working directory to the selected file's directory
            selected_dir = os.path.dirname(file_path)
            selected_dir = os.path.normpath(selected_dir)  # normalize the path (use "\\"" instead of windows stype "/"")
            if selected_dir != os.getcwd():
                os.chdir(selected_dir)
                SharedVariables.current_path = selected_dir
                self.controller.working_directory.set(selected_dir)
                SharedMethods.print_message(f"ATTENTION: Working directiory set to:\n{selected_dir}","33")
                
    def run_new_thread_or_process(self, target_script, **inputs):
        """
        Run a target script in a separate thread with the provided inputs.
        input format:
        key_string1 = tkinter_object1, key_string2 = tkinter_object2, ... (all optional)
        This method prepares the arguments for the target script and starts a new thread to execute it.
        ALLOWED INPUTS:

        - sim_name: The name of the simulation (tkinter variable)
        - main_option: The main option for the simulation (tkinter variable)
        - time_start: The start time for the simulation (tkinter variable)
        - time_end: The end time for the simulation (tkinter variable)
        - option_select: The selected option for the simulation (tkinter variable)
        - text_input: Additional text input for the simulation (tkinter variable)
        - low_v: The low threshold for the simulation (tkinter variable)
        - high_v: The high threshold for the simulation (tkinter variable)
        - time_step: The time step for the simulation (tkinter variable)
        - current_path: The current working directory (tkinter variable)
        - independent_process: If True, run in a separate process instead of a thread (boolean)

        """

        try:
            # Get shared variables that are always needed
            sim_name = SharedVariables.sim_variable.get()
            main_option = SharedVariables.main_option
            
            # Initialize args with defaults
            args = [
                target_script,                      # Position 0 = target script
                sim_name,                           # Position 1 = sim_name (controlled via shared variable)
                main_option,                        # Position 2 = main_option (controlled via shared variable)
                None,                               # Position 3 = time_start
                None,                               # Position 4 = time_end
                None,                               # Position 5 = option_select
                None,                               # Position 6 = text_input
                None,                               # Position 7 = low_v
                None,                               # Position 8 = high_v
                None,                               # Position 9 = time_step
                SharedVariables.current_path,       # Position 10 = current_path (current working directory controlled via shared variable)
            ]

            # preprare a mapping of key strings and arguments indexes
            input_mapping = {
                'sim_name': 1,
                'main_option': 2,
                'time_start': 3,
                'time_end': 4,
                'option_select': 5,
                'text_input': 6,
                'low_v': 7,
                'high_v': 8,
                'time_step': 9,
                'current_path': 10,
            }

            # initialize independent process flag
            independenet_process = False

            # Update args with provided inputs
            for key, value in inputs.items():
                if key in input_mapping:
                    index = input_mapping[key]
                    if isinstance(value, tk.Variable):
                        args[index] = value.get()  # Get the value from the tkinter variable
                    else:
                        args[index] = value  # Directly use the provided value
                else:
                    if key == 'independent_process':
                        # If the key is 'independent_process', set the flag
                        independenet_process = value if isinstance(value, bool) else False
                    else:
                        SharedMethods.print_message(
                            f"WARNING: Unrecognized input key '{key}' provided. Skipping...",
                            '33'
                        )

            # decide run multiprocessing or threading
            if independenet_process:
                # run in separate process
                process = Process(
                    target=SharedMethods.launch_new_thread_or_process,
                    args=tuple(args)
                )
                process.start()
            else:
                # Run in separate thread
                thread = Thread(
                    target=SharedMethods.launch_new_thread_or_process,
                    args=tuple(args)
                )
                thread.start()

        except Exception as e:
            SharedMethods.print_message(
                f"ERROR: Error in threading/processing...{e}\nContact Support / Do not carry out multiple tasking at the same time.",
                '31'
            )
