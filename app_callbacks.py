#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : February 21, 2021
@description : generates a GUI for telecommand selection
'''

import threading
import app_utils

def start_thread(target):
    x = threading.Thread(target=target)
    x.start()

#----------------------- thread targets ----------------------#
def debug_led_toggle():
    confirmation = app_utils.confirm_input('Toggle Debug LED')
    if confirmation:
        print("Toggled the debug LED.")

def debug_led_off():
    confirmation = app_utils.confirm_input('Debug LED Off')
    if confirmation:
        print("Turned off the debug LED.")

def debug_led_on():
    confirmation = app_utils.confirm_input('Debug LED On')
    if confirmation:
        print("Turned on debug LED.")

#---------------------- button callbacks ---------------------#
def debug_led_toggle_cb():
    start_thread(debug_led_toggle)

def debug_led_off_cb():
    start_thread(debug_led_off)

def debug_led_on_cb():
    start_thread(debug_led_on)