# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 21:31:19 2016

@author: isaiahnields
"""
import Tkinter as tk
import ttk


class SettingsWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        tk.Toplevel.resizable(self,0,0)
        tk.Toplevel.title(self, "Settings")
        
        frame = tk.Frame(self, padx=5, pady=5)
        frame.grid(column=0, row=0, sticky=('nesw'))
        
        trial_time = SettingsEntry(frame, text = "Trial Time (s)")
        trial_time.grid(row=1)
        trial_time.set_text("60.0")        
        
        minimum_servo_extension = SettingsEntry(frame, text = "Minimum Servo Extension: ")
        minimum_servo_extension.grid(row =2)
        minimum_servo_extension.set_text("110.0")
        
        maximum_servo_extension = SettingsEntry(frame, text = "Maximum Servo Extension: ")
        maximum_servo_extension.set_text("35.0")
        maximum_servo_extension.grid(row=3)
        
        maximum_cue_time = SettingsEntry(frame, text = "Maximum Cue Time: ")
        maximum_cue_time.set_text("1.0")
        maximum_cue_time.grid(row=4)
        
        cue_delay_time = SettingsEntry(frame, text = "Cue Delay Time: ")
        cue_delay_time.set_text("0.5")
        cue_delay_time.grid(row=5)
        
        reward_time = SettingsEntry(frame, text = "Reward Time: ")
        reward_time.set_text(".016")
        reward_time.grid(row=6)
        
        punish_time = SettingsEntry(frame, text = "Punish Time: ")
        punish_time.set_text("5.0")
        punish_time.grid(row=7)
        
        servo_extension_time = SettingsEntry(frame, text = "Servo Extension Time: ")
        servo_extension_time.set_text("0.0")
        servo_extension_time.grid(row=8)
        
        
class SettingsEntry(tk.Frame):
    
    def __init__(self, parent, input_width = 5, sticky = 'n', text = '', padx=5, pady=5, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.label = ttk.Label(self, text=text).grid(column=1, row=1, sticky=sticky, padx=5, pady=5)
        self.string_var = tk.StringVar()
        self.entry = ttk.Entry(self, width=input_width, textvariable=self.string_var).grid(column=2, row=1, sticky=sticky, padx=5, pady=5)
        
    def set_text(self, text):
        self.string_var.set(text)
        
    def get_text(self):
        return self.string_var.get()
        
        
        
        