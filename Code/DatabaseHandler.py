 # -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 17:52:07 2016

@author: isaiahnields
"""

import sqlite3


class BoardDatabase():
    
    def save(self, board_devices=list):
            
        self.conn = sqlite3.connect('Database/board_settings.db')
        self.c = self.conn.cursor()
        
        self.board_devices = board_devices
        
        # Create table
        try:
            self.c.executescript('DROP TABLE IF EXISTS Board;')
            self.c.execute('''CREATE TABLE Board (Pin int, Type text, Name text)''')
        except sqlite3.OperationalError, e:
            print e
        
        for row, device in zip(range(2,13), self.board_devices):
            # Insert a row of data
        
            self.pin = device[0]
            self.device_type = device[1]
            self.device_name = device[2]
            
            self.c.execute("INSERT OR REPLACE INTO Board (Pin, Type, Name) values (?, ?, ?)", (self.pin, self.device_type, self.device_name))
        
            # Save (commit) the changes
        self.conn.commit()
            
            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
        self.conn.close()
        
    def load(self):
        try:       
            self.conn = sqlite3.connect('Database/board_settings.db')
            self.c = self.conn.cursor()
            
            self.board_devices = []
            for row in self.c.execute("SELECT rowid, * FROM Board ORDER BY Pin"):
                self.board_devices.append([row[1], row[2], row[3]])
            return self.board_devices
        except:
            pass