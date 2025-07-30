#
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
base_frame.py
Used Input:
N/A
Expected Output:
Detailed windows based on user selection
Description:
This script defines individual processing option in a new ‘class’ object following logic stated in section 4.1.

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
#=================================================================
# Set Information Variable
# N/A
#=================================================================

import tkinter as tk
from vision_oslo_extension.shared_contents import SharedMethods
from vision_oslo_extension.base_frame import BasePage

# List OSLO Train Data
class P01(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 1: List OSLO Train Data',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This will produce a step output of all OSLO trains within the simulation. User could copy and paste the information to a Excel --> data convert to table using space as seperator --> analysis and plot as required.',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain0 = tk.Label(master=self.headframe, text = 'NOTE: OPTION 3 and 4 require a Branch List text file (User Defined Name Allowed)',font = controller.text_font)
        explain0.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: List all trains step output from the simulation', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: List all trains step output From Start to End (Time information below required)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: List all trains step output of selected branches for the whole simulation window', value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: List all trains step output of selected branches From Start to End (Time information below required)', value="4", variable=option1)
        choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        label0 = tk.Label(master=self.inputframe, text = 'Option 2 and Option 3 requires Info Below',font = controller.text_font)
        label0.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 1,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 1, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 1,column = 3)

        label3 = tk.Label(master=self.inputframe, text = 'Option 3 and Option 4 requires Info Below',font = controller.text_font)
        label3.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        label4 = tk.Label(master=self.inputframe, text = 'Customised Branch File Name',font = controller.text_font)
        label4.grid(row = 3, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry3 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry3.grid(row = 3,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 3, column = 2, sticky = "w", padx=2, pady=2)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "post_processing.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                text_input = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFour"))
        button2.grid(row = 0, column = 1)


# Low Voltage Analysis Report
class P02(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 2: Low Voltage Analysis',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This will produce three tables (csv files). Table list will cover all trains step output where the voltage is below the threshold. Summary table 1 will provide summary report group by trains. Summary table 2 will provide summary report group by branches.',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: OPTION 3 and 4 require a Branch List text file (User Defined Name Allowed)',font = controller.text_font)
        explain1.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Processing whole simulation', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Processing customised time window (Time information below required)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: Processing customised branches (Branch info below required)', value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: Processing customised branches during customised time window (2&3)', value="4", variable=option1)
        choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        label3 = tk.Label(master=self.optionframe, text = 'VOLTAGE THRESHOLD IS REQUIRED FOR ALL OPTIONS',font = controller.text_font)
        label3.grid(row = 4, column = 0, sticky = "w", padx=2, pady=2)
        
        label6 = tk.Label(master=self.inputframe, text = 'Low Voltage Threshold (max 5 digit):',font = controller.text_font)
        label6.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)

        input4 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry4 = tk.Entry(master=self.inputframe,width = 10,textvariable = input4)
        entry4.grid(row = 1,column = 1)

        label7 = tk.Label(master=self.inputframe, text = 'Range [0 - 30000], Unit (V)',font = controller.text_font)
        label7.grid(row = 1, column = 2, sticky = "w", padx=2, pady=2)

        label1 = tk.Label(master=self.inputframe, text = 'Output From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 2,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Output To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 2,column = 3)

        label4 = tk.Label(master=self.inputframe, text = 'Customised Branch File Name',font = controller.text_font)
        label4.grid(row = 3, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry3 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry3.grid(row = 3,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 3, column = 2, sticky = "w", padx=2, pady=2)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "post_processing.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                text_input = input3,
                low_v = input4,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFour"))
        button2.grid(row = 0, column = 1)

# One stop AC power prepare
class P03(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 3: AC - Supply Points Load Analysis - Average Power',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This function requires the excel spreadsheet with proper pre-defined information. See manual for detailed requirements',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Excel spreadsheet in .xlsx format is required before click RUN',font = controller.text_font)
        explain1.pack()
        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Import "Excel - For Average Power" if needed ',font = controller.text_font)
        explain2.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Full Auto Process. (Require .oof + .lst.txt files.)', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Auto process with user defined node configuration. (Only require .oof file)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: Update spreadsheet only. (Require all .d4 files and .mxn files)', value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: Extract d4 files and mxn file only. (Only require .oof file)', value="4", variable=option1)
        choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        label01 = tk.Label(master=self.inputframe, text = 'Excel Name:',font = controller.text_font)
        label01.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry01 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry01.grid(row = 0,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 0, column = 2, sticky = "w", padx=2, pady=2)

        label02 = tk.Label(master=self.inputframe, text = 'Below required for Option 1,2,4',font = controller.text_font)
        label02.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)
        
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 2,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 2,column = 3)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "average_load.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                text_input = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFive"))
        button2.grid(row = 0, column = 1)

# Umean useful Analysis
class P04(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 4: Umeanuseful',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This will produce a text file stating the Umean useful (ZONE) for the selected geographical section and list of Umeanuseful (TRAIN) in ascending order. User needs to make sensible choice of Trains for the assessment.',aspect = 1200, font = controller.text_font)
        explain.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Processing whole time window (Suggest for Umean (TRAIN))', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Processing customised time window (Suggest for Umean (Zone), Umean (Train) still whole time window)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        explain1 = tk.Label(master=self.optionframe, text = 'NOTE: Branch List File should define the assessed geographic range.',font = controller.text_font)
        explain1.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)
        

        label4 = tk.Label(master=self.inputframe, text = 'Branch File Name (Required):',font = controller.text_font)
        label4.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry3 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry3.grid(row = 0,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 0, column = 2, sticky = "w", padx=2, pady=2)

        label1 = tk.Label(master=self.inputframe, text = 'Peak time From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 1,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Peak time To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 1, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 1,column = 3)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "post_processing.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                text_input = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFive"))
        button2.grid(row = 0, column = 1)


# Incoming Feeder Protection
class P05(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 5: AC - Incoming Feeder Protection',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This function is used to carry out prelimiary assessment on incoming feeder protection based on relay type (DT or IDMT). This function requires the excel spreadsheet with proper pre-defined information. See manual for detailed requirements',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Excel spreadsheet in .xlsx format is required before click RUN',font = controller.text_font)
        explain1.pack()
        
        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Import "Excel - For IF Protection" if needed ',font = controller.text_font)
        explain2.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Full Auto Process. (Require .oof files)', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Update Spreadsheet only. (Require all .d4 files)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        label01 = tk.Label(master=self.inputframe, text = 'Excel Name:',font = controller.text_font)
        label01.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry01 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry01.grid(row = 0,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 0, column = 2, sticky = "w", padx=2, pady=2)

        label02 = tk.Label(master=self.inputframe, text = 'Below required for Option 1',font = controller.text_font)
        label02.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 2,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 2,column = 3)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "protection_if.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                text_input = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFive"))
        button2.grid(row = 0, column = 1)


# New Grid Connection Assessment
class P06(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 6: AC - New Supply Point Connection Assessment',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This function is used to carry out new supply point assessment as required by Grid Code. This function requires the excel spreadsheet with proper pre-defined information. See manual for detailed requirements',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Excel spreadsheet in .xlsx format is required before click RUN',font = controller.text_font)
        explain1.pack()
        
        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Import "Excel - For New SP Connect" if needed ',font = controller.text_font)
        explain2.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Full Auto Process. (Require .oof files)', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Update Spreadsheet only. (Require extracted .d4 files)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        label01 = tk.Label(master=self.inputframe, text = 'Excel Name:',font = controller.text_font)
        label01.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry01 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry01.grid(row = 0,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 0, column = 2, sticky = "w", padx=2, pady=2)

        label02 = tk.Label(master=self.inputframe, text = 'Below required for Option 1',font = controller.text_font)
        label02.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 2,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 2,column = 3)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "grid_connection.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                text_input = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFive"))
        button2.grid(row = 0, column = 1)


# OLE Rating Assessment
class P07(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 7: AC - OLE Current Rating Assessment',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This function is used to carry out OLE current rating assessment. This function requires the excel spreadsheet with proper pre-defined information. See manual for detailed requirements',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Excel spreadsheet in .xlsx format is required before click RUN',font = controller.text_font)
        explain1.pack()
        
        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Import "Excel - For OLE Rating" if needed ',font = controller.text_font)
        explain2.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Full Auto Process. (Require .oof files)', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Update Spreadsheet only. (Require extracted .d4 files)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        label01 = tk.Label(master=self.inputframe, text = 'Excel Name:',font = controller.text_font)
        label01.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry01 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry01.grid(row = 0,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 0, column = 2, sticky = "w", padx=2, pady=2)

        label02 = tk.Label(master=self.inputframe, text = 'Below required for Option 1',font = controller.text_font)
        label02.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 2,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 2,column = 3)
        
        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "ole_processing.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                text_input = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFive"))
        button2.grid(row = 0, column = 1)


# Static Frequence Converter
class P08(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 8: AC - Static Frequency Converter SFC Assessment',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This function requires the excel spreadsheet with proper pre-defined information. See manual for detailed requirements',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Excel spreadsheet in .xlsx format is required before click RUN',font = controller.text_font)
        explain1.pack()
        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Import "Excel - For SFC" if needed ',font = controller.text_font)
        explain2.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Full Auto Process. (Require .oof + .lst.txt files.)', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Auto process with user defined node configuration. (Only require .oof file)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: Update spreadsheet only. (Require all .d4 files and .mxn files)', value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: Extract d4 files and mxn file only. (Only require .oof file)', value="4", variable=option1)
        choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        label01 = tk.Label(master=self.inputframe, text = 'Excel Name:',font = controller.text_font)
        label01.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry01 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry01.grid(row = 0,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 0, column = 2, sticky = "w", padx=2, pady=2)

        label02 = tk.Label(master=self.inputframe, text = 'Below required for Option 1,2,4',font = controller.text_font)
        label02.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)
        
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 2,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 2,column = 3)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "sfc_assess.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                text_input = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFive"))
        button2.grid(row = 0, column = 1)


# Substation TRU assessment
class P09(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 9: Substation TRU Assessment Data Prepare',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This will produce multiple .d4 files from extraction and .csv files for each substation. A substation list named as "FeederList.txt" is required.',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: "FeederList.txt" is required before click RUN',font = controller.text_font)
        explain1.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Substation RMS current (1,4,5,30,60,120,180 min) and average power (30 min)', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Grid Calculation (require "GridAllocation.csv" file)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        label0 = tk.Label(master=self.inputframe, text = 'Enter Assessment Time Window',font = controller.text_font)
        label0.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 1,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 1, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 1,column = 3)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "batch_processing.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageSix"))
        button2.grid(row = 0, column = 1)


# Substation Branch Process
class P10(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 10: Substation Protection/Track CB & ETE Assessment Data Prepare',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This will produce multiple .csv files depending on the option selection. Option 2 is used to prepare data for report assessment',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Time Window is COMPULSORY.',font = controller.text_font)
        explain1.pack()

        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Option 3 or 6 should be chosen for DC assessment.',font = controller.text_font)
        explain2.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: All branches (Auto) step output summary', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: All branches (Auto) rolling RMS current calculation',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: All branches (Auto) maximum rolling RMS current summary', value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: Customised branches step output summary ("BranchNodeList.txt"is required)', value="4", variable=option1)
        choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        choice5 = tk.Radiobutton(master=self.optionframe, text = 'Option 5: Customised branches rolling RMS current calculation ("BranchNodeList.txt"is required)', value="5", variable=option1)
        choice5.grid(row = 4, column = 0, sticky = "w", padx=5, pady=5)

        choice6 = tk.Radiobutton(master=self.optionframe, text = 'Option 6: Customised branches maximum rolling RMS current summary ("BranchNodeList.txt"is required)', value="6", variable=option1)
        choice6.grid(row = 5, column = 0, sticky = "w", padx=5, pady=5)

        label0 = tk.Label(master=self.inputframe, text = 'Enter Assessment Time Window',font = controller.text_font)
        label0.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 1,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 1, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 1,column = 3)

        label3 = tk.Label(master=self.inputframe, text = 'Time Seconds (0 - 86400):',font = controller.text_font)
        label3.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry3 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry3.grid(row = 2,column = 1)

        label4 = tk.Label(master=self.inputframe, text = '(Note this is time in seconds)',font = controller.text_font)
        label4.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "batch_processing.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                time_step = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageSix"))
        button2.grid(row = 0, column = 1)


# Substation DC Summary
class P11(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 11: DC Substation Assessment Summary',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This will produce assessment summary against ratings for all scenarios. User is expected to set some presettings in a spreadsheet. A setting excel required.',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Excel spreadsheet in .xlsx format is required before click RUN.',font = controller.text_font)
        explain1.pack()

        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Import proper excel as required Below if needed.',font = controller.text_font)
        explain2.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: TRU Summary - [Import: Excel - For TRU Summary if needed]', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Main DC Circuit Breaker Summary - [Import: Excel - For Main DCCB Summary if needed]',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: DC Busbar Summary - [Import: Excel - For DCBB Summary if needed]',value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: Negative ETE Summary - [Import: Excel - For Neg ETE Summary if needed]',value="4", variable=option1)
        choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        choice5 = tk.Radiobutton(master=self.optionframe, text = 'Option 5: Impedance Bond Summary - [Import: Excel - For Imp Bond Summary if needed]',value="5", variable=option1)
        choice5.grid(row = 4, column = 0, sticky = "w", padx=5, pady=5)

        choice6 = tk.Radiobutton(master=self.optionframe, text = 'Option 6: Track Circuit Breaker Summary - [Import: Excel - For Track CB Summary if needed]',value="6", variable=option1)
        choice6.grid(row = 5, column = 0, sticky = "w", padx=5, pady=5)

        choice7 = tk.Radiobutton(master=self.optionframe, text = 'Option 7: Positive ETE Summary - [Import: Excel - Pos ETE Summary if needed]',value="7", variable=option1)
        choice7.grid(row = 6, column = 0, sticky = "w", padx=5, pady=5)

        choice8 = tk.Radiobutton(master=self.optionframe, text = 'Option 8: Train Min Voltage Summary - [Import: Excel - Train V Summary if needed]',value="8", variable=option1)
        choice8.grid(row = 7, column = 0, sticky = "w", padx=5, pady=5)


        label01 = tk.Label(master=self.inputframe, text = 'Excel Name:',font = controller.text_font)
        label01.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry01 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry01.grid(row = 0,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 0, column = 2, sticky = "w", padx=2, pady=2)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "dc_summary.py",
                option_select = option1,
                text_input = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageSix"))
        button2.grid(row = 0, column = 1)


# DC Single End Feeding 1st Stage Processing
class P12(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 12: DC Single End Feeding 1st Stage Processing',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This option will generate Single End Feeding loads by adding the loads of both ends of a branch to get an estimate. This is used for 1st stage Single End Feeding analysis. List file will be automatically generated if it does not already exist. Excel Spreadsheet containing ratings and branch names is required.',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Time Window is COMPULSORY. Excel spreadsheet in .xlsx format is required before click RUN.',font = controller.text_font)
        explain1.pack()

        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Option 3 and 4 are for generating step results in CSV format in addition to results summary,', font = controller.text_font)
        explain2.pack()

        explain3 = tk.Label(master=self.headframe, text = 'results summary will be avalaible in the chosen spreadsheet in all options.', font = controller.text_font)
        explain3.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Track Circuit Breaker (TCB) Assessment, 15min RMS used.', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: ETE (Positive Cables) Assessment, 30min RMS used.',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: Track Circuit Breaker (TCB) Assessment, 15min RMS used. With CSV step outputs', value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: ETE (Positive Cables) Assessment, 30min RMS used. With CSV step outputs', value="4", variable=option1)
        choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        #choice5 = tk.Radiobutton(master=self.optionframe, text = 'Option 5: Customised branches rolling RMS current calculation ("BranchNodeList.txt"is required)', value="5", variable=option1)
        #choice5.grid(row = 4, column = 0, sticky = "w", padx=5, pady=5)

        #choice6 = tk.Radiobutton(master=self.optionframe, text = 'Option 6: Customised branches maximum rolling RMS current summary ("BranchNodeList.txt"is required)', value="6", variable=option1)
        #choice6.grid(row = 5, column = 0, sticky = "w", padx=5, pady=5)

        label0 = tk.Label(master=self.inputframe, text = 'Enter Assessment Time Window',font = controller.text_font)
        label0.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 1,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 1, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 1,column = 3)

        #label3 = tk.Label(master=self.inputframe, text = 'Time Seconds (0 - 86400):',font = controller.text_font)
        #label3.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        #input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        #entry3 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        #entry3.grid(row = 2,column = 1)

        #label4 = tk.Label(master=self.inputframe, text = '(Note this is time in seconds)',font = controller.text_font)
        #label4.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        label3 = tk.Label(master=self.inputframe, text = 'Excel Name:',font = controller.text_font)
        label3.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry3 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry3.grid(row = 2,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "dc_single_end_feeding.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                text_input = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageSix"))
        button2.grid(row = 0, column = 1)


# Battery EMU Assessment
class P13(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 13: Battery EMU Assessment',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This function requires the excel spreadsheet with proper pre-defined information. See manual for detailed requirements',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Excel spreadsheet in .xlsx format is required before click RUN',font = controller.text_font)
        explain1.pack()
        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Option 1 & 2 require "Import "Excel - For Quick BEMU Assessment" if needed ',font = controller.text_font)
        explain2.pack()
        explain21 = tk.Label(master=self.headframe, text = 'NOTE: Option 3 & 4 require "Import "Excel - For BEMU Assessment (<RN29)" if needed ',font = controller.text_font)
        explain21.pack()
        explain22 = tk.Label(master=self.headframe, text = 'NOTE: Option 5 require "Import "Excel - For BEMU Assessment (>RN29)" if needed ',font = controller.text_font)
        explain22.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Preliminary Assessment (Import Excel - For Quick BEMU Assessment). (Only require .oof file)', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Update spreadsheet only (Import Excel - For Quick BEMU Assessment). (Require all .d4 files)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: Detailed Modelling Auto Assessment (Import Excel - For BEMU Assessment(<RN29)). (Only require .oof file)', value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: Update spreadsheet only (Import Excel - For BEMU Assessment(<RN29)). (Require all .ds1 files)',value="4", variable=option1)
        choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        choice5 = tk.Radiobutton(master=self.optionframe, text = 'Option 5: New BEMU Assessment (Import Excel - For BEMU Assessment(>RN29)).(Require .battery.txt file)',value="5", variable=option1)
        choice5.grid(row = 4, column = 0, sticky = "w", padx=5, pady=5)

        label01 = tk.Label(master=self.inputframe, text = 'Excel Name:',font = controller.text_font)
        label01.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry01 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry01.grid(row = 0,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 0, column = 2, sticky = "w", padx=2, pady=2)

        label02 = tk.Label(master=self.inputframe, text = 'Below required for Option 1 and Option 3',font = controller.text_font)
        label02.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 2,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 2,column = 3)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "battery_processing.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                text_input = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFour"))
        button2.grid(row = 0, column = 1)


# DC Falling Voltage Protection Processing
class P14(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 14: DC Falling Voltage Protection (FVP) Processing and Assessment',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This option will assess TCBs with FVP by extracting the step voltage/current results and compare them agaist FVP curves. Excel Spreadsheet containing FVP ratings and branch names is required. There is an option to extract all step results with plotted graphs',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: NOTE: Time Window is COMPULSORY. Excel spreadsheet in .xlsx format is required before click RUN. ',font = controller.text_font)
        explain1.pack()

        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Option 3 or 4 to skip OSOP extraction, if OSOP extraction has already been done for all branches', font = controller.text_font)
        explain2.pack()

        explain3 = tk.Label(master=self.headframe, text = 'NOTE: Option 2 and 4 are for generating step results and scatter graphs in addition to results summary,', font = controller.text_font)
        explain3.pack()

        explain4 = tk.Label(master=self.headframe, text = 'Results summary will be avalaible in the chosen spreadsheet in all options.', font = controller.text_font)
        explain4.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: FVP assessment with OSOP extraction', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: FVP assessment with OSOP extraction, with scatter plots and step results',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: FVP assessment ONLY', value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: FVP assessment ONLY, with scatter plots and step results', value="4", variable=option1)
        choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        #choice5 = tk.Radiobutton(master=self.optionframe, text = 'Option 5: Customised branches rolling RMS current calculation ("BranchNodeList.txt"is required)', value="5", variable=option1)
        #choice5.grid(row = 4, column = 0, sticky = "w", padx=5, pady=5)

        #choice6 = tk.Radiobutton(master=self.optionframe, text = 'Option 6: Customised branches maximum rolling RMS current summary ("BranchNodeList.txt"is required)', value="6", variable=option1)
        #choice6.grid(row = 5, column = 0, sticky = "w", padx=5, pady=5)

        label0 = tk.Label(master=self.inputframe, text = 'Enter Assessment Time Window',font = controller.text_font)
        label0.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)
        
        label1 = tk.Label(master=self.inputframe, text = 'Extraction From (Format: DHHMMSS)',font = controller.text_font)
        label1.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 1,column = 1)

        label2 = tk.Label(master=self.inputframe, text = 'Extraction To (Format: DHHMMSS)',font = controller.text_font)
        label2.grid(row = 1, column = 2, sticky = "w", padx=2, pady=2)

        input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        entry2.grid(row = 1,column = 3)

        #label3 = tk.Label(master=self.inputframe, text = 'Time Seconds (0 - 86400):',font = controller.text_font)
        #label3.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        #input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        #entry3 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        #entry3.grid(row = 2,column = 1)

        #label4 = tk.Label(master=self.inputframe, text = '(Note this is time in seconds)',font = controller.text_font)
        #label4.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        label3 = tk.Label(master=self.inputframe, text = 'Excel Name:',font = controller.text_font)
        label3.grid(row = 2, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry3 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry3.grid(row = 2,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 2, column = 2, sticky = "w", padx=2, pady=2)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "dc_falling_voltage_protection.py",
                time_start = input1,
                time_end = input2,
                option_select = option1,
                text_input = input3,
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFour"))
        button2.grid(row = 0, column = 1)
