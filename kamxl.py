#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : February 21, 2021
@description : transmits and receives the telecommand and data to/from the TNC over KISS
@source      : https://github.com/ampledata/kiss
'''

import telecommands
import logging
from aioax25.kiss import SerialKISSDevice
from aioax25.interface import AX25Interface
from aioax25.frame import AX25UnnumberedInformationFrame


class KAMXL_TNC():
    def __init__(self):
        self.kissdev = SerialKISSDevice(
            device='/dev/ttyS0',
            baudrate=9600,
            log=logging.getLogger('./assets/D3_KISS.log'))
        self.ax25int = AX25Interface(
            kissport= self.kissdev[0],
            log=logging.getLogger('./assets/D3_AX25.log'))
        self.kissdev.open()


    def print_inbound(self, x):
        print(x)                                    # prints whatever is passed in.

    def read(self):
        self.print_inbound("Receive not yet implemented.")

    def write(self, text):
        payload = bytes(text, 'utf-8')
        frame = AX25UnnumberedInformationFrame(
            destination=telecommands.DST_CALLSIGN,
            source=telecommands.SRC_CALLSIGN,
            pid=0xf0,
            payload=payload)

        self.ax25int.transmit(frame)