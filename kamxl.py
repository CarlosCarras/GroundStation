#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : February 21, 2021
@description : transmits and receives the telecommand and data to/from the TNC over KISS
@source      : https://github.com/ampledata/kiss
'''

import telecommands
import kiss
import aprs

#------------- Special Characters -------------#
FEND  = 0xC0
FESC  = 0xDB
TFEND = 0xDC
TFESC = 0xDD

#--------------- Command Codes ----------------#
date_frame   = 0x00
tx_delay     = 0x01
persistence  = 0x02
slot_time    = 0x03
tx_tail      = 0x04
full_duplex  = 0x05
set_hardware = 0x06
exit_kiss    = 0xFF


class KAMXL_TNC():
    def __init__(self):
        self.k = kiss.SerialKISS('/dev/ttyUSB0', 9600)
        self.k.start()                              # inits the TNC, optionally passes KISS config flags.

        self.frame = aprs.Frame()
        self.frame.source = aprs.Callsign(telecommands.SRC_CALLSIGN)
        self.frame.destination = aprs.Callsign(telecommands.DST_CALLSIGN)

    def print_inbound(x):
        print(x)                                    # prints whatever is passed in.

    def read(self):
        self.k.read(callback=self.print_inbound)    # reads frames and passes them to `p`

    def write(self, text):
        self.frame.text = text
        self.k.write(self.frame)