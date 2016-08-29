# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 10:25:15 2016

@author: isaiahnields
"""

from TimeHandler import Method, DelayedMethod, TimedMethod, TimedDelayedMethod
import time


class StateHandler():
    def __init__(self, state_information, devices):
        self.state_information = state_information
        self.devices = devices
        
        self.states = {}
        
        for information in self.state_information:
            self.states[information[0]] = State(information, self.devices)
    def start(self):
        
        self.current_state = self.states[self.states.keys()[0]]
        print self.current_state.information[0]
        
        while True:
            
            self.current_state.run()
            if self.current_state.check_next():
                self.next()
            
    def next(self):
        self.current_state = self.states[self.current_state.information[2]]
        
        
        
        

class State():
    def __init__(self, information, devices, *args, **kwargs):
        self.information = information
        self.devices = devices
        
        self.time_stamped = False
        self.procedures = []
        self.methods = []
        
        for procedure in self.information[3]:
            for device in self.devices:
                if procedure[0] == self.devices[device].device_name:
                    print devices[device].type
                    if procedure[1] == None and procedure[3] == None:
                        self.methods.append(lambda: self.devices["Chamber Light"].write(procedure[2]))
                        self.procedures.append(Method(self.methods[len(self.methods)-1]))
#                    elif procedure[1] == None and procedure[3] != None:
#                        on_method = lambda: self.devices[device].write(procedure[2])
#                        off_method = lambda: self.devices[device].write(procedure[4])
#                        self.procedures.append(TimedMethod(lambda: on_method, procedure[3], off_method))
#                    elif procedure[1] != None and procedure[3] == None:
#                        method = lambda: self.devices[device].write(procedure[2])
#                        self.procedures.append(DelayedMethod(method, procedure[1]))
#                    elif procedure[1] != None and procedure[3] != None:
#                        on_method = lambda: self.devices[device].write(procedure[2])
#                        off_method = lambda: device.write(procedure[4])
#                        self.procedures.append(TimedDelayedMethod(procedure[1], on_method, procedure[3], off_method))
    def run(self):
        for procedure in self.procedures:
            procedure.method()
            
    def check_next(self):
        
        if not self.time_stamped:
            self.start_time = time.time()
            
        if type(self.information[1]) == float:
            if time.time() - self.start_time >= self.information[1]:
                return True
        
        elif type(self.information[1]) == str:
            pass
        
        return False