# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 00:06:27 2016

@author: isaiahnields
"""

import time

class Method():
    def __init__(self, method):
        self.method = method
        
        self.call_completed = False
        
        def method(self):
    
            if not self.call_completed:
                self.method()
                self.call_completed = True
            

class DelayedMethod():
    def __init__(self, method, delay_time):
        
        self.method = method
        self.delay_time = delay_time
        
        self.call_time = time.time()
        self.call_completed = False
        
    def method(self):
        
        if time.time() - self.call_time >= self.delay_time and not self.call_completed:
            
            self.method()
            self.call_completed = True
            return self.call_completed
        
        else:
            return self.call_completed
            
class TimedMethod():
    def __init__(self, on_method, on_duration, off_method):
        
        self.on_method = on_method
        self.on_duration = on_duration
        self.off_method = off_method
        
        self.call_time = time.time()
        self.call_completed = False
        
        self.on_method()
        
    def method(self):
        
        if time.time() - self.call_time >= self.on_duration and not self.call_completed:
            
            self.off_method()
            self.call_completed = True
            return self.call_completed
        
        else:
            return self.call_completed


class TimedDelayedMethod():
    def __init__(self, delay_time, on_method, on_duration, off_method):
        
        self.delay_time = delay_time
        self.on_method = on_method
        self.on_duration = on_duration
        self.off_method = off_method
        
        self.call_time = time.time()
        self.call_started = False
        self.call_ended = False
        
    def method(self):
        
        if time.time() - self.call_time >= self.delay_time and not self.call_started:
            self.on_method()
            self.call_started = True
            self.on_time = time.time()
        elif self.call_started:
            if time.time() - self.on_time >= self.on_duration and not self.call_ended:
                self.off_method()
                self.call_ended = True
                return self.call_ended
        else:
            return self.call_ended