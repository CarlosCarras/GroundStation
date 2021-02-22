#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : February 21, 2021
@description : generates a GUI for telecommand selection
'''

import threading
import tkinter as tk
from tkinter import messagebox


GUI_DIMS = "1000x500"
LOGO = 'assets/adamus-logo.ico'


def confirm_input(telecom_str):
    warning = 'Are you sure you transmit the \'' + telecom_str + '\' telecommand?'
    response = tk.messagebox.askquestion('Transmission Warning',
                                         warning,
                                         icon='warning',
                                         default='no')
    return response

def start_thread(target):
    x = threading.Thread(target=target)
    x.start()

#----------------------- thread targets ----------------------#
def debug_led_toggle():
    response = confirm_input('Toggle Debug LED')
    if response == 'yes':
        print("Toggled the debug LED.")

def debug_led_off():
    response = confirm_input('Debug LED Off')
    if response == 'yes':
        print("Turned off the debug LED.")

def debug_led_on():
    response = confirm_input('Debug LED On')
    if response == 'yes':
        print("Turned on debug LED.")

#---------------------- button callbacks ---------------------#
def debug_led_toggle_cb():
    start_thread(debug_led_toggle)

def debug_led_off_cb():
    start_thread(debug_led_off)

def debug_led_on_cb():
    start_thread(debug_led_on)

#------------------------ Application ------------------------#
class Application(tk.Frame):
    def __init__(self, master=None):
        if (master == None): master = tk.Tk()

        super().__init__(master)
        self.master = master
        self.pack(pady=20)

        self.button_arr = []
        self.num_buttons = 0

        self.master.title("ADAMUS Ground Station Control Panel")
        self.master.iconbitmap(LOGO)

        self.master.eval('tk::PlaceWindow . center')
        self.master.geometry(GUI_DIMS)
        self.master['bg'] = '#0D1B46'
        self.center()
        self.create_widgets()

    def center(self):
        win = self.master
        win.update_idletasks()

        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width

        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width

        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def create_button(self, text, callback):
        n = self.num_buttons
        self.num_buttons += 1

        self.button_arr.append(tk.Button(self, text=text, command=callback, padx = 50, pady=10))
        self.button_arr[n].place(y=n)
        self.button_arr[n].pack(side="top", fill=tk.BOTH)

    def create_widgets(self):
        self.create_button("Toggle Debug LED", debug_led_toggle_cb)
        self.create_button("Turn Off Debug LED", debug_led_off_cb)
        self.create_button("Turn On Debug LED", debug_led_on_cb)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)