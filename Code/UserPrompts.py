# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 23:10:03 2016

@author: Isaiah Nields
"""

import tkMessageBox
import tkFileDialog


def show_error(title, text):
    tkMessageBox.showerror(title, text)

def show_warning(title, text):
    tkMessageBox.showwarning(title, text)

def show_info(title, text):
    tkMessageBox.showinfo(title, text)
    

def ask_save_location():
    options = {}             
    options['defaultextension'] = '.csv'        
    options['filetypes'] = [('Comma Separated Values file', ".csv")]
    save_location = tkFileDialog.asksaveasfilename(**options)
    return save_location

def ask_open_location():
    options = {}                    
    file_location = tkFileDialog.askopenfilename(**options)
    return file_location