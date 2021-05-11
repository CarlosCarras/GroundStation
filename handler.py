#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : March 4, 2021
@modified    : May 6, 2021
@description : handles telecommand transmission
'''

import packager


def send_telecom(telecom, param=''):
    response = packager.send_telecom(telecom, param)
    return response


def transfer_file(telecom, filename, dest):
    with open(filename, 'r') as file:
        data = file.read()
    dest += '/' + filename.split('/')[-1]
    response = packager.send_file(telecom, dest, data)
    return response
