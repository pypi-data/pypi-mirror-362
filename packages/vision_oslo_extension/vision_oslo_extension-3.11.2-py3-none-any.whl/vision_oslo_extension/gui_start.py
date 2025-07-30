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
-supporting- folder with various templates. 
Used Input:
Calling from master.py
Expected Output:
Main GUI window and Menu Bar
Description:
This script defines main properties of GUI such as font, title, size, etc.
This script also defines the main frame of all GUI window and menu bar, including actions of each item listed in the menu.
Attention:
This script needs to be updated once a new frame / page is developed. This could be achieved by importing the new class and updating top-level frame list (def _init_)

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
# V2.0 (Jieming Ye) - Refactor to lazy import frames to speed up start up
#=================================================================
# Set Information Variable
# N/A
#=================================================================

# Third Party
import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog
import os
import importlib.metadata
import webbrowser
import subprocess
import threading
import queue

# Internal imports
from vision_oslo_extension.shared_contents import SharedVariables, SharedMethods
from vision_oslo_extension.base_frame import BasePage

# Commonly accessed frames to preload
PRELOAD_FRAMES = {
    'PageOne', 'PageTwo', 'PageThree', 'PageFour', 'PageFive', 'PageSix'
}

# Lazy imports for frames
def import_frames():
    from vision_oslo_extension.main_page_frame import Page0, PageOne, PageTwo, PageThree, PageFour, PageFive, PageSix
    from vision_oslo_extension.extraction_frame import F01, F02, F03, F04, F05, F06, F07, F08, F09, F10, F11, F12, F13, F14
    from vision_oslo_extension.processing_frame import P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13, P14
    from vision_oslo_extension.check_frame import C01, C02, C03, C04
    from vision_oslo_extension.input_frame import S01, S02, S03, S04, S05, S06
    return {
        'Page0': Page0, 'PageOne': PageOne, 'PageTwo': PageTwo, 'PageThree': PageThree,
        'PageFour': PageFour, 'PageFive': PageFive, 'PageSix': PageSix,
        'F01': F01, 'F02': F02, 'F03': F03, 'F04': F04, 'F05': F05, 'F06': F06,
        'F07': F07, 'F08': F08, 'F09': F09, 'F10': F10, 'F11': F11, 'F12': F12,
        'F13': F13, 'F14': F14,
        'P01': P01, 'P02': P02, 'P03': P03, 'P04': P04, 'P05': P05, 'P06': P06,
        'P07': P07, 'P08': P08, 'P09': P09, 'P10': P10, 'P11': P11, 'P12': P12,
        'P13': P13, 'P14': P14,
        'C01': C01, 'C02': C02, 'C03': C03, 'C04': C04,
        'S01': S01, 'S02': S02, 'S03': S03, 'S04': S04, 'S05': S05, 'S06': S06
    }


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Set initial window size and make it resizable
        # self.geometry("700x500")
        # self.resizable(True, True)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.sub_title_font = tkfont.Font(family='Helvetica', size=12, weight="bold")
        self.big_text_font = tkfont.Font(family='Helvetica', size=10, weight="bold")
        self.text_font = tkfont.Font(family='Helvetica', size=10)
        self.title('Vision-Oslo Extension')
        
        # add shared string variable of current work directory
        self.working_directory = tk.StringVar()
        self.working_directory.set(os.getcwd())

        # Setup the container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self._frame_classes = None  # Will store frame classes when needed
        self._container = container
        self._preload_queue = queue.Queue()

        # Initialize only the start page
        frame = StartPage(parent=container, controller=self)
        self.frames["StartPage"] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        self._setup_menu()
        
        # Start preloading common frames after a short delay
        self.after(100, self._start_preloading)

    def _start_preloading(self):
        """Start background thread to preload common frames."""
        def preload_worker():
            try:
                if self._frame_classes is None:
                    self._frame_classes = import_frames() # import the frame classes
                
                for page_name in PRELOAD_FRAMES:
                    if page_name not in self.frames and page_name in self._frame_classes:
                        frame_class = self._frame_classes[page_name]
                        # Queue the frame creation to be done in the main thread
                        self._preload_queue.put((page_name, frame_class))
                        # Process one frame at a time in the main thread
                        self.after(0, self._process_preload_queue)
            except Exception as e:
                print(f"Preloading warning: {e}")

        thread = threading.Thread(target=preload_worker)
        thread.daemon = True
        thread.start()

    def _process_preload_queue(self):
        """Process queued frame creation in the main thread."""
        try:
            while not self._preload_queue.empty():
                page_name, frame_class = self._preload_queue.get_nowait()
                if page_name not in self.frames:
                    frame = frame_class(parent=self._container, controller=self)
                    self.frames[page_name] = frame
                    frame.grid(row=0, column=0, sticky="nsew")
                    frame.grid_remove()  # Hide the frame
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Frame creation warning: {e}")

    def _setup_menu(self):
        # define the top bar menu
        menu = tk.Menu(self)
        self.config(menu=menu)
        
        # sub-menu 1 = filemenu
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Select Simulation', command=self.open_simulation)
        filemenu.add_command(label='Open Configuration File', command=self.open_file_dialog)
        filemenu.add_separator()
        filemenu.add_command(label='BHTPBANK library', command=lambda: webbrowser.open(SharedVariables.bhtpbank_central_library))
        filemenu.add_separator()
        filemenu.add_command(label='Select working directory', command=self.set_working_directory)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.quit)

        # sub-menu 2 import template
        getmenu = tk.Menu(menu)
        menu.add_cascade(label='Import', menu = getmenu)
        getmenu.add_command(label= 'Text - FeederList.txt',command = lambda: SharedMethods.copy_example_files('FeederList.txt'))
        getmenu.add_command(label= 'Text - BranchList.txt',command = lambda: SharedMethods.copy_example_files('BranchList.txt'))
        getmenu.add_command(label= 'Text - BranchNodeList.txt',command = lambda: SharedMethods.copy_example_files('BranchNodeList.txt'))
        getmenu.add_command(label= 'Text - TransformerList.txt',command = lambda: SharedMethods.copy_example_files('TransformerList.txt'))
        getmenu.add_command(label= 'Text - TrainList.txt',command = lambda: SharedMethods.copy_example_files('TrainList.txt'))
        getmenu.add_command(label= 'CSV - GridAllocation.csv',command = lambda: SharedMethods.copy_example_files('GridAllocation.csv'))
        getmenu.add_command(label= 'CSV - CIF_selection.csv',command = lambda: SharedMethods.copy_example_files('CIF_selection.csv'))
        getmenu.add_command(label= 'CSV - BatchControlTemplate.csv',command = lambda: SharedMethods.copy_example_files('BatchControlTemplate.csv'))
        getmenu.add_command(label= 'Excel - (AC) For Average Power',command = lambda: SharedMethods.copy_example_files('power_template.xlsx'))
        getmenu.add_command(label= 'Excel - (AC) For IF Protection',command = lambda: SharedMethods.copy_example_files('protection_template.xlsx'))
        getmenu.add_command(label= 'Excel - (AC) For New SP Connect',command = lambda: SharedMethods.copy_example_files('new_connection_template.xlsx'))
        getmenu.add_command(label= 'Excel - (AC) For OLE Rating',command = lambda: SharedMethods.copy_example_files('ole_rating_template.xlsx'))
        getmenu.add_command(label= 'Excel - (AC) For SFC Assessment',command = lambda: SharedMethods.copy_example_files('SFC_assessment_template.xlsx'))
        getmenu.add_command(label= 'Excel - (DC) For TRU Summary',command = lambda: SharedMethods.copy_example_files('TRU_rating_template.xlsx'))
        getmenu.add_command(label= 'Excel - (DC) For Main DCCB Summary',command = lambda: SharedMethods.copy_example_files('mainCB_rating_template.xlsx'))
        getmenu.add_command(label= 'Excel - (DC) For DCBB Summary',command = lambda: SharedMethods.copy_example_files('DCBB_rating_template.xlsx'))
        getmenu.add_command(label= 'Excel - (DC) For Neg ETE Summary',command = lambda: SharedMethods.copy_example_files('NegETE_rating_template.xlsx'))
        getmenu.add_command(label= 'Excel - (DC) For Imp Bond Summary',command = lambda: SharedMethods.copy_example_files('ImpBond_rating_template.xlsx'))
        getmenu.add_command(label= 'Excel - (DC) For Track CB Summary',command = lambda: SharedMethods.copy_example_files('trackCB_rating_template.xlsx'))
        getmenu.add_command(label= 'Excel - (DC) For Pos ETE Summary',command = lambda: SharedMethods.copy_example_files('PosETE_rating_template.xlsx'))
        getmenu.add_command(label= 'Excel - (DC) For Train V Summary',command = lambda: SharedMethods.copy_example_files('trainV_template.xlsx'))
        getmenu.add_command(label= 'Excel - (DC) For Single End Feeding Analysis (TCB)',command = lambda: SharedMethods.copy_example_files('dc_single_end_feeding_template_tcb.xlsx'))
        getmenu.add_command(label= 'Excel - (DC) For Single End Feeding Analysis (Pos ETE)',command = lambda: SharedMethods.copy_example_files('dc_single_end_feeding_template_pos_ete.xlsx'))
        getmenu.add_command(label= 'Excel - (DC) For Falling Voltage Protection Analysis',command = lambda: SharedMethods.copy_example_files('dc_falling_voltage_protectoin_input_template.xlsx'))
        getmenu.add_command(label= 'Excel - For Quick BEMU Assessment',command = lambda: SharedMethods.copy_example_files('BEMU_support_capacity.xlsx'))
        getmenu.add_command(label= 'Excel - For BEMU Assessment(<RN29)',command = lambda: SharedMethods.copy_example_files('battery_train_template.xlsx'))
        getmenu.add_command(label= 'Excel - For BEMU Assessment(>RN29)',command = lambda: SharedMethods.copy_example_files('battery_train_template_new.xlsx'))
        # getmenu.add_command(label= 'Excel - For Data Input')

        # submeanu 3 osop configuration
        osopmenu = tk.Menu(menu)
        menu.add_cascade(label='OSOP Configuration', menu = osopmenu)

        self.config_var = tk.IntVar()
        self.config_var.set(3)  # Default to option 1, From sep/2024 default to 2. From June/2025 default to 3 as RN29 is released
        SharedVariables.osop_version = 3
        
        osopmenu.add_radiobutton(label='RN - 26', variable=self.config_var, value=1, command=lambda: self.osop_option_action(1))
        osopmenu.add_radiobutton(label='RN - 27 and 28', variable=self.config_var, value=2, command=lambda: self.osop_option_action(2))
        osopmenu.add_radiobutton(label='RN - 29', variable=self.config_var, value=3, command=lambda: self.osop_option_action(3))

        # sub-menu 2 = helpmenu
        helpmenu = tk.Menu(menu)
        menu.add_cascade(label='Help', menu = helpmenu)

        helpmenu.add_command(label='Help Document',command =  lambda: SharedMethods.open_support_file('VISION-OSLO Extension User Guide.pdf'))
        helpmenu.add_separator()
        helpmenu.add_command(label='Report Extension Tool Issue (Internal ONLY)',command =  lambda: webbrowser.open(SharedVariables.issue_online))
        helpmenu.add_command(label='Report VISION OSLO Issue (Internal ONLY)',command =  lambda: webbrowser.open(SharedVariables.vo_issue_online))
        helpmenu.add_separator()
        helpmenu.add_command(label='About',command = self.show_about_popup)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        # Create the frame if it doesn't exist
        if page_name not in self.frames:
            if self._frame_classes is None:
                self._frame_classes = import_frames()
            
            frame_class = self._frame_classes.get(page_name)
            if frame_class:
                frame = frame_class(parent=self._container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the requested frame
        frame = self.frames[page_name]
        frame.grid()  # Ensure the frame is shown
        frame.tkraise()

    def osop_option_action(self, version):
        """Handle OSOP version selection."""
        if version == 1:
            SharedVariables.osop_version = 1
            SharedMethods.print_message("WARNING: VISION OSLO RN26 is selected.","33")
        elif version == 2:
            SharedVariables.osop_version = 2
            SharedMethods.print_message("WARNING: VISION OSLO RN27 is selected.","33")
        elif version == 3:
            SharedVariables.osop_version = 3
            SharedMethods.print_message("WARNING: VISION OSLO RN29 is selected.","33")
        else:
            SharedMethods.print_message("ERROR: Invalid OSOP version selected.","31")
    
    def show_about_popup(self):
        about_popup = tk.Toplevel(self)
        about_popup.title("About-Copyright")

        installed_version = importlib.metadata.version(SharedVariables.package_name)
        about_text = f"VISION-OSLO extension, version {installed_version}"
        about_font = tkfont.Font(family='Helvetica', size=11, weight="bold")
        about_label = tk.Label(about_popup, text=about_text, font = about_font, padx=10, pady=10)
        about_label.pack()

        info_text = "This is Developed by Jieming Ye.\n"\
            "Copyright (c) 2024 [Jieming Ye, Engineering Services].\n"\
            f"External Link Validate: {SharedVariables.lastupdate}.\n"\
            "License: OSNCL V1.0.\n"\
            "For Support Please Consult 'traction.power@networkrail.co.uk'"
        #info_label = tk.Message(about_popup, text=info_text, aspect = 800, padx=10, pady=10)
        info_label = tk.Label(about_popup, text=info_text, padx=10, pady=10, justify="left")
        info_label.pack()

        # Center the popup window on the screen
        about_popup.geometry("+%d+%d" % (self.winfo_rootx() + self.winfo_width() // 2 - about_popup.winfo_reqwidth() // 2,
                                         self.winfo_rooty() + self.winfo_height() // 2 - about_popup.winfo_reqheight() // 2))
    
    
    def open_simulation(self):
        initial_dir = os.getcwd()
        file_path = filedialog.askopenfilename(title="Select Simulation",initialdir=initial_dir)
        if file_path:
            print(f"Selected file: {file_path}")
            file_name = os.path.basename(file_path)
            simname = ""
            # JY 2024.10: change to allow dot in simulation name
            # Check if file_name ends with any suffix in file_extensions
            for ext in SharedVariables.file_extension:
                if file_name.endswith(ext):
                    # Strip the suffix and return the name without it
                    simname = file_name[: -len(ext)]
                    break
            if simname == "":
                SharedMethods.print_message("WARNING: NOT VALID EXTENSION. FULL FILE NAME SELECTED.","33")
                simname = file_name

            print(f"Simulation Name: {simname}")
            SharedVariables.sim_variable.set(simname)
            # update the working directory to the selected file's directory
            selected_dir = os.path.dirname(file_path)
            selected_dir = os.path.normpath(selected_dir)  # normalize the path (use "\\"" instead of windows stype "/"")
            if selected_dir != os.getcwd():
                os.chdir(selected_dir)
                SharedVariables.current_path = selected_dir
                self.working_directory.set(selected_dir)
                SharedMethods.print_message(f"ATTENTION: Working directiory set to:\n{selected_dir}","33")

    
    # Create a function to be called when the "Open" menu option is clicked
    def open_file_dialog(self):
        initial_dir = os.getcwd()  # Get the current working directory
        file_path = filedialog.askopenfilename(title="Select a file",initialdir=initial_dir)
        if file_path:
            print(f"Selected file: {file_path}")

            SharedMethods.print_message("WARNING: DO NOT EXIT THE PROGRAME BEFORE SAVING THE OPENED FILE.","33")
            
            self.open_file(file_path)


    def open_file(self, file_path):
        try:
            subprocess.Popen(['start', '', file_path], shell=True,close_fds=True)
        except Exception as e:
            SharedMethods.print_message(f"ERROR: Error opening file with default app: {e}","31")

    # open the file explorer to select the working directory
    def set_working_directory(self):
        initial_dir = os.getcwd()
        print(f"Current working directory:\n{initial_dir}")
        directory_path = filedialog.askdirectory(title="Select Working Directory", initialdir=initial_dir)
        if directory_path:
            os.chdir(directory_path)
            SharedVariables.current_path = directory_path
            self.working_directory.set(directory_path)
            SharedMethods.print_message(f"WARNING: Working directiory set to:\n{directory_path}","33")
            
class StartPage(BasePage): # define another object of first page
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # adjustable fixed height for padding frame
        PADDING_HEIGHT = 160

        self.controller = controller

        self.headframe = self.create_frame(fill=tk.BOTH)
        self.nameframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1), column_weights=(1, 6))
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1), column_weights=(4, 1))
        self.infoframe = self.create_frame(fill=tk.BOTH)
        # Add padding frame between infoframe and footframe
        self.padding_frame = self.create_frame(fill=tk.BOTH)
        self.padding_frame.configure(height=PADDING_HEIGHT)  # Set fixed height
        self.footframe = self.create_frame(fill=tk.BOTH,column_weights=(1,10),side=tk.BOTTOM)

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Welcome to VISION-OSLO Add-In',font = controller.title_font)
        head.pack()
        
        text1 = tk.Label(master=self.nameframe, text = 'Simulation Name',font = controller.text_font)
        text1.grid(row = 1, column = 0 ,pady=15) # sticky n alight to top center part

        SharedVariables.sim_variable = tk.StringVar()
        entry1 = tk.Entry(master=self.nameframe,width = 40,textvariable = SharedVariables.sim_variable)
        entry1.grid(row = 1,column = 1, pady=15)

        explain1 = tk.Label(master=self.optionframe, text = 'Model Prepare: Create VISION-OSLO ready information', font = controller.text_font)
        explain1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        button1 = tk.Button(master=self.optionframe, text = 'Model Prepare', command=lambda: self.button_callback("PageOne"))
        button1.grid(row = 0, column = 1, sticky = "w", padx=5, pady=5)

        explain2 = tk.Label(master=self.optionframe, text = 'Model Check: A working VISION-OSLO model is required', font=controller.text_font)
        explain2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        button2 = tk.Button(master=self.optionframe, text = 'Model Check', command=lambda: self.button_callback("PageTwo"))
        button2.grid(row = 1, column = 1, sticky = "w", padx=5, pady=5)

        explain3 = tk.Label(master=self.optionframe, text = 'Default OSLO Extraction: A VISION-OSLO simulation result (oof) file is required',font = controller.text_font)
        explain3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)  

        button3 = tk.Button(master=self.optionframe, text = 'Result Extraction', command=lambda: self.button_callback("PageThree"))
        button3.grid(row = 2, column = 1, sticky = "w", padx=5, pady=5)

        explain4 = tk.Label(master=self.optionframe, text = 'Post Processing - General: Including improved batch extraction',font = controller.text_font)
        explain4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)  

        button4 = tk.Button(master=self.optionframe, text = 'Result Process 0', command=lambda: self.button_callback("PageFour"))
        button4.grid(row = 3, column = 1, sticky = "w", padx=5, pady=5)

        explain5 = tk.Label(master=self.optionframe, text = 'Post Processing - Mainly For AC Related Assessment',font = controller.text_font)
        explain5.grid(row = 4, column = 0, sticky = "w", padx=5, pady=5)  

        button5 = tk.Button(master=self.optionframe, text = 'Result Process 1', command=lambda: self.button_callback("PageFive"))
        button5.grid(row = 4, column = 1, sticky = "w", padx=5, pady=5)

        explain5 = tk.Label(master=self.optionframe, text = 'Post Processing - Mainly For DC Related Assessment ',font = controller.text_font)
        explain5.grid(row = 5, column = 0, sticky = "w", padx=5, pady=5)  

        button5 = tk.Button(master=self.optionframe, text = 'Result Process 2', command=lambda: self.button_callback("PageSix"))
        button5.grid(row = 5, column = 1, sticky = "w", padx=5, pady=5)

        installed_version = importlib.metadata.version(SharedVariables.package_name)
        diclaimer = tk.Label(master=self.infoframe, text = f'Version {installed_version} -- {SharedVariables.copyright}')
        diclaimer.pack()

        working_dir_identifer = tk.Label(master=self.footframe, text="Current Folder: ", font=controller.text_font)
        working_dir_identifer.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)
        working_dir_label = tk.Label(master=self.footframe, textvariable=controller.working_directory, font=controller.text_font,wraplength=550, justify="left")
        working_dir_label.grid(row = 0, column = 1, sticky = "w", padx=5, pady=5)

    def button_callback(self,target_page):
        self.get_entry_value()
        self.controller.show_frame(target_page)
    
    def get_entry_value(self):
        user_input = SharedVariables.sim_variable.get()
        if user_input:
            print(f"Simulation Name from User Input:{user_input}" )
    
# programme running
if __name__ == '__main__':
    app = SampleApp()
    app.mainloop() 
