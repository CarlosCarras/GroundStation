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
        filename = app_utils.get_filename("Guidance", ext=".csv", initdir="assets")
        if not filename: return

        dest = app_utils.get_dir()
        if not dest: return

        response = handler.uplink_file(telecommands.TELECOM_UPLOAD_FILE, filename, dest)
        interpreter.interpret(response)
        print("Uploaded guidance file '" + filename + "' to directory '" + dest + "'.")

def retrieve_file():
    confirmation = app_utils.confirm_input('Retrieve File')
    if confirmation:
        sel = app_utils.important_prompt("Would you like to find the file in the BeagleBone Black simulated "
                                         "directory? Selecting 'yes' will launch the file browser. Selecting 'no' "
                                         "will prompt you to first find the destination directory and then manually "
                                         "enter the filename.")
        if sel == 1:
            dest = app_utils.get_filename("All Files", initdir="bbb_sim", filterByDir=True)
            if not dest: return
        elif sel == 2:
            dir = app_utils.get_dir()
            if not dir: return

            filename = app_utils.get_textentry("Filename Prompt", "Enter the filename of the file to be retrieved.")
            if not filename: return

            dest = dir + "/" + filename
        else:
            return

        response = handler.downlink_file(telecommands.TELECOM_GET_FILE, dest)
        interpreter.interpret(response)
        print("Downloaded file: " + dest)