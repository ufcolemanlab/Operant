# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 18:23:37 2016

@author: isaiahnields
"""
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import tkSimpleDialog
import ttk
import csv
import matplotlib.pyplot as plt
from pyfirmata import Arduino, util, serial
import time
import numpy
from scipy import stats

save_loc = ''
time_array = []
amount_of_water_array = []
time_value = float()
amount_of_water_value = float()
x_time = float()
m = float()
b = float()


def start_board():
    try:
        board = Arduino('COM5')
        it = util.Iterator(board)
        it.start()
        board.analog[0].enable_reporting()
        global solenoid_pin
        solenoid_pin = board.get_pin('d:3:p')
        solenoid_pin.write(0.0)
        print "done"
    except serial.SerialException:
        tkMessageBox.showwarning("Solenoid Calibrator", "Could not open port")
def add_data(*args):
    global save_loc
    if save_loc == '':
        tkMessageBox.showwarning("Solenoid Calibrator", "Please choose CSV save locaiton")
    
    elif sol_time.get() == None:
        tkMessageBox.showwarning("Solenoid Calibrator", "Please input time")
    
    else:
        amount_of_water_value = ask_amount_of_water()
        if amount_of_water_value == None:
            tkMessageBox.showwarning("Solenoid Calibrator", "Please amount of water")
            add_data()
            
        else:
            time_value = float(sol_time.get())
            with open(save_loc, 'a') as csvfile:
                writer = csv.writer(csvfile, lineterminator='\n', dialect = 'excel')
                writer.writerow([time_value, amount_of_water_value])
                
            time_array.append(time_value)
            amount_of_water_array.append(amount_of_water_value)
            print len(amount_of_water_array)
            trial_number.set("Trial: " + str(len(amount_of_water_array)))
                
            last_trial_time = float(sol_time.get())
            next_trial_time = last_trial_time + float(time_increment.get())
            sol_time.set(str(next_trial_time))
            amount_of_water.set('')
            calc_linear_reg()
def choose_save_location():
    global save_loc
    options = {}             
    options['defaultextension'] = '.csv'        
    options['filetypes'] = [('Comma Separated Values file', ".csv")]
    save_loc = tkFileDialog.asksaveasfilename(**options)
    try:
        with open(save_loc, 'a') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n', dialect = 'excel')
            writer.writerow(['Solenoid Open Time (s)', 'Amount of Water (g)'])
    except IOError:
        pass
def ask_amount_of_water():
    return tkSimpleDialog.askfloat('Solenoid Calibrator', 'Amount of Water (g):')
def plot_data():
    try:
        plt.grid(True)
        plt.xlabel('Amount of Water (grams)')
        plt.ylabel('Solenoid Open Time (seconds)')
        plt.plot(amount_of_water_array, time_array,'ro')
        plt.plot(amount_of_water_array, numpy.poly1d(numpy.polyfit(amount_of_water_array, time_array, 1))(amount_of_water_array))
        plt.show()
    except TypeError:
        tkMessageBox.showwarning("Solenoid Calibrator", "No data has been created or imported")
def run_trial():
    try:
        time_value = float(sol_time.get())
        solenoid_pin.write(1.0)
        time.sleep(time_value)
        solenoid_pin.write(0.0)
    except ValueError:
        tkMessageBox.showwarning("Solenoid Calibrator", "Please input amount of time")
    except NameError, e:
        tkMessageBox.showwarning("Solenoid Calibrator", "Please start board")
        print e
        
def open_csv():
    time_array[:] = []
    amount_of_water_array[:] = []
    options = {}             
    options['defaultextension'] = '.csv'        
    options['filetypes'] = [('Comma Separated Values file', ".csv")]
    try:
        csv_file_loc = tkFileDialog.askopenfilename(**options)
        with open(csv_file_loc, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                try:
                    time_array.append(float(row[0]))
                    amount_of_water_array.append(float(row[1]))
                except ValueError:
                    pass
    except IOError: 
        pass
    if len(time_array) != 0:        
        calc_linear_reg()
        tkMessageBox.showinfo("Solenoid Calibrator", "Data loaded")
def run_f_of_x():
    if x_time_entry.get() == '':
        tkMessageBox.showwarning("Solenoid Calibrator", "Please input x value")
    elif len(time_array) == 0:
        tkMessageBox.showwarning("Solenoid Calibrator", "Please create or import data")
    else:        
        calc_linear_reg()
        m, b = numpy.polyfit(amount_of_water_array, time_array, 1)    
        f_of_x.set("f(" + str(round(float(x_time_entry.get()), 4)) + ") = " + str(round(float(x_time_entry.get()), 4)*m + b))
        
def calc_linear_reg():
    m, b = numpy.polyfit(amount_of_water_array, time_array, 1)
    best_fit_line.set("f(x) = x*" + str(m) + ' + ' + str(b))
def clear_data():
    time_array[:] = []
    amount_of_water_array[:] = []
    f_of_x.set('')
    best_fit_line.set('')
    sem_text.set('')
def calc_sem():
    print amount_of_water_array
    sem_text.set(str(round(numpy.mean(amount_of_water_array), 3)) + " +/- " + str(round(stats.sem(amount_of_water_array), 3)))
    
    
root = tk.Tk()
root.resizable(0,0)
root.title("Solenoid Calibrator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=('nesw'))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

sol_time = tk.StringVar()
sol_time.set('100')
amount_of_water = tk.StringVar()
time_increment = tk.StringVar()
best_fit_line = tk.StringVar()
f_of_x = tk.StringVar()
sem_text = tk.StringVar()
trial_number = tk.StringVar()

ttk.Label(mainframe, text="Solenoid Open Time (s):").grid(column=1, row=1, sticky='n')
time_entry = ttk.Entry(mainframe, width=7, textvariable=sol_time)
time_entry.grid(column=2, row=1, sticky=('w', 'e'))

ttk.Label(mainframe, text="Time Increment per Trial (s):").grid(column=1, row=2, sticky='n')
trial_increment_entry = ttk.Entry(mainframe, width=7, textvariable=time_increment)
trial_increment_entry.grid(column=2, row=2, sticky=('w', 'e'))

ttk.Label(mainframe, text="Best Fit Line:").grid(column=1, row=3, sticky='n')
ttk.Label(mainframe, text="", textvariable=best_fit_line).grid(column=2, row=3, sticky='n')

ttk.Label(mainframe, text="Desired Amount of Water (g) = ").grid(column=1, row=4, sticky='e')
x_time_entry = ttk.Entry(mainframe, width=4, textvariable=x_time)
x_time_entry.grid(column=2, row=4, sticky=('w'))
ttk.Label(mainframe, text="f(" + x_time_entry.get() + ") = ", textvariable=f_of_x).grid(column=2, row=4, sticky='e')

ttk.Label(mainframe, text="Average +/- SEM:").grid(column=1, row=5, sticky='n')
ttk.Label(mainframe, text="", textvariable=sem_text).grid(column=2, row=5, sticky='n')
ttk.Label(mainframe, text="Trial:", textvariable=trial_number).grid(column=1, row=7, sticky='n')

ttk.Button(mainframe, text="Start Board", command=start_board).grid(column=3, row=1, sticky='n')
ttk.Button(mainframe, text="CSV Location", command=choose_save_location).grid(column=4, row=1, sticky='n')
ttk.Button(mainframe, text="Run Trial", command=run_trial).grid(column=3, row=2, sticky='n')
ttk.Button(mainframe, text="Record Data", command=add_data).grid(column=4, row=2, sticky='n')
ttk.Button(mainframe, text="Plot Data", command=plot_data).grid(column=3, row=3, sticky='n')
ttk.Button(mainframe, text="Open CSV", command=open_csv).grid(column=4, row=3, sticky='n')
ttk.Button(mainframe, text="Run f(x)", command=run_f_of_x).grid(column=3, row=4, sticky='n')
ttk.Button(mainframe, text="Clear data", command=clear_data).grid(column=4, row=4, sticky='n')
ttk.Button(mainframe, text="Calculate SEM", command=calc_sem).grid(column=3, row=5, columnspan=2, sticky='n')

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

time_entry.focus()
trial_increment_entry.focus()
root.bind('<Return>', add_data)

root.mainloop()