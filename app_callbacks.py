#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : March 19, 2021
@description : generates a GUI for telecommand selection
'''

import time
import app_utils
import telecommands
import handler
import listener


def await_response():
    time.sleep(2)
    listener.listen()

#----------------------- thread targets ----------------------#
def debug_led_toggle():
    confirmation = app_utils.confirm_input('Toggle Debug LED')
    if confirmation:
        print("Toggled the debug LED.")
        app_utils.start_thread(await_response)

def debug_led_off():
    confirmation = app_utils.confirm_input('Debug LED Off')
    if confirmation:
        print("Turned off the debug LED.")
        app_utils.start_thread(await_response)

def debug_led_on():
    confirmation = app_utils.confirm_input('Debug LED On')
    if confirmation:
        print("Turned on debug LED.")
        app_utils.start_thread(await_response)

def update_guidance():
    confirmation = app_utils.confirm_input('Update Guidance')
    if confirmation:
        filename = app_utils.get_filename("Guidance", ".csv")
        if not filename: return

        time.sleep(1) # artificial delay, not necessary but helps user experience
        dest = app_utils.get_dir()
        if not dest:
            app_utils.show_error("File Upload Error", "Unable to place the file in the selected folder.")
            return

        print("Uploading guidance file: " + filename)
        handler.transfer_file(telecommands.TELECOM_UPLOAD_GUIDANCE, filename, dest)
        app_utils.start_thread(await_response)


#---------------------- button callbacks ---------------------#
def debug_led_toggle_cb():
    app_utils.start_thread(debug_led_toggle)

def debug_led_off_cb():
    app_utils.start_thread(debug_led_off)

def debug_led_on_cb():
    app_utils.start_thread(debug_led_on)

def update_guidance_cb():
    app_utils.start_thread(update_guidance)