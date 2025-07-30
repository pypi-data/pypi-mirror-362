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
# 18/07/2024: This frame is not currenly in use in this programme
# Pending future upgrade using new frame
#=================================================================
# Set Information Variable
# N/A
#=================================================================


import tkinter as tk
from vision_oslo_extension.shared_contents import SharedMethods
from vision_oslo_extension.base_frame import BasePage

# TBC
class A01(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 14: Output to Data Files',font = controller.sub_title_font)
        head.pack()

        explain = tk.Label(master=self.headframe, text = 'Directs seveval outputs plus train summary output', font = controller.text_font)
        explain.pack()

        #button = tk.Button(master=self.excuteframe, text="RUN!", command = lambda: self.run_post_processing(),width = 20, height =2)
        button = tk.Button(master=self.excuteframe, text="RUN!", command=lambda: controller.show_frame("PageFour"),width = 20, height =2)
        button.pack()


        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFour"))
        button2.grid(row = 0, column = 1)

# TBC
class A02(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 14: Output to Data Files',font = controller.sub_title_font)
        head.pack()

        explain = tk.Label(master=self.headframe, text = 'Directs seveval outputs plus train summary output', font = controller.text_font)
        explain.pack()

        #button = tk.Button(master=self.excuteframe, text="RUN!", command = lambda: self.run_post_processing(),width = 20, height =2)
        button = tk.Button(master=self.excuteframe, text="RUN!", command=lambda: controller.show_frame("PageFour"),width = 20, height =2)
        button.pack()


        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFour"))
        button2.grid(row = 0, column = 1)


# TBC
class A03(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 14: Output to Data Files',font = controller.sub_title_font)
        head.pack()

        explain = tk.Label(master=self.headframe, text = 'Directs seveval outputs plus train summary output', font = controller.text_font)
        explain.pack()

        #button = tk.Button(master=self.excuteframe, text="RUN!", command = lambda: self.run_post_processing(),width = 20, height =2)
        button = tk.Button(master=self.excuteframe, text="RUN!", command=lambda: controller.show_frame("PageFour"),width = 20, height =2)
        button.pack()


        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageFour"))
        button2.grid(row = 0, column = 1)


