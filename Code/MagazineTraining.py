# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:40:07 2016

@author: isaiahnields
"""

from BoardHandler import Board
from StateHandler import TrialHandler

cue_time = 1.0
reward_time = .025

board_information = [

  # JEC: need to add 'nosepoke" detection
['d' , 1, 'o', None, None],
['d' , 2, 's', 'Servo', 'Servo 1'],
['d' , 3, 'o', None, None],
['d' , 4, 'o', None, None],
['d' , 5, 'o', None, None],
['d' , 6, 'o', None, None],
['d' , 7, 'o', 'Light', 'Cue Light'],
['d' , 8, 'o', None, None],
['d' , 9, 'o', None, None],
['d' , 10, 'o', None, None],
['d' , 11, 'o', None, None],
['d' , 12, 'o', 'Light', 'Chamber Light']

]
# output CSV with event timestamps (including nosepoke entry/exit)                        
trial_states = [
["Resting State", 2.0, 9.0, "Reward State", 
     [
         [12, "Chamber Light", None, 1.0, None, None],
         [7, "Cue Light", None, 0.0, None, None],

     ]
],
["Reward State", 1.0, None, "Resting State", 
     [   [12, "Chamber Light", None, 1.0, None, None],
#         ["Solenoid 1", None, 1.0, reward_time, 0.0],
         [7, "Cue Light", None, 1.0, cue_time, 0.0],
         [2, "Servo 1", None, 170.0, 1.0, 2.0]
     ]
]
           ]

                
board = Board(board_information=board_information)
board.boot_board()
board.boot_pins()

magazine_traing = TrialHandler(trial_information=trial_states, devices=board.pins)
magazine_traing.start()
