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
    with open(filename, 'r') as file:
        data = file.read()
    dest += '/' + filename.split('/')[-1]
    packager.send_file(telecom, dest, data)
    return dest
