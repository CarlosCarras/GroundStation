#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : February 22, 2021
@description : generates a GUI for telecommand selection
'''

import tkinter as tk
import app_callbacks
import app_utils
import app_security


GUI_DIMS = "1000x500"
PAGE_HEADER = "D3 Telecommands:"


class Application(tk.Frame):
    def __init__(self, master=None):
        app_security.check_creds()

        if (master == None): master = tk.Tk()

        super().__init__(master)
        self.master = master
        self.pack(pady=20)

        self.button_arr = []

        self.master.title(app_utils.WINDOW_NAME)
        self.master.iconbitmap(app_utils.LOGO)

        self.master.eval('tk::PlaceWindow . center')
        self.master.geometry(GUI_DIMS)
        self.master['bg'] = app_utils.GUI_COLOR
        app_utils.center(self.master)
        self.create_widgets()

    def create_button(self, text, callback):
        n = len(self.button_arr)
        self.button_arr.append(tk.Button(self, text=text, command=callback, padx = 50, pady=10))
        self.button_arr[n].place(y=n)
        self.button_arr[n].pack(fill=tk.BOTH)

        app_utils.add_spacer(self)

    def create_widgets(self):
        title = tk.Label(self, text=PAGE_HEADER, bg=app_utils.GUI_COLOR, fg='#fff', font=("Arial", 20))
        title.pack(fill=tk.BOTH)
        app_utils.add_spacer(self, 10)

        self.create_button("Toggle Debug LED", app_callbacks.debug_led_toggle)
        self.create_button("Turn Off Debug LED", app_callbacks.debug_led_off)
        self.create_button("Turn On Debug LED", app_callbacks.debug_led_on)
        self.create_button("Update Guidance", app_callbacks.update_guidance)
        self.create_button("Retreive File", app_callbacks.retrieve_file)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)