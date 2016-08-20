# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 21:25:43 2016

@author: isaiahnields
"""

import Tkinter as tk
import ttk
import UserPrompts
from DatabaseHandler import BoardDatabase


class ConfigureBoardWindow(tk.Toplevel):
    
    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)
        self.resizable(0,0)
        self.title("Configure Board")
        
        self.frame = tk.Frame(self, padx=5, pady=5)
        self.frame.grid(column = 0, row = 0, sticky = ('nesw'))
        
        
        ttk.Label(self.frame, text = "Device Pin").grid(column=1, row=1, padx=5, pady=5)
        ttk.Label(self.frame, text = "Device Type").grid(column=2, row=1, padx=5, pady=5)
        ttk.Label(self.frame, text = "Device Name").grid(column=3, row=1, padx=5, pady=5)
        
        ttk.Button(self.frame, text = "Save Board", command=self.save_board_alert).grid(column=3, row=13, padx=5, pady=5)

        self.device_frame_list = []
        
        for pin_number in range(2, 13):
            self.device_frame_list.append(DeviceFrame(self.frame, self, pin_number, pin_number))
            
        self.database = BoardDatabase()
        self.load_board()
            
    def save_board(self, clicked=None):
        
        self.device_list = []
        self.device_name_list = []
        self.save_error = False
        
        
        for device_frame in self.device_frame_list:
            self.device_list.append([str(device_frame.pin_number), device_frame.device_type_var.get(), device_frame.device_name_var.get()])
            if device_frame.device_name_var.get() != '':
                self.device_name_list.append(device_frame.device_name_var.get())
            
            
        for device in self.device_list:
            if device[1] == 'None' and device[2] != '':
                self.save_error = True
                UserPrompts.show_error("Error", "Pin " + str(device[0]) + " name needed")
            if device[1] != 'None' and device[2] == '':
                self.save_error = True
                UserPrompts.show_error("Error", "Pin " + str(device[0]) + " type needed")
            
    
        if len(self.device_name_list) != len(set(self.device_name_list)):
            self.save_error = True
            UserPrompts.show_error("Error", "Devices must have unique names")
            
            
        elif not self.save_error:

            self.database.save(self.device_list)
            self.board_saved = True
        
    def save_board_alert(self, clicked=None):
        self.save_board()
        if not self.save_error == True:  
            UserPrompts.show_info("Success", "Board Saved: Please unplug board and plug in again")
        
    def load_board(self):
        self.device_list = self.database.load()
        for device_frame, device in zip(self.device_frame_list, self.device_list):
            device_frame.device_type_var.set(device[1])
            device_frame.device_name_var.set(device[2])
        
class DeviceFrame():
    def __init__(self, master_frame, master_window, row, pin_number):
        
        self.master_frame = master_frame
        self.master_window = master_window
        self.row = row
        self.pin_number = pin_number
        
        ttk.Label(self.master_frame, text="Pin " + str(self.pin_number)).grid(column=1, row=self.row, padx=5, pady=5)
        
        self.device_type_options = ("None",
                                    "Infrared Beam",
                                    "Lever",
                                    "Light",
                                    "Servo",
                                    "Solenoid")
                                    
        self.device_type_var = tk.StringVar(self.master_frame)
        self.device_type_var.set(self.device_type_options[0])
        self.device_option_menu = tk.OptionMenu(self.master_frame, self.device_type_var, *self.device_type_options)
        self.device_option_menu.grid(column=2, row=self.pin_number)
        
        self.device_name_var = tk.StringVar(self.master_frame)
        ttk.Entry(self.master_frame, width=15, textvariable=self.device_name_var).grid(column=3, row=self.row, padx=5, pady=5)
        
        
