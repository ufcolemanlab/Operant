# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 22:05:55 2016

@author: isaiahnields
"""

from pyfirmata import Arduino, util, serial
import serial.tools.list_ports
import UserPrompts
import time

class BoardHandler():
    def __init__(self, device_list=list, record_board=True):
        
        self.device_list = device_list
        self.record_board = record_board
        
        self.board_booted = False
    
    def boot(self):
        self.board = Board(device_list=self.device_list, record_board=self.record_board)
        self.board_booted = True
    
    def exit(self):
        if self.board_booted == True:            
            self.board.exit()

class Board(Arduino):
    
    def __init__(self, device_list=list, record_board=True, *args, **kwargs):
        
        self.record_board = record_board
        self.device_list = device_list
                
        try:
            
            self.ports = list(serial.tools.list_ports.comports())
            
            for port in self.ports:
                if "Arduino" in port[1] or "Generic" in port[1]:
                    self.aruindo_port = port[0]
                
            Arduino.__init__(self, self.aruindo_port, *args, **kwargs)
            it = util.Iterator(self)
            it.start()
            self.analog[0].enable_reporting()
                        
            self.board_connected = True          
            
        except serial.SerialException, e:
            UserPrompts.show_error("Serial Exception", "Could not open port: " + str(e))
        
        except AttributeError, e:
            UserPrompts.show_error("Attribute Error", "Board not plugged in: " + str(e))
            
        if self.board_connected:
            
            self.devices = {}
            
            if self.record_board:
                self.recordings = []
            
            for device in self.device_list:
                print device
                if device[1] == "None":
                    pass
                elif device[1] == "Light":
                    self.devices[device[2]] = Light(board=self, device_type=device[1], pin_number=device[0], device_name=device[2])
                elif device[1] == "Solenoid":
                    self.devices[device[2]] = Solenoid(board=self, device_type=device[1], pin_number=device[0], device_name=device[2])
                elif device[1] == "Servo":
                    self.devices[device[2]] = Servo(board=self, device_type=device[1], pin_number=device[0], device_name=device[2])
                elif device[1] == "Lever":
                    self.devices[device[2]] = Lever(board=self, device_type=device[1], pin_number=device[0], device_name=device[2])
                elif device[1] == "Infrared Beam":
                    self.devices[device[2]] = InfraredBeam(board=self, device_type=device[1], pin_number=device[0], device_name=device[2])
                
                self.board_booted = True

            
    def board_booted(self):
        return self.board_booted

class Pin():
    def __init__(self, board, device_type, pin_number=int(), device_name=str()):
        try:
            
            self.board = board
            self.device_type = device_type
            self.pin_number = pin_number
            self.device_name = device_name
            
            if self.device_type == "Light":
                self.pin_settings = 'd:' + str(self.pin_number) +':o'
                self.pin = self.board.get_pin(self.pin_settings)
                
            if self.device_type == "Solenoid":
                self.pin_settings = 'd:' + str(self.pin_number) +':p'
                self.pin = self.board.get_pin(self.pin_settings)
                
            if self.device_type == "Servo":
                self.pin_settings = 'd:' + str(self.pin_number) +':s'
                self.pin = self.board.get_pin(self.pin_settings)
                
            if self.device_type == "Lever":
                self.pin_settings = 'd:' + str(self.pin_number) +':i'
                self.pin = self.board.get_pin(self.pin_settings)

            if self.device_type == "Infrared Beam":
                self.pin_settings = 'd:' + str(self.pin_number) +':i'
                self.pin = self.board.get_pin(self.pin_settings)
            
        except:
            UserPrompts.show_error("Error", self.device_name + " failed to connect")

    def read(self):
        return self.pin.read()
    
    def record(self, action):
        if self.board.record_board == True:
            self.board.recordings.append([time.time(), self.device_name, action])
            print [time.time(), self.device_name, action]

class WritablePin(Pin):
    def __init__(self, *args, **kwargs):
        Pin.__init__(self, *args, **kwargs)
        
        self.pin_type = "Writable Pin"
    
    def write(self, value):
    
        self.record(value)
        self.pin.write(value)
         
        
class Servo(WritablePin):
    def __init__(self, init_value=110.0, retract_value=110.0, extend_value=35.0, *args, **kwargs):
        WritablePin.__init__(self, *args, **kwargs)
        
        self.type = "Servo"
        
        self.init_value = init_value
        self.retract_value = retract_value
        self.extend_value = extend_value
        
        self.write(self.init_value)
        self.extended = False
        
    def retract(self):
        self.write(self.retract_value)
        self.extended = False
        
    def extend(self):
        self.write(self.extend_value)
        self.extended = True

class Light(WritablePin):
    def __init__(self, init_value=0.0, off_value=0.0, on_value=1.0, *args, **kwargs):
        WritablePin.__init__(self, *args, **kwargs)
        
        self.type = "Light"
        
        
        self.init_value = init_value
        self.off_value = off_value
        self.on_value = on_value
        
        self.write(init_value)
    
    def extinguish(self):
        return self.write(self.off_value)
        
    def illuminate(self):
        return self.write(self.on_value)
    
    def toggle(self):
        if self.read() == True:
            self.extinguish()
        elif self.read() == False:
            self.illuminate()

class Solenoid(WritablePin):
    def __init__(self, init_value=0.0, off_value=0.0, on_value=1.0, *args, **kwargs):
        WritablePin.__init__(self, *args, **kwargs)
        
        self.type = "Solenoid"
        
        self.init_value = init_value
        self.off_value = off_value
        self.on_value = on_value
        
        self.write(self.init_value)
    
    def close(self):
        self.write(self.off_value)
        
    def open(self):
        self.write(self.on_value)
    
    def toggle(self):
        if self.read() == True:
            self.close()
        elif self.read() == False:
            self.open()


class IterativePin(Pin):
    def __init__(self, resting_state=False, *args, **kwargs):
        Pin.__init__(self, *args, **kwargs)
        
        self.pin_type = "Iterative Pin"
        
        self.resting_state = resting_state
        
        self.current_read = self.resting_state
        self.previous_read = self.resting_state
    
    def check_entrance(self):
        self.previous_read = self.current_read
        self.current_read = self.read()
        
        if (self.current_read !=  self.resting_state) and (self.previous_read == self.resting_state):
            self.record("Entrance")
            return True
        else:
            return False

    def check_exit(self):
        if self.current_read == self.resting_state and self.previous_read != self.resting_state:
            self.record("Exit")
            return True
        else:
            return False
        
class Lever(IterativePin):
    def __init__(self, *args, **kwargs):
        IterativePin.__init__(self, *args, **kwargs)
        
        self.type = "Lever"
        
        
class InfraredBeam(IterativePin):
    def __init__(self, *args, **kwargs):
        IterativePin.__init__(self, *args, **kwargs)
        
        self.type = "Infrared Beam"
