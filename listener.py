import tnc
import time
import app_utils

LOADINGTXT = "Waiting for a response"
LOADER_CNT = 0


def wait(win):
    waiting_text = app_utils.create_label(win, LOADINGTXT)

    for i in range(3):  # will try 3 times before failing
        time.sleep(1)
        response = check_signal()
        update_msg(win, waiting_text)
        if response:
            waiting_text.destroy()
            return response

    waiting_text.destroy()
    return None


def check_signal():
    response = tnc.read()
    if len(response) > 0:
        return response
    return None


def update_msg(win, text):
    global LOADER_CNT
    trailing = ''

    if LOADER_CNT > 2:
        LOADER_CNT = 0
    for i in range(0, LOADER_CNT + 1):
        trailing += '.'

    loading_text = LOADINGTXT + trailing
    text.config(text=loading_text)
    win.update()
    print(loading_text)
    LOADER_CNT += 1
