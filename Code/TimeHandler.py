# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 00:06:27 2016

@author: isaiahnields
"""

import time



def package_method(method=None, delay_time=None, on_value=None, on_duration=None, off_value=None):
    
    if method == None:
        print "Method required"
    
    elif (on_value != None) and (delay_time == None and on_duration == None and off_value == None):
        return Method(method=method, on_value=on_value)
        
    elif (delay_time != None and on_value != None) and (on_duration == None and off_value == None):
        return DelayedMethod(method=method, delay_time=delay_time, on_value=on_value)
        
    elif (on_value != None and on_duration != None and off_value != None) and (delay_time == None):
        return TimedMethod(method=method, on_value=on_value, on_duration=on_duration, off_value=off_value)
    
    elif (delay_time != None and on_value != None and on_duration != None and off_value != None):
        return TimedDelayedMethod(method=method, delay_time=delay_time, on_value=on_value, on_duration=on_duration, off_value=off_value)
        
        


class Method():
    def __init__(self, method=None, on_value=float):

        self.method = method
        self.on_value = on_value
        
        self.reset_variables()

    def packaged_method(self):
        
        if not self.time_stamped:
            self.call_time = time.time()
            self.time_stamped = True

        if not self.on_call_completed:
            self.method(self.on_value)
            self.on_call_completed = True
                
    def reset_variables(self):
        
        self.on_call_completed = False
        self.on_time_completed = False
        self.off_call_completed = False
        self.time_stamped = False
        
        self.call_time = time.time()*2
        self.on_time = time.time()*2
            

class DelayedMethod(Method):
    def __init__(self, method, delay_time, on_value, *args, **kwargs):
    
        self.method = method
        self.delay_time = delay_time
        self.on_value = on_value
        
        self.reset_variables()
        
    def packaged_method(self):
        
        if not self.time_stamped:
            self.call_time = time.time()
            self.time_stamped = True
        
        if time.time() - self.call_time >= self.delay_time and not self.on_call_completed:
            
            self.method(self.on_value)
            self.on_call_completed = True
            return self.on_call_completed
        
        else:
            return self.on_call_completed
            
class TimedMethod(Method):
    def __init__(self, method, on_value, on_duration, off_value):
        
        self.method = method
        self.on_value = on_value
        self.on_duration = on_duration
        self.off_value = off_value
        
        self.reset_variables()
        
    def packaged_method(self):

        if not self.on_call_completed:
            self.method(self.on_value)
            self.on_call_completed = True
        
        if not self.time_stamped:
            self.call_time = time.time()
            self.time_stamped = True
        
        if time.time() - self.call_time >= self.on_duration and not self.off_call_completed:
            self.method(self.off_value)
            self.off_call_completed = True
            return self.off_call_completed
        
        else:
            return self.off_call_completed


class TimedDelayedMethod(Method):
    def __init__(self, method, delay_time, on_value, on_duration, off_value):
        
        self.method = method
        self.delay_time = delay_time
        self.on_value = on_value
        self.on_duration = on_duration
        self.off_value = off_value
        
        self.reset_variables()
        
    def packaged_method(self):
        
        if not self.time_stamped:
            self.call_time = time.time()
            self.time_stamped = True
        
        if time.time() - self.call_time >= self.delay_time and not self.on_call_completed:
            self.method(self.on_value)
            self.on_call_completed = True
            self.on_time = time.time()
        elif self.on_call_completed:
            if time.time() - self.on_time >= self.on_duration and not self.off_call_completed:
                self.method(self.off_value)
                self.off_call_completed = True
                return self.off_call_completed
        else:
            return self.off_call_completed
            
            
