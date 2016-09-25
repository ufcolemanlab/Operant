# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 10:25:15 2016

@author: isaiahnields
"""

import TimeHandler
import time
import random



class TrialHandler():
    def __init__(self, trial_information=list, devices=list):
        
        self.trial_information = trial_information
        
        
        self.states = {}
        
        for state_information in self.trial_information:
            self.states[state_information[0]] = State(state_information, devices)
            
    def start(self):
        
        self.current_state = self.states[self.states.keys()[0]]
        print self.current_state.state_information[0]
        
        while True:
            
            self.current_state.run()
            if self.current_state.check_next():
                self.next()
        
    def next(self):
        self.current_state.time_stamped = False
        self.current_state = self.states[self.current_state.state_information[3]]
        print self.current_state.state_information[0]
        
        

class State():
    def __init__(self, state_information, devices):

        self.state_information = state_information
        
        self.procedures = []
        
        self.time_stamped = False
        self.random_time_generated = False
        for procedure in self.state_information[4]:
            for device in devices:
                if device != None:
                    if int(procedure[0]) == int(device.pin_number):
                        self.procedures.append(TimeHandler.package_method(method=device.write, delay_time=procedure[2], on_value=procedure[3], on_duration=procedure[4], off_value=procedure[5]))
                        
    def run(self):
        for procedure in self.procedures:
            procedure.packaged_method()
            
    def check_next(self):
        
        if not self.time_stamped:
            self.start_time = time.time()
            self.time_stamped = True
            
        if type(self.state_information[1]) == float and self.state_information[2] == None:
            if time.time() - self.start_time >= self.state_information[1]:
                for procedure in self.procedures:
                    procedure.reset_variables()
                return True
        elif type(self.state_information[1]) == float and type(self.state_information[2]) == float:
            if not self.random_time_generated:
                self.time_range = random.uniform(0, self.state_information[2])
            if time.time() - self.start_time >= self.state_information[1] + self.time_range:
                for procedure in self.procedures:
                    procedure.reset_variables()
                return True
                
        return False
            