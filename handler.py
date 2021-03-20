#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : March 4, 2021
@modified    : March 19, 2021
@description : handles telecommand transmission
'''

import packager
import telecommands

def send_telecom(telecom, param="\0"):
    packager.send_telecom(telecom, param)

def transfer_file(telecom, filename, dest):
    data = chr(len(dest))
    data += dest
    data += chr(telecommands.SOF)
    with open(filename, 'r') as file:
        data += file.read()
    data += chr(telecommands.EOF)

    packager.send_telecom(telecom, data)
