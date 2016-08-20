# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 21:21:22 2016

@author: isaiahnields
"""

import Tkinter as tk
import ttk
import UserPrompts
import csv

class RecordingWindow(tk.Toplevel):
    def __init__(self, window_name='', *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.resizable(0,0)
        self.title(window_name)
        self.geometry("1000x500")
        
        self.frame = tk.Frame(self, padx=5, pady=5)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.filemenu.add_command(label="Save As", command=self.save_file_as)
        

        self.menubar.add_cascade(label='File', menu=self.filemenu)
        
        self.config(menu=self.menubar)
        
        self.tree = ttk.Treeview(self.frame)
        self.tree["columns"] = ("time", "device", "event")
        self.tree["show"] = "headings"
        self.tree.column("time", stretch=True)
        self.tree.column("device", stretch=True)
        self.tree.column("event", stretch=True)
        self.tree.heading("time", text="Time")
        self.tree.heading("device", text="Device")
        self.tree.heading("event", text="Event")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.recording_data = []
        
    def open_file(self):
        self.file_location = UserPrompts.ask_open_location()
        try:
            with open(self.file_location, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in reader:
                    try:
                        self.recording_data.append([float(row[0]), row[1], row[2]])
                    except ValueError:
                        pass
                    except IndexError:
                        pass
        except IOError: 
            pass
        self.display_data()
        
    def display_data(self):
        for item in self.recording_data:
            self.tree.insert("" , tk.END, values=(item[0], item[1], item[2]))

    def save_file_as(self):
        self.save_location = UserPrompts.ask_save_location()
        try:
            with open(self.save_location, 'a') as csvfile:
                writer = csv.writer(csvfile, lineterminator='\n', dialect = 'excel')
                for item in range(len(self.recording_data)):
                    try:
                        writer.writerow[self.recording_data[item][0], self.recording_data[item][1], self.recording_data[item][2]]
                    except:
                        pass
        except IOError:
            pass