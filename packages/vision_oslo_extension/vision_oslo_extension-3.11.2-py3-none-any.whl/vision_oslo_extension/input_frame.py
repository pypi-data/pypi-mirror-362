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
Detailed windows based on user selection.
Description:
This script defines individual input preparation option in a new class object following logic stated in section 4.1.
Note that due to the complexity of some input data preparation. Some method is considered more suitable to be edited in excel environment. If excel name is to be changed in the future, this script needs to be updated accordingly.


"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
# V1.1 (Jieming Ye) 03/10/2024: Add another option in CIF process
#=================================================================
# Set Information Variable
# N/A
#=================================================================


import tkinter as tk

from vision_oslo_extension.shared_contents import SharedMethods
from vision_oslo_extension.base_frame import BasePage

# BHTPBANK SUPPORT
class S01(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 1: BHTPBANK Creation /  Check',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'BHTPBANK File Creator (excel) is still in use to support very customised traction profile creation. The checking process is for information only and should be treated with caution.',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Option 1 - Import BHTPBANK Creator and Follow Excel Instructions',font = controller.text_font)
        explain1.pack()

        explain4 = tk.Label(master=self.headframe, text = 'NOTE: Option 2 - Import Battery BHTPBANK File Creator and Follow Excel Instructions.', font = controller.text_font)
        explain4.pack()

        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Option 3 - Ensure BHTPBANK file exist in the current path',font = controller.text_font)
        explain2.pack()

        explain3 = tk.Label(master=self.headframe, text = 'WARNING: Option 3 will freeze this window once RUN due to Plotting Function Limitation.', font = controller.text_font)
        explain3.pack()

        choice1 = tk.Label(master=self.optionframe, text = 'Option 1: BHTPBANK Traction File Creator',font = controller.text_font)
        choice1.grid(row = 0, column = 0, sticky = "w", padx= 10, pady=5)

        filename = 'bhtpbank_file_creator.xlsm'
        button1 = tk.Button(master=self.optionframe, text="Import Traction Creator",command = lambda: SharedMethods.copy_example_files(filename),width = 20, height =1)
        button1.grid(row = 1, column = 0, sticky = "w", padx= 10, pady=5)

        choice3 = tk.Label(master=self.optionframe, text = 'Option 2: BHTPBANK Battery File Creator',font = controller.text_font)
        choice3.grid(row = 2, column = 0, sticky = "w", padx= 10, pady=5)

        filename1 = 'battery_bhtpbank_file_creator.xlsm'
        button3 = tk.Button(master=self.optionframe, text="Import Battery Creator",command = lambda: SharedMethods.copy_example_files(filename1),width = 20, height =1)
        button3.grid(row = 3, column = 0, sticky = "w", padx= 10, pady=5)

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: Traction BHTPBANK File Check (No Interactive Window)',value="1", variable=option1)
        choice2.grid(row = 4, column = 0, sticky = "w", padx= 5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: Traction BHTPBANK File Check (Keep Interactive Window)',value="2", variable=option1)
        choice4.grid(row = 5, column = 0, sticky = "w", padx= 5, pady=5)

        label01 = tk.Label(master=self.inputframe, text = 'BHTPBANK Name:',font = controller.text_font)
        label01.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry01 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry01.grid(row = 0,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_excel_select(input3),width = 10, height =1)
        button_select.grid(row = 0, column = 2, sticky = "w", padx=2, pady=2)
        
        label1 = tk.Label(master=self.inputframe, text = 'Car Number (1-12): ',font = controller.text_font)
        label1.grid(row = 1, column = 0, sticky = "w", padx=2, pady=2)

        input1 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry1 = tk.Entry(master=self.inputframe,width = 10,textvariable = input1)
        entry1.grid(row = 1,column = 1)

        label2 = tk.Label(master=self.inputframe, text = '(Freight Loco Enter 1)',font = controller.text_font)
        label2.grid(row = 1, column = 2, sticky = "w", padx=2, pady=2)

        # input2 = tk.StringVar() # Initialize with a value not used by the radio buttons
        # entry2 = tk.Entry(master=self.inputframe,width = 10,textvariable = input2)
        # entry2.grid(row = 1,column = 3)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "bhtpbank_check.py",
                option_select = option1,
                text_input = input3,
                time_step = input1,
                independent_process=True,  # Run in a separate process
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Input", command=lambda: controller.show_frame("PageOne"))
        button2.grid(row = 0, column = 1)

# OSLO Impedance Calculation
class S02(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 2: OSLO Branch Impedance',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'User is expected to work from a excel template due to the complexity of information involved.',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Pending future support.', font = controller.text_font)
        explain1.pack()

        choice1 = tk.Label(master=self.optionframe, text = 'Option 1: AC Model',font = controller.text_font)
        choice1.grid(row = 0, column = 0, sticky = "w", padx= 10, pady=5)

        filename = 'ac_oslo_section_impedance.xlsx'
        button1 = tk.Button(master=self.optionframe, text="Import AC Spreadsheet",command = lambda: SharedMethods.copy_example_files(filename),width = 20, height =1)
        button1.grid(row = 1, column = 0, sticky = "w", padx= 10, pady=5)

        choice2 = tk.Label(master=self.optionframe, text = 'Option 2: DC Model',font = controller.text_font)
        choice2.grid(row = 2, column = 0, sticky = "w", padx= 10, pady=5)

        filename2 = 'dc_oslo_section_impedance.xlsx'
        button2 = tk.Button(master=self.optionframe, text="Import DC Spreadsheet",command = lambda: SharedMethods.copy_example_files(filename2),width = 20, height =1)
        button2.grid(row = 3, column = 0, sticky = "w", padx= 10, pady=5)
        

        # button = tk.Button(master=self.excuteframe, text="RUN!", command = lambda: self.run_model_check(),width = 20, height =2)
        # button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Input", command=lambda: controller.show_frame("PageOne"))
        button2.grid(row = 0, column = 1)

# Extra.OSLO and Extra.Bat.OSLO Support
class S03(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 3: Extra.OSLO and Extra.Bat.OSLO Creator',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This support the creating of Extra.OSLO and Extra.Bat.OSLO file. Excel creator is recommended due to the complexity of information involved. ',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Pending Future Support',font = controller.text_font)
        explain1.pack()

        choice1 = tk.Label(master=self.optionframe, text = 'Option 1: AC Extra Oslo Creator',font = controller.text_font)
        choice1.grid(row = 0, column = 0, sticky = "w", padx= 10, pady=5)

        filename = 'ac_extra_oslo_creator.xlsm'
        button1 = tk.Button(master=self.optionframe, text="Import AC Creator",command = lambda: SharedMethods.copy_example_files(filename),width = 20, height =1)
        button1.grid(row = 1, column = 0, sticky = "w", padx= 10, pady=5)

        choice2 = tk.Label(master=self.optionframe, text = 'Option 2: DC Extra Oslo Creator',font = controller.text_font)
        choice2.grid(row = 2, column = 0, sticky = "w", padx= 10, pady=5)

        filename2 = 'dc_extra_oslo_creator.xlsm'
        button2 = tk.Button(master=self.optionframe, text="Import DC Creator",command = lambda: SharedMethods.copy_example_files(filename2),width = 20, height =1)
        button2.grid(row = 3, column = 0, sticky = "w", padx= 10, pady=5)

        choice3 = tk.Label(master=self.optionframe, text = 'Option 3: Extra Battery Oslo Creator',font = controller.text_font)
        choice3.grid(row = 4, column = 0, sticky = "w", padx= 10, pady=5)

        filename3 = 'extra_bat_oslo_creator.xlsm'
        button3 = tk.Button(master=self.optionframe, text="Import Battery Extra.bat.OSLO Creator",command = lambda: SharedMethods.copy_example_files(filename3),width = 30, height =1)
        button3.grid(row = 5, column = 0, sticky = "w", padx= 10, pady=5)

        # button = tk.Button(master=self.excuteframe, text="RUN!", command = lambda: self.run_bhtp_check(input1,input3),width = 20, height =2)
        # button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Input", command=lambda: controller.show_frame("PageOne"))
        button2.grid(row = 0, column = 1)

# Timetable / CIF Support
class S04(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 4: CIF Timetable Support',font = controller.sub_title_font)
        head.pack()

        explain = tk.Label(master=self.headframe, text = 'This will do some pre-CIF analysing and fitering', font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: Option 3-7 requires a csv file called "CIF_selection.csv".', font = controller.text_font)
        explain1.pack()

        explain2 = tk.Label(master=self.headframe, text = 'NOTE: "CIF_selection.csv" template can be imported from Import menu.', font = controller.text_font)
        explain2.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: Readable Format Output (CIF Checking)', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: Filter out / Remove Diesel Services (FOR CIF IMPORT)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: Select Trains Passing Specific TIPLOC - [REQUIRE: CIF_selection.csv]', value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: Select Specific TOC Code - [REQUIRE: CIF_selection.csv]', value="4", variable=option1)
        choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        choice5 = tk.Radiobutton(master=self.optionframe, text = 'Option 5: Select Specific Train (as per CIF train sequence) - [REQUIRE: CIF_selection.csv]', value="5", variable=option1)
        choice5.grid(row = 4, column = 0, sticky = "w", padx=5, pady=5)

        choice6 = tk.Radiobutton(master=self.optionframe, text = 'Option 6: Remove Specific TIPLOC (Use with caution) - [REQUIRE: CIF_selection.csv]', value="6", variable=option1)
        choice6.grid(row = 5, column = 0, sticky = "w", padx=5, pady=5)

        choice7 = tk.Radiobutton(master=self.optionframe, text = 'Option 7: Remove Specific Platform INFO only at a TIPLOC (Use with caution) - [REQUIRE: CIF_selection.csv]', value="7", variable=option1)
        choice7.grid(row = 6, column = 0, sticky = "w", padx=5, pady=5)

        label01 = tk.Label(master=self.inputframe, text = 'CIF File Name (FULL):',font = controller.text_font)
        label01.grid(row = 0, column = 0, sticky = "w", padx=2, pady=2)

        input3 = tk.StringVar() # Initialize with a value not used by the radio buttons
        entry01 = tk.Entry(master=self.inputframe,width = 10,textvariable = input3)
        entry01.grid(row = 0,column = 1)

        button_select = tk.Button(master=self.inputframe, text="Select", command = lambda: self.auto_file_select(input3),width = 10, height =1)
        button_select.grid(row = 0, column = 2, sticky = "w", padx=2, pady=2)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "cif_prepare.py",
                option_select=option1,
                text_input=input3
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Input", command=lambda: controller.show_frame("PageOne"))
        button2.grid(row = 0, column = 1)


# CIF Import Support
class S05(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 5: CIF Import Support / Model Improvement Guidance',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This will generate a model improvement guidance report based on the importing process. This should be run multiple rounds to improve the CIF import quality.',aspect = 1200, font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: The following files are required.', font = controller.text_font)
        explain1.pack()

        explain2 = tk.Label(master=self.headframe, text = 'NOTE: simulation.gd', font = controller.text_font)
        explain2.pack()

        explain3 = tk.Label(master=self.headframe, text = 'NOTE: simulation.C2V.routes.txt', font = controller.text_font)
        explain3.pack()

        explain4 = tk.Label(master=self.headframe, text = 'NOTE: simulation.routes.mon.txt', font = controller.text_font)
        explain4.pack()

        explain5 = tk.Label(master=self.headframe, text = 'NOTE: simulation.routes.itf.txt', font = controller.text_font)
        explain5.pack()

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "cif_output_analysis.py",
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Input", command=lambda: controller.show_frame("PageOne"))
        button2.grid(row = 0, column = 1)
    

# CIF Import Support
class S06(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 6: Provision for development',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'To be developed.',aspect = 1200, font = controller.text_font)
        explain.pack()

        button = tk.Button(master=self.excuteframe, text="RUN!", command=lambda: controller.show_frame("PageOne"),width = 20, height =2)
        button.pack()


        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Input", command=lambda: controller.show_frame("PageOne"))
        button2.grid(row = 0, column = 1)