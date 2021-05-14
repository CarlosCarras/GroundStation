#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : February 21, 2021
@description : transmits and receives the telecommand and data to/from the TNC over KISS
@source      : https://github.com/ampledata/kiss
'''

import telecommands
import kiss3 as kiss


class KAMXL_TNC():
    def __init__(self):
        self.k = kiss.SerialKISS(port='/dev/cu.usbserial-RTNG2ER', speed='9600')
        self.k.start()                              # inits the TNC

        self.frame = kiss.Frame()
        self.frame.set_source(telecommands.SRC_CALLSIGN)
        self.frame.set_dest(telecommands.DST_CALLSIGN)

    def print_inbound(self, x):
        print(x)                                    # prints whatever is passed in.

    def read(self):
        frames = self.k.read()
        self.print_inbound(frames)

    def write(self, text):
        self.frame.text = text
        self.k.write(self.frame)