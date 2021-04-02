
import time
import tkinter as tk
from tkinter import messagebox
import app_utils


GUI_DIMS = "400x400"
LOADINGTXT = "Waiting for a response"

LOADER_CNT = 0
DEBUG_CNT = 0


def listen():
    load_win = open_loadscreen()
    await_signal(load_win)

def check_signal():
    time.sleep(1)
    global DEBUG_CNT
    if DEBUG_CNT < 4:
        DEBUG_CNT += 1
        return 0
    DEBUG_CNT = 0
    return 1

def await_signal(win):
    loading_text = tk.Label(win, bg=None)

    while(1):
        update_msg(win, loading_text)
        if check_signal():
            win.destroy()
            break


def update_msg(win, loading_text):
    global LOADER_CNT
    trailing = ''

    for i in range(0,LOADER_CNT-1):
        trailing += '.'
    if LOADER_CNT > 3:
        LOADER_CNT = 0

    loading_text.config(text=LOADINGTXT + trailing)
    print(LOADINGTXT + trailing)
    LOADER_CNT += 1
    win.update()


def open_loadscreen():
    load_win = tk.Toplevel()
    load_win.title("Awaiting a Response")
    load_win.geometry(GUI_DIMS)
    load_win.iconbitmap(app_utils.LOGO)
    app_utils.center(load_win)
    app_utils.add_spacer(load_win, bg=None)

    return load_win