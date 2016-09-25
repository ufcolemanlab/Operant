# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 12:37:34 2016

@author: isaiahnields
"""

from pyfirmata import Arduino, util, serial
import serial.tools.list_ports
import UserPrompts
import time



class Board(Arduino):
    def __init__(self, board_information=list, record_board=True, *args, **kwargs):

        self.board_information = board_information
        self.record_board = record_board
        
        self.board_booted = False
        
    def boot_board(self):
            
        self.ports = list(serial.tools.list_ports.comports())
        
        for port in self.ports:
            if "Arduino" in port[1] or "Generic" in port[1]:
                self.aruindo_port = port[0]
            
        Arduino.__init__(self, self.aruindo_port)
        it = util.Iterator(self)
        it.start()
        self.analog[0].enable_reporting()
                    
        self.board_connected = True          
            
    
    def boot_pins(self):
    
        if self.board_connected:
            
            self.pins = [None]
            
            for pin in self.board_information:
                if pin[3] == None:
                    self.pins.append(None)
                else:
                    self.pins.append(Pin(board=self, pin_type=pin[0], pin_number=str(pin[1]), pin_mode=pin[2], pin_name=pin[4]))
                
                self.board_booted = True
                
                
class Pin():
    def __init__(self, board=None, pin_type='d', pin_number=int, pin_mode= 'o', pin_name=str):
        
        self.board = board        
        self.pin_type = pin_type
        self.pin_number = pin_number
        self.pin_mode = pin_mode
        self.pin_name = pin_name
        
        self.pin = self.board.get_pin(self.pin_type + ':' + str(self.pin_number) + ':' + self.pin_mode)
        
    def write(self, value=float):
        if self.board.record_board == True and self.pin.read() != value:
            print [time.time(), self.pin_name, value]
        self.pin.write(value)
        
    def read(self):
        return self.pin.read()
        
    
    
#board.pins[7].write(1.0)
#board.pins[12].write(1.0)
        