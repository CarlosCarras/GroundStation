#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : February 22, 2021
@description : generates a GUI for telecommand selection
'''

import time
import app_utils
import telecommands
import handler
import interpreter

def debug_led_toggle():
    confirmation = app_utils.confirm_input('Toggle Debug LED')
    if confirmation:
        response = handler.send_telecom(telecommands.TELECOM_DEBUG_TOGGLE)
        interpreter.interpret(response)
        print("Toggled the debug LED.")

def debug_led_off():
    confirmation = app_utils.confirm_input('Debug LED Off')
    if confirmation:
        response = handler.send_telecom(telecommands.TELECOM_DEBUG_OFF)
        interpreter.interpret(response)
        print("Turned off the debug LED.")

def debug_led_on():
    confirmation = app_utils.confirm_input('Debug LED On')
    if confirmation:
        response = handler.send_telecom(telecommands.TELECOM_DEBUG_ON)
        interpreter.interpret(response)
        print("Turned on debug LED.")

def update_guidance():
    confirmation = app_utils.confirm_input('Update Guidance')
    if confirmation:
        filename = app_utils.get_filename("Guidance", ".csv")
        if not filename: return

        time.sleep(1)  # artificial delay, not necessary but helps user experience
        dest = app_utils.get_dir()
        if not dest:
            app_utils.show_error("File Upload Error", "Unable to place the file in the selected folder.")
            return

        response = handler.transfer_file(telecommands.TELECOM_UPLOAD_GUIDANCE, filename, dest)
        interpreter.interpret(response)
        print("Uploaded guidance file: " + dest)