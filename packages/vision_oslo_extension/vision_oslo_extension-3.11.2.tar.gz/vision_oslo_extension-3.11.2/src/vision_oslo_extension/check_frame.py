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
This script defines individual checking option in a new ‘class’ object following logic stated in section 4.1.

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

# Basic Information Summary
class C01(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 1: Basic Information Summary',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This will produce various summary reports inlcuding branch list, supply point list, transformer list and errors or warnings summary. This process should be fairly quick.',aspect = 1200, font = controller.text_font)
        explain.pack()

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "model_check.py",
                option_select="1",
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Check", command=lambda: controller.show_frame("PageTwo"))
        button2.grid(row = 0, column = 1)

# Connectivity
class C02(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 2: Connectivity Report',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This will produce two summaries. One showing the node connection summary. One showing all connected nodes from the supply points.',aspect = 1200, font = controller.text_font)
        explain.pack()

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "model_check.py",
                option_select="2",
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Check", command=lambda: controller.show_frame("PageTwo"))
        button2.grid(row = 0, column = 1)

# Plotting
class C03(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 3: Network Connection Plot',font = controller.sub_title_font)
        head.pack()

        explain = tk.Label(master=self.headframe, text = 'This will create a plot (A3 Picture format) of the OSLO network.', font = controller.text_font)
        explain.pack()

        explain1 = tk.Label(master=self.headframe, text = 'NOTE: AC Network Plot is Regulated (Option 1 and 2).', font = controller.text_font)
        explain1.pack()

        explain3 = tk.Label(master=self.headframe, text = 'NOTE: DC Network Plot is Random (Option 3). Different plots each run.', font = controller.text_font)
        explain3.pack()
        
        explain2 = tk.Label(master=self.headframe, text = 'WARNING: This process will freeze this window once RUN due to Plotting Function Limitation.', font = controller.text_font)
        explain2.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Option 1: AC OSLO Network Plotting (NOT show Branch ID)', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        choice2 = tk.Radiobutton(master=self.optionframe, text = 'Option 2: AC OSLO Network Plotting (Show Branch ID)',value="2", variable=option1)
        choice2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        choice3 = tk.Radiobutton(master=self.optionframe, text = 'Option 3: DC OSLO Network Plotting (Random Gen, To Be Improved)', value="3", variable=option1)
        choice3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)

        # choice4 = tk.Radiobutton(master=self.optionframe, text = 'Option 4: TO BE DECIDED', value="4", variable=option1)
        # choice4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)

        button = tk.Button(
            master=self.excuteframe, 
            text="RUN!", 
            command=lambda: self.run_new_thread_or_process(
                "model_check.py",
                option_select="3",
                text_input=option1,
                independent_process=True,  # Run in a separate process
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Check", command=lambda: controller.show_frame("PageTwo"))
        button2.grid(row = 0, column = 1)


# Batch Simulation Running Control
class C04(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 4: Batch Simulation Running',font = controller.sub_title_font)
        head.pack()

        explain = tk.Label(master=self.headframe, text = 'This support automatically running of multiple simulations.', font = controller.text_font)
        explain.pack()

        explain1 = tk.Message(master=self.headframe, text = 'Note that this supports from VISION RN-28 onwards. Once the process started, user could stop the process by shutting down the VISION model directly.',aspect = 1200, font = controller.text_font)
        explain1.pack()

        explain2 = tk.Label(master=self.headframe, text = 'NOTE: Import "BatchControlTemplate.csv" to start.', font = controller.text_font)
        explain2.pack()
        
        explain3 = tk.Label(master=self.headframe, text = 'WARNING: This process takes time and the extension tool cannot be used for other purpose once running.', font = controller.text_font)
        explain3.pack()

        option1 = tk.StringVar(value = "0") # Initialize with a value not used by the radio buttons
        choice1 = tk.Radiobutton(master=self.optionframe, text = 'Only ONE option available for this version.', value="1", variable=option1)
        choice1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

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
                "simulation_batch_run.py",
                option_select=option1,
                text_input=input3,
                independent_process=True,  # Run in a separate process
            ),
            width=20, 
            height=2
        )
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Check", command=lambda: controller.show_frame("PageTwo"))
        button2.grid(row = 0, column = 1)
