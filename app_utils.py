#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 22, 2021
@modified    : May 6, 2021
@description : general application utilities
'''

import threading
import tkinter as tk
import time
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter import ttk


GUI_DIMS = "300x200"
GUI_COLOR = '#0D1B46'
LOGO = 'assets/adamus-logo.ico'
WINDOW_NAME = "ADAMUS Ground Station Control Panel"


def start_thread(target):
    x = threading.Thread(target=target)
    x.start()


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
    filename = filedialog.askopenfilename(initialdir="./assets",
                                          title="Select a " + filetype + " File",
                                          filetypes=((filetype, "*"+ext), ("all files", "*.*")))
    return filename

def get_dir():
    file_browser = tk.Tk()
    file_browser.withdraw()
    dir = filedialog.askdirectory(title="Select a Destination in the BBB Directory", initialdir="./bbb_sim")
    dir_split = dir.split("bbb_sim")
    if len(dir_split) != 2: return None

    return dir_split[1]


def show_error(title, message):
    messagebox.showerror(title, message)


def open_window(title, dims=GUI_DIMS):
    win = tk.Toplevel()
    win.title(title)
    win.geometry(dims)
    win.iconbitmap(LOGO)
    center(win)
    add_spacer(win, bg=None)

    return win


def open_busywindow(title, dims=GUI_DIMS):
    win = open_window(title, dims)
    win.config(cursor="wait")
    return win


def create_label(win, text, pady=10, color=None):
    if color:
        label = tk.Label(win, text=text, fg=color)
    else:
        label = tk.Label(win, text=text)
    label.pack(pady=pady)
    win.update()
    return label


def openProgressbar(win):
    progress = Progressbar(win, orient=tk.HORIZONTAL, length=180, mode='determinate')
    progress.pack(pady=10)
    time.sleep(1)
    return progress


def incrementProgressbar(win, progress, inc=50):
    progress['value'] += inc
    win.update()
    time.sleep(1)


def create_dictionary(win, key, text):
    frame = tk.Frame(win)
    frame.pack(fill=tk.X)

    key_label = tk.Label(frame, text=key)
    key_label.pack(side=tk.LEFT, padx=20, pady=5)

    text_label = tk.Entry(frame)
    text_label.insert(tk.END, text)
    text_label.pack(side=tk.LEFT, padx=5, pady=5)