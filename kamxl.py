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
        self.rxbuf = []
        self.src = telecommands.SRC_CALLSIGN
        self.dst = telecommands.DST_CALLSIGN

        self.kissdev = SerialKISSDevice(
            device='/dev/ttyS0',
            baudrate=9600,
            log=logging.getLogger('./assets/D3_KISS.log'))

        self.ax25int = AX25Interface(
            kissport= self.kissdev[0],
            log=logging.getLogger('./assets/D3_AX25.log'))

        self.ax25int.bind(
            callback=self.read,
            callsign=self.dst,
            ssid=None)

        self.kissdev.open()

    def read(self, interface, frame, **kwargs):
        payload = frame.payload
        print(payload)
        self.rxbuf.append(payload)

    def write(self, text):
        payload = bytes(text, 'utf-8')

        print(payload)
        frame = AX25UnnumberedInformationFrame(
            destination=self.dst,
            source=self.src,
            pid=0xf0,
            payload=payload)

        print(frame)
        self.ax25int.transmit(frame)