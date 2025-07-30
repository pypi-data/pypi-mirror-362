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
2nd windows based on user selection.
Description:
This script defines the GUI for 2nd window based on user selection. This could guide people to proper location based on detailed user requirements.
The maximum number of option list for this version is 14.

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
#=================================================================
# Set Information Variable
# N/A
#=================================================================


import tkinter as tk

from vision_oslo_extension.shared_contents import SharedVariables
from vision_oslo_extension.base_frame import BasePage

# Redundency Page
# Model Check Page
class Page0(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.headframe = self.create_frame(fill=tk.BOTH)
        self.dirframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1))
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), column_weights=(4, 1))
        self.infoframe = self.create_frame(fill=tk.BOTH)

        label = tk.Label(master=self.headframe, text = 'TO BE DEVELOPED',font = controller.sub_title_font)
        label.pack(side="top", fill="x", pady=2)

        note = tk.Label(master=self.headframe, text = 'THIS PAGE IS TO BE DEVELOPED IN FUTURE...',font = controller.text_font)
        note.pack(side="top", fill="x", pady=5)

        button = tk.Button(self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady = 5)


    def set_main_option(self,value,target_page):
        SharedVariables.main_option = value
        self.controller.show_frame(target_page)

# Input Support Page
class PageOne(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.headframe = self.create_frame(fill=tk.BOTH)
        self.dirframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1))
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), column_weights=(4, 1))
        self.infoframe = self.create_frame(fill=tk.BOTH)

        label = tk.Label(master=self.headframe, text = 'VISION OSLO Model Data Preparation',font = controller.sub_title_font)
        label.pack(side="top", fill="x", pady=2)

        note = tk.Label(master=self.headframe, text = 'Instruction: User expected to have relavent technical data ready.',font = controller.text_font)
        note.pack(side="left", fill="x", pady=5)

        explain1 = tk.Label(master=self.optionframe, text = '1. BHTPBANK File Creation / Check', font = controller.text_font)
        explain1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=2)

        button1 = tk.Button(master=self.optionframe, text = 'execute 1', command=lambda: self.set_main_option("1","S01"))
        button1.grid(row = 0, column = 1, sticky = "w", padx=5, pady=2)

        explain2 = tk.Label(master=self.optionframe, text = '2: OSLO Impedance Spreadsheet', font = controller.text_font)
        explain2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=2)

        button2 = tk.Button(master=self.optionframe, text = 'execute 2', command=lambda: self.set_main_option("2","S02"))
        button2.grid(row = 1, column = 1, sticky = "w", padx=5, pady=2)

        explain3 = tk.Label(master=self.optionframe, text = '3: Extra.OSLO / Extra.Bat.OSLO Preparation', font = controller.text_font)
        explain3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=2)

        button3 = tk.Button(master=self.optionframe, text = 'execute 3', command=lambda: self.set_main_option("3","S03"))
        button3.grid(row = 2, column = 1, sticky = "w", padx=5, pady=2)

        explain4 = tk.Label(master=self.optionframe, text = '4: Timetable Input Support / CIF Support', font = controller.text_font)
        explain4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=2)

        button4 = tk.Button(master=self.optionframe, text = 'execute 4', command=lambda: self.set_main_option("4","S04"))
        button4.grid(row = 3, column = 1, sticky = "w", padx=5, pady=2)

        explain5 = tk.Label(master=self.optionframe, text = '5: CIF Import Analysis / Model Improvement Guidance', font = controller.text_font)
        explain5.grid(row = 4, column = 0, sticky = "w", padx=5, pady=2)

        button5 = tk.Button(master=self.optionframe, text = 'execute 5', command=lambda: self.set_main_option("5","S05"))
        button5.grid(row = 4, column = 1, sticky = "w", padx=5, pady=2)

        explain6 = tk.Label(master=self.optionframe, text = '6: Provision for development', font = controller.text_font)
        explain6.grid(row = 5, column = 0, sticky = "w", padx=5, pady=2)

        button6 = tk.Button(master=self.optionframe, text = 'execute 6', command=lambda: self.set_main_option("6","S06"))
        button6.grid(row = 5, column = 1, sticky = "w", padx=5, pady=2)


        button = tk.Button(self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady = 5)


    def set_main_option(self,value,target_page):
        SharedVariables.main_option = value
        self.controller.show_frame(target_page)

# Model Check Page
class PageTwo(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.headframe = self.create_frame(fill=tk.BOTH)
        self.dirframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1))
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), column_weights=(4, 1))
        self.infoframe = self.create_frame(fill=tk.BOTH)

        label = tk.Label(master=self.headframe, text = 'OSLO Model Check / Verification',font = controller.sub_title_font)
        label.pack(side="top", fill="x", pady=2)

        note = tk.Label(master=self.headframe, text = 'Instruction: User expected solve all VISION Model and can click Run to OSLO diagnose page to proceed.',font = controller.text_font)
        note.pack(side="left", fill="x", pady=5)

        explain1 = tk.Label(master=self.optionframe, text = '1. OSLO Information Listing', font = controller.text_font)
        explain1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=2)

        button1 = tk.Button(master=self.optionframe, text = 'execute 1', command=lambda: self.set_main_option("1","C01"))
        button1.grid(row = 0, column = 1, sticky = "w", padx=5, pady=2)

        explain2 = tk.Label(master=self.optionframe, text = '2: Connectivity Report', font = controller.text_font)
        explain2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=2)

        button2 = tk.Button(master=self.optionframe, text = 'execute 2', command=lambda: self.set_main_option("2","C02"))
        button2.grid(row = 1, column = 1, sticky = "w", padx=5, pady=2)

        explain3 = tk.Label(master=self.optionframe, text = '3: Network Map Auto Creation', font = controller.text_font)
        explain3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=2)

        button3 = tk.Button(master=self.optionframe, text = 'execute 3', command=lambda: self.set_main_option("3","C03"))
        button3.grid(row = 2, column = 1, sticky = "w", padx=5, pady=2)

        explain4 = tk.Label(master=self.optionframe, text = '4: Simulation Batch Run', font = controller.text_font)
        explain4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=2)

        button4 = tk.Button(master=self.optionframe, text = 'execute 4', command=lambda: self.set_main_option("4","C04"))
        button4.grid(row = 3, column = 1, sticky = "w", padx=5, pady=2)

        button = tk.Button(self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady = 5)

    def set_main_option(self,value,target_page):
        SharedVariables.main_option = value
        self.controller.show_frame(target_page)

# OSLO Extraction Page
class PageThree(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.headframe = self.create_frame(fill=tk.BOTH)
        # self.timeframe = self.create_frame(fill=tk.BOTH, column_weights=(2, 1, 2, 1))
        self.dirframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1))
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), column_weights=(4, 1))
        self.infoframe = self.create_frame(fill=tk.BOTH)

        label = tk.Label(master=self.headframe, text = 'OSLO Extraction Option Selection',font = controller.sub_title_font)
        label.pack(side="top", fill="x", pady=2)

        note = tk.Label(master=self.headframe, text = 'Instruction: User can go to info page entering extraction requirements using execute buttons below',font = controller.text_font)
        note.pack(side="left", fill="x", pady=5)

        # extraction user interface
        explain1 = tk.Label(master=self.optionframe, text = '1. List of electrical files', font = controller.text_font)
        explain1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=2)

        button1 = tk.Button(master=self.optionframe, text = 'execute 1', command=lambda: self.set_main_option("1","F01"))
        button1.grid(row = 0, column = 1, sticky = "w", padx=5, pady=2)

        explain2 = tk.Label(master=self.optionframe, text = '2: Snapshot', font = controller.text_font)
        explain2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=2)

        button2 = tk.Button(master=self.optionframe, text = 'execute 2', command=lambda: self.set_main_option("2","F02"))
        button2.grid(row = 1, column = 1, sticky = "w", padx=5, pady=2)

        explain3 = tk.Label(master=self.optionframe, text = '3: Individual train step output', font = controller.text_font)
        explain3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=2)

        button3 = tk.Button(master=self.optionframe, text = 'execute 3', command=lambda: self.set_main_option("3","F03"))
        button3.grid(row = 2, column = 1, sticky = "w", padx=5, pady=2)

        explain4 = tk.Label(master=self.optionframe, text = '4: Maximum currents and minimum and maximum voltages', font = controller.text_font)
        explain4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=2)

        button4 = tk.Button(master=self.optionframe, text = 'execute 4', command=lambda: self.set_main_option("4","F04"))
        button4.grid(row = 3, column = 1, sticky = "w", padx=5, pady=2)

        explain5 = tk.Label(master=self.optionframe, text = '5: Train high voltage summary', font = controller.text_font)
        explain5.grid(row = 4, column = 0, sticky = "w", padx=5, pady=2)

        button5 = tk.Button(master=self.optionframe, text = 'execute 5', command=lambda: self.set_main_option("5","F05"))
        button5.grid(row = 4, column = 1, sticky = "w", padx=5, pady=2)

        explain6 = tk.Label(master=self.optionframe, text = '6: Train low voltage summary', font = controller.text_font)
        explain6.grid(row = 5, column = 0, sticky = "w", padx=5, pady=2)

        button6 = tk.Button(master=self.optionframe, text = 'execute 6', command=lambda: self.set_main_option("6","F06"))
        button6.grid(row = 5, column = 1, sticky = "w", padx=5, pady=2)

        explain7 = tk.Label(master=self.optionframe, text = '7: Average MW and MVAr demands in supply points, metering points, static VAr, etc', font = controller.text_font)
        explain7.grid(row = 6, column = 0, sticky = "w", padx=5, pady=2)

        button7 = tk.Button(master=self.optionframe, text = 'execute 7', command=lambda: self.set_main_option("7","F07"))
        button7.grid(row = 6, column = 1, sticky = "w", padx=5, pady=2)

        explain8 = tk.Label(master=self.optionframe, text = '8: Feeder step output', font = controller.text_font)
        explain8.grid(row = 7, column = 0, sticky = "w", padx=5, pady=2)

        button8 = tk.Button(master=self.optionframe, text = 'execute 8', command=lambda: self.set_main_option("8","F08"))
        button8.grid(row = 7, column = 1, sticky = "w", padx=5, pady=2)

        explain9 = tk.Label(master=self.optionframe, text = '9: Branch step output', font = controller.text_font)
        explain9.grid(row = 8, column = 0, sticky = "w", padx=5, pady=2)

        button9 = tk.Button(master=self.optionframe, text = 'execute 9', command=lambda: self.set_main_option("9","F09"))
        button9.grid(row = 8, column = 1, sticky = "w", padx=5, pady=2)

        explain10 = tk.Label(master=self.optionframe, text = '10: Transformer step output', font = controller.text_font)
        explain10.grid(row = 9, column = 0, sticky = "w", padx=5, pady=2)

        button10 = tk.Button(master=self.optionframe, text = 'execute 10', command=lambda: self.set_main_option("10","F10"))
        button10.grid(row = 9, column = 1, sticky = "w", padx=5, pady=2)

        explain11 = tk.Label(master=self.optionframe, text = '11: Smoothed feeder currents', font = controller.text_font)
        explain11.grid(row = 10, column = 0, sticky = "w", padx=5, pady=2)

        button11 = tk.Button(master=self.optionframe, text = 'execute 11', command=lambda: self.set_main_option("11","F11"))
        button11.grid(row = 10, column = 1, sticky = "w", padx=5, pady=2)

        explain12 = tk.Label(master=self.optionframe, text = '12: Smoothed branch currents', font = controller.text_font)
        explain12.grid(row = 11, column = 0, sticky = "w", padx=5, pady=2)

        button12 = tk.Button(master=self.optionframe, text = 'execute 12', command=lambda: self.set_main_option("12","F12"))
        button12.grid(row = 11, column = 1, sticky = "w", padx=5, pady=2)

        explain13 = tk.Label(master=self.optionframe, text = '13: Supply point persistent currents (development in progress)', font = controller.text_font)
        explain13.grid(row = 12, column = 0, sticky = "w", padx=5, pady=2)

        button13 = tk.Button(master=self.optionframe, text = 'execute 13', command=lambda: self.set_main_option("13","F13"))
        button13.grid(row = 12, column = 1, sticky = "w", padx=5, pady=2)

        explain14 = tk.Label(master=self.optionframe, text = '14: Output to data files', font = controller.text_font)
        explain14.grid(row = 13, column = 0, sticky = "w", padx=5, pady=2)

        button14 = tk.Button(master=self.optionframe, text = 'execute 14', command=lambda: self.set_main_option("14","F14"))
        button14.grid(row = 13, column = 1, sticky = "w", padx=5, pady=2)


        button = tk.Button(self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady = 5)

    def set_main_option(self,value,target_page):
        SharedVariables.main_option = value
        self.controller.show_frame(target_page)

# OSLO Post Processing page - General
class PageFour(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        self.headframe = self.create_frame(fill=tk.BOTH)
        self.dirframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1))
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), column_weights=(4, 1))
        self.infoframe = self.create_frame(fill=tk.BOTH)

        label = tk.Label(master=self.headframe, text = 'OSLO Post-Processing Option Selection - General',font = controller.sub_title_font)
        label.pack(side="top", fill="x", pady=2)

        note = tk.Label(master=self.headframe, text = 'Instruction: User can go to info page entering processing requirements using execute buttons below',font = controller.text_font)
        note.pack(side="left", fill="x", pady=5)

        explain1 = tk.Label(master=self.optionframe, text = '1. AC & DC: List OSLO Train Data', font = controller.text_font)
        explain1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=2)

        button1 = tk.Button(master=self.optionframe, text = 'execute 1', command=lambda: self.set_main_option("1","P01"))
        button1.grid(row = 0, column = 1, sticky = "w", padx=5, pady=2)

        explain2 = tk.Label(master=self.optionframe, text = '2: AC & DC: Low Voltage Analysis Report', font = controller.text_font)
        explain2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=2)

        button2 = tk.Button(master=self.optionframe, text = 'execute 2', command=lambda: self.set_main_option("2","P02"))
        button2.grid(row = 1, column = 1, sticky = "w", padx=5, pady=2)

        explain3 = tk.Label(master=self.optionframe, text = '3. AC & DC: Battery Train Assessment Support', font = controller.text_font)
        explain3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=2)

        button3 = tk.Button(master=self.optionframe, text = 'execute 3', command=lambda: self.set_main_option("1","P13"))
        button3.grid(row = 2, column = 1, sticky = "w", padx=5, pady=2)

        explain14 = tk.Label(master=self.optionframe, text = '4: To be developed', font = controller.text_font)
        explain14.grid(row = 3, column = 0, sticky = "w", padx=5, pady=2)

        button14 = tk.Button(master=self.optionframe, text = 'execute 4', command=lambda: self.set_main_option("14","Page0"))
        button14.grid(row = 3, column = 1, sticky = "w", padx=5, pady=2)

        button = tk.Button(self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady = 5)


    def set_main_option(self,value,target_page):
        SharedVariables.main_option = value
        self.controller.show_frame(target_page)

# OSLO Post Processing page - AC
class PageFive(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.headframe = self.create_frame(fill=tk.BOTH)
        self.dirframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1))
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), column_weights=(4, 1))
        self.infoframe = self.create_frame(fill=tk.BOTH)

        label = tk.Label(master=self.headframe, text = 'OSLO Post-Processing Option Selection - Mainly AC',font = controller.sub_title_font)
        label.pack(side="top", fill="x", pady=2)

        note = tk.Label(master=self.headframe, text = 'Instruction: User can go to info page entering processing requirements using execute buttons below',font = controller.text_font)
        note.pack(side="left", fill="x", pady=5)

        explain3 = tk.Label(master=self.optionframe, text = '1: AC: Average Power & Voltage Assessment (Minimum Requirement)', font = controller.text_font)
        explain3.grid(row = 0, column = 0, sticky = "w", padx=5, pady=2)

        button3 = tk.Button(master=self.optionframe, text = 'execute 1', command=lambda: self.set_main_option("3","P03"))
        button3.grid(row = 0, column = 1, sticky = "w", padx=5, pady=2)

        explain4 = tk.Label(master=self.optionframe, text = '2: AC: Meanuseful Processing (BSEN 50388:2022 Annex B)', font = controller.text_font)
        explain4.grid(row = 1, column = 0, sticky = "w", padx=5, pady=2)

        button4 = tk.Button(master=self.optionframe, text = 'execute 2', command=lambda: self.set_main_option("4","P04"))
        button4.grid(row = 1, column = 1, sticky = "w", padx=5, pady=2)

        explain5 = tk.Label(master=self.optionframe, text = '3: AC: Incoming Feeder Protection (Suggest use for IDMT Protection)', font = controller.text_font)
        explain5.grid(row = 2, column = 0, sticky = "w", padx=5, pady=2)

        button5 = tk.Button(master=self.optionframe, text = 'execute 3', command=lambda: self.set_main_option("5","P05"))
        button5.grid(row = 2, column = 1, sticky = "w", padx=5, pady=2)

        explain6 = tk.Label(master=self.optionframe, text = '4: AC: New Supply Point Connection Assessment (Grid Code Compliance)', font = controller.text_font)
        explain6.grid(row = 3, column = 0, sticky = "w", padx=5, pady=2)

        button6 = tk.Button(master=self.optionframe, text = 'execute 4', command=lambda: self.set_main_option("6","P06"))
        button6.grid(row = 3, column = 1, sticky = "w", padx=5, pady=2)

        explain7 = tk.Label(master=self.optionframe, text = '5: AC: OLE Current Rating Assessment', font = controller.text_font)
        explain7.grid(row = 4, column = 0, sticky = "w", padx=5, pady=2)

        button7 = tk.Button(master=self.optionframe, text = 'execute 5', command=lambda: self.set_main_option("7","P07"))
        button7.grid(row = 4, column = 1, sticky = "w", padx=5, pady=2)

        explain8 = tk.Label(master=self.optionframe, text = '6: AC: Static Frequency Converter SFC Assessment', font = controller.text_font)
        explain8.grid(row = 5, column = 0, sticky = "w", padx=5, pady=2)

        button8 = tk.Button(master=self.optionframe, text = 'execute 6', command=lambda: self.set_main_option("8","P08"))
        button8.grid(row = 5, column = 1, sticky = "w", padx=5, pady=2)

        explain1 = tk.Label(master=self.optionframe, text = '7. To be developed', font = controller.text_font)
        explain1.grid(row = 6, column = 0, sticky = "w", padx=5, pady=2)

        button1 = tk.Button(master=self.optionframe, text = 'execute 7', command=lambda: self.set_main_option("1","Page0"))
        button1.grid(row = 6, column = 1, sticky = "w", padx=5, pady=2)

        explain2 = tk.Label(master=self.optionframe, text = '8: To be developed', font = controller.text_font)
        explain2.grid(row = 7, column = 0, sticky = "w", padx=5, pady=2)

        button2 = tk.Button(master=self.optionframe, text = 'execute 8', command=lambda: self.set_main_option("2","Page0"))
        button2.grid(row = 7, column = 1, sticky = "w", padx=5, pady=2)

        button = tk.Button(self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady = 5)


    def set_main_option(self,value,target_page):
        SharedVariables.main_option = value
        self.controller.show_frame(target_page)

# OSLO Post Processing page - DC
class PageSix(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.headframe = self.create_frame(fill=tk.BOTH)
        self.dirframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1))
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), column_weights=(4, 1))
        self.infoframe = self.create_frame(fill=tk.BOTH)

        label = tk.Label(master=self.headframe, text = 'OSLO Post-Processing Option Selection - Mainly DC',font = controller.sub_title_font)
        label.pack(side="top", fill="x", pady=2)

        note = tk.Label(master=self.headframe, text = 'Instruction: User can go to info page entering processing requirements using execute buttons below',font = controller.text_font)
        note.pack(side="left", fill="x", pady=5)

        explain9 = tk.Label(master=self.optionframe, text = '1: DC: (DATA PREP.) For Grid, TRU, Main CB, DC Busbar, Neg ETE, Bonding Assessment', font = controller.text_font)
        explain9.grid(row = 0, column = 0, sticky = "w", padx=5, pady=2)

        button9 = tk.Button(master=self.optionframe, text = 'execute 1', command=lambda: self.set_main_option("9","P09"))
        button9.grid(row = 0, column = 1, sticky = "w", padx=5, pady=2)

        explain10 = tk.Label(master=self.optionframe, text = '2: DC (DATA PREP.): For Track CB, Pos ETE Assessment', font = controller.text_font)
        explain10.grid(row = 1, column = 0, sticky = "w", padx=5, pady=2)

        button10 = tk.Button(master=self.optionframe, text = 'execute 2', command=lambda: self.set_main_option("10","P10"))
        button10.grid(row = 1, column = 1, sticky = "w", padx=5, pady=2)

        explain12 = tk.Label(master=self.optionframe, text = '3: DC: (Data PREP. and Assessment) Single End Feeding', font = controller.text_font)
        explain12.grid(row = 2, column = 0, sticky = "w", padx=5, pady=2)

        button12 = tk.Button(master=self.optionframe, text = 'execute 3', command=lambda: self.set_main_option("12","P12"))
        button12.grid(row = 2, column = 1, sticky = "w", padx=5, pady=2)
        
        explain13 = tk.Label(master=self.optionframe, text = '4: DC (Data PREP. and Assessment) Falling Voltage Protection', font = controller.text_font)
        explain13.grid(row = 3, column = 0, sticky = "w", padx=5, pady=2)

        button13 = tk.Button(master=self.optionframe, text = 'execute 4', command=lambda: self.set_main_option("13","P14"))
        button13.grid(row = 3, column = 1, sticky = "w", padx=5, pady=2)

        explain11 = tk.Label(master=self.optionframe, text = '5: DC (Assessment): Generate All Assessment Summary Reports', font = controller.text_font)
        explain11.grid(row = 4, column = 0, sticky = "w", padx=5, pady=2)

        button11 = tk.Button(master=self.optionframe, text = 'execute 5', command=lambda: self.set_main_option("11","P11"))
        button11.grid(row = 4, column = 1, sticky = "w", padx=5, pady=2)

        explain1 = tk.Label(master=self.optionframe, text = '6. To be developed', font = controller.text_font)
        explain1.grid(row = 5, column = 0, sticky = "w", padx=5, pady=2)

        button1 = tk.Button(master=self.optionframe, text = 'execute 6', command=lambda: self.set_main_option("1","Page0"))
        button1.grid(row = 5, column = 1, sticky = "w", padx=5, pady=2)

        explain2 = tk.Label(master=self.optionframe, text = '7: To be developed', font = controller.text_font)
        explain2.grid(row = 6, column = 0, sticky = "w", padx=5, pady=2)

        button2 = tk.Button(master=self.optionframe, text = 'execute 7', command=lambda: self.set_main_option("2","Page0"))
        button2.grid(row = 6, column = 1, sticky = "w", padx=5, pady=2)

        explain3 = tk.Label(master=self.optionframe, text = '8: To be developed', font = controller.text_font)
        explain3.grid(row = 7, column = 0, sticky = "w", padx=5, pady=2)

        button3 = tk.Button(master=self.optionframe, text = 'execute 8', command=lambda: self.set_main_option("3","Page0"))
        button3.grid(row = 7, column = 1, sticky = "w", padx=5, pady=2)


        button = tk.Button(self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady = 5)


    def set_main_option(self,value,target_page):
        SharedVariables.main_option = value
        self.controller.show_frame(target_page)
