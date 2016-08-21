# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 10:25:15 2016

@author: isaiahnields
"""

import Tkinter as tk
import ttk
from DatabaseHandler import BoardDatabase

class ConfigureTrialWindow(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)
        
        self.resizable(0,0)
        self.title("Configure Trial")
        
        self.name_trial_frame = NameTrialFrame(self, padx=5, pady=5)
        self.name_trial_frame.grid(row=1, column=1)
        
        board_database = BoardDatabase()
        self.devices = board_database.load()
        
            
    def configure_states(self, trial_name, number_of_states):
        
        self.trial_name = trial_name
        self.number_of_states = number_of_states
        
        self.name_trial_frame.destroy()
        
        self.state_frames = []
        
        for state_frame in range(0, self.number_of_states):
            self.state_frames.append(ConfigureStateFrame(self, devices=self.devices))
        
        self.state_frames[0].grid(column=1, row=1)
        self.current_state_index = 0
        
    def next_state(self):
        if self.number_of_states - 1 != self.current_state_index:
            self.state_frames[self.current_state_index].grid_forget()
            self.current_state_index = self.current_state_index + 1
            self.state_frames[self.current_state_index].grid(column=1, row=1)
        
        
    def previous_state(self):
        if self.current_state_index != 0:
            self.state_frames[self.current_state_index].grid_forget()
            self.current_state_index = self.current_state_index - 1
            self.state_frames[self.current_state_index].grid(column=1, row=1)
            
        
            
        
        
        
class NameTrialFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        
        self.master = master
        
        ttk.Label(self, text = "Trial Name: ").grid(column=1, row=1, padx=5, pady=5)
        self.trial_name_var = tk.StringVar()
        ttk.Entry(self, width=15, textvariable=self.trial_name_var).grid(column=2, row=1, padx=5, pady=5)
        
        
        ttk.Label(self, text = "Number of States: ").grid(column=1, row=2, padx=5, pady=5)
        self.number_of_states_options = ("1","2","3","4","5","6","7","8","9","10")
        self.number_of_states_var = tk.StringVar()
        self.number_of_states_var.set(self.number_of_states_options[0])
        self.device_option_menu = tk.OptionMenu(self, self.number_of_states_var, *self.number_of_states_options)
        self.device_option_menu.grid(column=2, row=2)
        
        ttk.Button(self, text = "Next", command=self.next).grid(column=2, row=3, padx=5, pady=5)
        
    def next(self):
    
        self.trial_name = self.trial_name_var.get()
        self.number_of_states = int(self.number_of_states_var.get())
        
        self.master.configure_states(self.trial_name, self.number_of_states)
    
    
class ConfigureStateFrame(tk.Frame):
    def __init__(self, master, devices, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.master = master        
        self.devices = devices
        
        ttk.Label(self, text = "State Name: ").grid(column=1, row=1, padx=5, pady=5)
        self.state_name_var = tk.StringVar()
        ttk.Entry(self, width=15, textvariable=self.state_name_var).grid(column=2, row=1, padx=5, pady=5)

        ttk.Button(self, text = "Save States", command=self.master.previous_state).grid(column=6, row=1, padx=5, pady=5)        
        ttk.Button(self, text = "Next State", command=self.master.next_state).grid(column=5, row=1, padx=5, pady=5)
        ttk.Button(self, text = "Previous State", command=self.master.previous_state).grid(column=4, row=1, padx=5, pady=5)
        
        ttk.Label(self, text = "State Procedure: ").grid(column=1, row=2, padx=5, pady=5)
        
        ttk.Button(self, text="+", command=self.add, width=1).grid(column=2, row=2, padx=5, pady=5)
        ttk.Button(self, text="-", command=self.remove, width=1).grid(column=2, row=2, padx=5, pady=5, sticky='w')
        
        ttk.Label(self, text = "Procedure Number").grid(column=1, row=3, padx=5, pady=5)
        ttk.Label(self, text = "Device Name").grid(column=2, row=3, padx=5, pady=5)
        ttk.Label(self, text = "Delay Time").grid(column=3, row=3, padx=5, pady=5)
        ttk.Label(self, text = "Procedure").grid(column=4, row=3, padx=5, pady=5)
        ttk.Label(self, text = "Procedure Run Time").grid(column=5, row=3, padx=5, pady=5)
        ttk.Label(self, text = "End Procedure").grid(column=6, row=3, padx=5, pady=5)
        
        self.next_row = 4
        self.device_number = 1
        
        self.device_procedures = []
        
    def add(self):
        self.device_procedures.append(DeviceProcedure(self, self.devices, self.device_number, self.next_row))
        
        self.next_row = self.next_row + 1
        self.device_number = self.device_number + 1
        
    def remove(self):
        self.device_procedures[len(self.device_procedures)-1].destroy()
        self.device_procedures.pop(len(self.device_procedures)-1)
        
        self.next_row = self.next_row - 1
        self.device_number = self.device_number - 1
        
        
class DeviceProcedure():
    def __init__(self, master, devices, procedure_number, row, *args, **kwargs):
        
        self.master = master
        self.devices = devices
        self.procedure_number = procedure_number
        self.row = row
        
        self.procedure_number_label = ttk.Label(self.master, text=str(self.procedure_number))
        self.procedure_number_label.grid(column=1, row=self.row, padx=5, pady=5)
        self.device_names = []
        
        for device in self.devices:
            if device[2] != '' and device[1] != 'Lever' and device[1] != 'Infrared Beam':                
                self.device_names.append(device[2])
        self.device_names.insert(0, "None")
            
        self.device_name_options = tuple(self.device_names)
                                    
        self.device_name_var = tk.StringVar()
        self.device_name_var.set(self.device_name_options[0])
        self.device_option_menu = tk.OptionMenu(self.master, self.device_name_var, command=self.selected, *self.device_name_options)
        self.device_option_menu.grid(column=2, row=self.row, sticky='ew')
        
        self.device_extra_options = []
        
    def destroy(self):
        self.procedure_number_label.destroy()
        self.device_option_menu.destroy()
        
        try:
            for device_option in self.device_extra_options:
                device_option.destroy()
        except:
            pass
        
    def selected(self, clicked):
        self.device_name = self.device_name_var.get()
        
        try:
            for device_option in self.device_extra_options:
                if self.row == int(device_option.delay_time_entry.grid_info()['row']):
                    print self.row
                    self.device_extra_options[self.row-4].destroy()
                    self.device_extra_options.pop(self.row-4)
        except:
            pass
                
        
        for device in self.devices:
            if self.device_name == device[2]:
                self.device_type = device[1]
                if self.device_type == 'Light':
                    print self.row
                    self.device_extra_options.append(LightProcedure(self.master, self.row))
                elif self.device_type == 'Servo':
                    self.device_extra_options.append(ServoProcedure(self.master, self.row))
                elif self.device_type == 'Solenoid':
                    self.device_extra_options.append(SolenoidProcedure(self.master, self.row))
        
class LightProcedure():
    def __init__(self, master, row):
        self.master = master
        self.row = row
        
        self.delay_time_var = tk.StringVar(value=0.0)
        self.delay_time_entry = ttk.Entry(self.master, width=15, textvariable=self.delay_time_var)
        self.delay_time_entry.grid(column=3, row=self.row, padx=5, pady=5)    
        
        self.start_state_var = tk.IntVar(value=0)
        self.start_check_button = ttk.Checkbutton(self.master, text="Start State", variable=self.start_state_var)
        self.start_check_button.grid(column=4, row=self.row, padx=5, pady=5)      
        
        self.procedure_run_time_var = tk.StringVar(value=0.0)
        self.procedure_run_time_entry = ttk.Entry(self.master, width=15, textvariable=self.procedure_run_time_var)
        self.procedure_run_time_entry.grid(column=5, row=self.row, padx=5, pady=5)
        
        self.end_state_var = tk.IntVar(value=0)
        self.end_check_button = ttk.Checkbutton(self.master, text="End State", variable=self.end_state_var)
        self.end_check_button.grid(column=6, row=self.row, padx=5, pady=5)
        
    def destroy(self):
        self.delay_time_entry.destroy()
        self.start_check_button.destroy()
        self.procedure_run_time_entry.destroy()
        self.end_check_button.destroy()
        
        

class ServoProcedure():
    def __init__(self, master, row):
        self.master = master
        self.row = row
        
        self.delay_time_var = tk.StringVar(value=0.0)
        self.delay_time_entry = ttk.Entry(self.master, width=15, textvariable=self.delay_time_var)
        self.delay_time_entry.grid(column=3, row=self.row, padx=5, pady=5) 
        
        self.start_state_var = tk.DoubleVar()
        self.start_scale = tk.Scale(self.master ,orient=tk.HORIZONTAL, from_=1, to=180, length=100, variable=self.start_state_var, resolution=1)
        self.start_scale.grid(column=4, row=self.row, padx=5, pady=5)
        
        self.procedure_run_time_var = tk.StringVar()
        self.procedure_run_time_entry = ttk.Entry(self.master, width=15, textvariable=self.procedure_run_time_var)
        self.procedure_run_time_entry.grid(column=5, row=self.row, padx=5, pady=5)
        
        self.end_scale_var = tk.DoubleVar()
        self.end_scale = tk.Scale(self.master ,orient=tk.HORIZONTAL, from_=1, to=180, length=100, variable=self.end_scale_var, resolution=1)
        self.end_scale.grid(column=6, row=self.row, padx=5, pady=5)
        
    def destroy(self):
        self.delay_time_entry.destroy()
        self.start_scale.destroy()
        self.procedure_run_time_entry.destroy()
        self.end_scale.destroy()
        
class SolenoidProcedure():
    def __init__(self, master, row):
        self.master = master
        self.row = row
        
        
        self.delay_time_var = tk.StringVar(value=0.0)
        self.delay_time_entry = ttk.Entry(self.master, width=15, textvariable=self.delay_time_var)
        self.delay_time_entry.grid(column=3, row=self.row, padx=5, pady=5)    
        
        self.start_state_var = tk.IntVar(value=0)
        self.start_check_button = ttk.Checkbutton(self.master, text="Start State", variable=self.start_state_var)
        self.start_check_button.grid(column=4, row=self.row, padx=5, pady=5)      
        
        self.procedure_run_time_var = tk.StringVar(value=0.0)
        self.procedure_run_time_entry = ttk.Entry(self.master, width=15, textvariable=self.procedure_run_time_var)
        self.procedure_run_time_entry.grid(column=5, row=self.row, padx=5, pady=5)
        
        self.end_state_var = tk.IntVar(value=0)
        self.end_check_button = ttk.Checkbutton(self.master, text="End State", variable=self.end_state_var)
        self.end_check_button.grid(column=6, row=self.row, padx=5, pady=5)
        
    def destroy(self):
        self.delay_time_entry.destroy()
        self.start_check_button.destroy()
        self.procedure_run_time_entry.destroy()
        self.end_check_button.destroy()
        
    

root = tk.Tk()
ConfigureTrialWindow(root)

root.mainloop()