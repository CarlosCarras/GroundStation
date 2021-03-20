#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 22, 2021
@modified    : February 22, 2021
@description : general application utilities
'''

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


GUI_COLOR = '#0D1B46'
LOGO = 'assets/adamus-logo.ico'
WINDOW_NAME = "ADAMUS Ground Station Control Panel"


def add_spacer(win, size=5, bg=GUI_COLOR):
    spacer = tk.Label(win, bg=bg, font=("Arial", size))
    spacer.pack(fill=tk.BOTH)


def center(win):
    win.update_idletasks()

    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width

    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width

    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('+{}+{}'.format(x, y))
    win.deiconify()


def confirm_input(telecom_str):
    warning = 'Are you sure you transmit the \'' + telecom_str + '\' telecommand?'
    response = tk.messagebox.askquestion('Transmission Warning',
                                         warning,
                                         icon='warning',
                                         default='no')
    if response == 'yes': return 1
    return 0

def get_filename(filetype, ext=".csv"):
    file_browser = tk.Tk()
    file_browser.withdraw()
    filename = filedialog.askopenfilename(initialdir=".",
                                          title="Select a " + filetype + " File",
                                          filetypes=((filetype, "*"+ext), ("all files", "*.*")))
    return filename

def get_dir():
    file_browser = tk.Tk()
    file_browser.withdraw()
    filename = filedialog.askdirectory(title="Select a Destination in the BBB Directory", initialdir="./bbb_sim")
    filename = filename.split("bbb_sim")[1]
    return filename
