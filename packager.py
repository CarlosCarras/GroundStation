#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : February 21, 2021
@description : creates the KISS frame
'''

import telecommands
#import kamxl

def send_packet(packet):
    text = packet.telecom + packet.params
    #kamxl.write(text)
    print(text)
