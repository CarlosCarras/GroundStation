#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : March 4, 2021
@modified    : March 4, 2021
@description : handles telecommand transmission
'''

import packager
import telecommands

def send_telecom(telecom, param=None):
    packet = telecommands.Packet(telecom, param)
    packager.send_packet(packet)

def transfer_file(telecom, filename):
    data = telecommands.CSV_START
    with open(filename, 'r') as file:
        data += file.read()
    data += telecommands.CSV_END

    send_telecom(telecom, data)
