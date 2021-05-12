#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : March 4, 2021
@modified    : May 6, 2021
@description : handles telecommand transmission
'''

import tnc
import packager


def send_telecom(telecom, param=''):
    tnc.read()      # clear buffer of all irrelevant packages
    response = packager.send_telecom(telecom, param)
    return response


def uplink_file(telecom, filename, dest):
    tnc.read()      # clear buffer of all irrelevant package
    with open(filename, 'r') as file:
        data = file.read()
    dest += '/' + filename.split('/')[-1]
    response = packager.send_file(telecom, dest, data)
    return response


def downlink_file(telecom, dest):
    tnc.read()      # clear buffer of all irrelevant package
    response = packager.get_file(telecom, dest)
    return response
