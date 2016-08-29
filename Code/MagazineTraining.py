# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:40:07 2016

@author: isaiahnields
"""

from BoardHandler import BoardHandler
from StateHandler import StateHandler

cue_time = 1.0
reward_time = 0.025

board_configuration = [
    [2, "Servo", "Infrared Beam 1"],
    [3, "Solenoid", "Solenoid 1"],
    [5, "Light", "Nosepoke Light"],
    [6, "Servo", "Servo 1"], 
    [7, "Light", "Cue Light"],
    [8, "Lever", "Lever 1"],
    [9, "Servo", "Servo 2"],
    [12, "Light", "Chamber Light"]
                        ]
                        
trial_states = [
["Resting State", 20.0, "Reward State", 
     [
         ["Chamber Light", None, 1.0, None, None],
     ]
],
["Reward State", 2.0, "Resting State", 
     [
         ["Solenoid 1", None, 1.0, reward_time, 0.0],
         ["Cue Light", None, 1.0, cue_time, 0.0],
     ]
]
           ]
           

board_handler = BoardHandler(device_list=board_configuration)

board_handler.boot()

magazine_traing = StateHandler(state_information=trial_states, devices=board_handler.devices())
magazine_traing.start()
