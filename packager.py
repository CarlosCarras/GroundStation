#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : February 21, 2021
@description : creates the KISS frame
'''

import telecommands

class Packager():
    def composeFrame(self, telecommand, params):
        telecommand = telecommands.Frame(telecommand, params)
