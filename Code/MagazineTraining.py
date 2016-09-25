# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:40:07 2016

@author: isaiahnields
"""

from BoardHandler2 import Board
from StateHandler2 import TrialHandler

cue_time = 1.0
reward_time = .025

board_information = [

['d' , 1, 'o', None, None],
['d' , 2, 'o', None, None],
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
                        
trial_states = [
["Resting State", 2.0, 3.0, "Reward State", 
     [
         [12, "Chamber Light", None, 1.0, None, None]
     ]
],
["Reward State", 2.0, None, "Resting State", 
     [   [12, "Chamber Light", None, 1.0, None, None],
#         ["Solenoid 1", None, 1.0, reward_time, 0.0],
         [7, "Cue Light", None, 1.0, cue_time, 0.0]
     ]
]
           ]
           

import TimeHandler

                
board = Board(board_information=board_information)
board.boot_board()
board.boot_pins()

magazine_traing = TrialHandler(trial_information=trial_states, devices=board.pins)
magazine_traing.start()
