#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 22, 2021
@modified    : February 22, 2021
@description : application security and password check functionalities
'''

import tkinter as tk
import app_utils

GUI_DIMS = "400x200"

PASSWORD = "test"
correct_pwd = 0
incorrect_pwd_attempts = 0


def password_iscorrect(password):
    if password == PASSWORD:
        return 1
    else:
        return 0


def check_password(win, password):
    global incorrect_pwd_attempts, correct_pwd
    if (password_iscorrect(password)):
        correct_pwd = 1
        win.destroy()
        return 1
    else:
        if incorrect_pwd_attempts == 0:
            app_utils.add_spacer(win, size=10, bg=None)
            tk.Label(win, text='Incorrect Password', fg='red').pack(side='top')
        incorrect_pwd_attempts += 1
        if incorrect_pwd_attempts == 3:
            exit(1)
    return 0


def launch_pwd_prompt(win):
    global correct_pwd
    password = ''

    pwdbox = tk.Entry(win, show='*')

    def onpwdentry(evt):
        password = pwdbox.get()
        check_password(win, password)

    def onokclick():
        password = pwdbox.get()
        check_password(win, password)

    tk.Label(win, text='Admin Password').pack(side='top')
    pwdbox.pack(side='top')
    pwdbox.bind('<Return>', onpwdentry)
    tk.Button(win, command=onokclick, text='OK').pack(side='top')

    win.geometry(GUI_DIMS)
    win.mainloop()
    if correct_pwd == 0: exit(1)

def check_creds():
    pwd_win = tk.Tk()

    app_utils.center(pwd_win)
    app_utils.add_spacer(pwd_win, bg=None, size=10)
    pwd_win.title(app_utils.WINDOW_NAME)
    pwd_win.iconbitmap(app_utils.LOGO)

    launch_pwd_prompt(pwd_win)