# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 21:40:19 2016

@author: isaiahnields
"""

import Tkinter as tk
import ttk
from ConfigureBoardWindow import ConfigureBoardWindow
from ControlBoardWindow import ControlBoardWindow
from BoardHandler import BoardHandler
from DatabaseHandler import BoardDatabase



class CommandWindow(tk.Tk):
    def __init__(self, *args, **kwargs):        
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable( 0, 0)
        self.title('Controller')
        
        self.frame = tk.Frame(self, padx = 5, pady = 5)
        self.frame.grid(column=0, row=0, sticky=('nesw'))
        
        ttk.Button(self.frame, text="Start Board", command=self.start_board).grid(column=1, row=1, padx=5, pady=5)
        ttk.Button(self.frame, text="Configure Board", command = self.configure_board).grid(column=1, row=2, padx=5, pady=5)
        ttk.Button(self.frame, text="Control Board", command=self.control_board).grid(column=1, row = 3, padx=5, pady=5)
        ttk.Button(self.frame, text="Run Trial").grid(column=2, row=1, padx=5, pady=5)
        ttk.Button(self.frame, text="Configure Trial").grid(column=2, row=2, padx=5, pady=5)
        ttk.Button(self.frame, text ="Open Recording").grid(column=3, row=1, padx=5, pady=5)
        
    
    def start_board(self):
        try:
            self.board.exit()
        except:
            pass
        board_database = BoardDatabase()
        print board_database.load()
        self.boardhandler = BoardHandler(board_database.load())
        self.boardhandler.boot()
        
    
    def configure_board(self):
        try:
            self.board.exit()
        except:
            pass
        
        ConfigureBoardWindow(self)

    def control_board(self):
        try:
            ControlBoardWindow(self, devices=self.boardhandler.board.devices)
        except AttributeError:
            self.start_board()
            ControlBoardWindow(self, devices=self.boardhandler.board.devices)
    def on_closing(self):
        try:
            self.board.exit()
            self.destroy()
        except:
            self.destroy()
        

root = CommandWindow()
root.protocol("WM_DELETE_WINDOW", root.on_closing)
root.mainloop()