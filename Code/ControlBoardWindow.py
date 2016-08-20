# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 21:12:25 2016

@author: isaiahnields
"""

import Tkinter as tk
import ttk

class ControlBoardWindow(tk.Toplevel):
    def __init__(self, master, devices, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)
        
        self.resizable(0,0)
        self.title("Manual Controls")
        
        self.devices = devices
        
        self.frame = tk.Frame(self, padx=5, pady=5)
        self.frame.grid(column=0, row=0)
    
        self.device_controllers = {}
        
        
        self.next_row = 1
        
        for device in self.devices:
            self.type = self.devices[device].type
            self.pin_number = self.devices[device].pin_number
            self.device = self.devices[device]
                
            if self.type == "Light":
                self.device_controllers[device[0]] = LightController(method=self.device.toggle, frame=self.frame, row=self.pin_number, device_name=device, pin_number=self.pin_number)
                self.next_row += 1
            elif self.type == "Solenoid":
                self.device_controllers[device] = SolenoidController(method=self.device.toggle, frame=self.frame, row=self.pin_number, device_name=device, pin_number=self.pin_number)
                self.next_row += 1
            elif self.type == "Servo":
                self.device_controllers[device] = ServoController(method=[self.device.write, self.device.read], frame=self.frame, row=self.pin_number, device_name=device, pin_number=self.pin_number)
                self.next_row += 1
            elif self.type == "Lever":
                self.device_controllers[device] = LeverController(method=self.device.read, frame=self.frame, row=self.pin_number, device_name=device, pin_number=self.pin_number)
                self.next_row += 1
            elif self.type == "Infrared Beam":
                self.device_controllers[device] = InfraredBeamController(method=self.device.read, frame=self.frame, row=self.pin_number, device_name=device, pin_number=self.pin_number)
        self.iterate_methods = []
        
        for device_controller in self.device_controllers:
            self.controller_type = self.device_controllers[device_controller].type
            
            if "Lever" in self.controller_type or "Infrared" in self.controller_type:
                self.iterate_methods.append(self.device_controllers[device_controller].iterate)
                
        while True:
            master.update()
            for method in self.iterate_methods:
                method()
        
            
class DeviceController():
    def __init__(self, frame, method, row=int, device_name =str, pin_number=int, *args, **kwargs):
        
        self.frame = frame
        self.method = method
        self.row = row
        self.device_name = device_name
        self.pin_number = str(pin_number)
        
        self.device_pin_label = ttk.Label(self.frame, text="Pin " + self.pin_number).grid(column=1, row=self.row, padx=5, pady=5)
        self.device_name_label = ttk.Label(self.frame, text=self.device_name).grid(column=2, row=self.row, padx=5, pady=5)
        
        
class LightController(DeviceController):
    def __init__(self, off_value=0.0, on_value=1.0, *args, **kwargs):
        DeviceController.__init__(self, *args, **kwargs)
        
        self.type = "Light Controller"
        
        self.off_value = off_value
        self.on_value = on_value
        
        self.state_var = tk.IntVar(value=0)
        self.check_button = ttk.Checkbutton(self.frame, text="State", command=self.method, variable=self.state_var).grid(column=3, row=self.row, padx=5, pady=5)
            
    

class ServoController(DeviceController):
    def __init__(self, minimum=1.0, maximum=180.0, length=180, resolution=1.0, *args, **kwargs):
        DeviceController.__init__(self, *args, **kwargs)
        
        self.type = "Servo Controller"
        
        self.minimum = minimum
        self.maximum = maximum
        self.length = length
        self.resolution = resolution
        
        self.scale_var = tk.DoubleVar(value=self.method[1]())
        self.scale = tk.Scale(self.frame ,orient=tk.HORIZONTAL, from_=self.minimum, to=self.maximum, length=self.length, variable=self.scale_var, resolution=self.resolution, command=self.method[0]).grid(column=3, row=self.row, padx=5, pady=5)


class SolenoidController(DeviceController):
    def __init__(self, init_value=0.0, off_value=0.0, on_value=1.0, *args, **kwargs):
        DeviceController.__init__(self, *args, **kwargs)
        
        self.type = "Solenoid Controller"
        
                
        self.off_value = off_value
        self.on_value = on_value
        
        self.state_var = tk.IntVar(value=0)
        self.check_button = ttk.Checkbutton(self.frame, text="State", command=self.method, variable=self.state_var).grid(column=3, row=self.row, padx=5, pady=5)

        

class LeverController(DeviceController):
    def __init__(self, *args, **kwargs):
        DeviceController.__init__(self, *args, **kwargs)
        
        self.type = "Lever Controller"
        
        self.state_var = tk.StringVar(value="Resting")
        ttk.Label(self.frame, textvariable=self.state_var).grid(column=3, row=self.row, padx=5, pady=5)
        
    def iterate(self):
        self.state = self.method()
        
        if self.state == True:
            self.state_var.set("Pressed")
        elif self.state == False:
            self.state_var.set("Resting")
    
class InfraredBeamController(DeviceController):
    def __init__(self, *args, **kwargs):
        DeviceController.__init__(self, *args, **kwargs)
        
        self.type = "Infrared Beam Controller"
        
        self.state_var = tk.StringVar(value="Resting")
        ttk.Label(self.frame, textvariable=self.state_var).grid(column=3, row=self.row, padx=5, pady=5)
        
    def iterate(self):
        self.state = self.method()
        if self.state == True:
            self.state_var.set("Broken")
        elif self.state == False:
            self.state_var.set("Resting")