
import time
import app_utils
from tkinter import messagebox

LOADINGTXT = "Waiting for a response"

LOADER_CNT = 0
DEBUG_CNT = 0


def listen():
    win = app_utils.open_busywindow("Waiting for Response")
    await_signal(win)
    return "Testing!"

def check_signal():
    time.sleep(1)
    global DEBUG_CNT
    if DEBUG_CNT < 8:
        DEBUG_CNT += 1
        return 0
    DEBUG_CNT = 0
    return 1

def await_signal(win):
    loading_text = app_utils.create_label(win, text="")

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

    loading_text.config(text=LOADINGTXT + trailing + "\n\n\nDO NOT PROCEED.")
    loading_text.place()
    loading_text.pack()
    print(LOADINGTXT + trailing)
    LOADER_CNT += 1
    win.update()

