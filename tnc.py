#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : May 14, 2021
@modified    : May 14, 2021
@description : wrapper class for the KAM XL TNC
'''

import kamxl
import time

DEBUG_CNT = 0

tnc = kamxl.KAMXL_TNC()
tnc_buffer = []

def read():
    # frames = tnc.read()
    # tnc_buffer.append(frames)
    #
    # if tnc_buffer:
    #     return tnc_buffer.pop(0)
    # else:
    #     return None

    # for debugging only
    global DEBUG_CNT
    if DEBUG_CNT < 2:
        DEBUG_CNT += 1
        return None
    DEBUG_CNT = 0
    return "@Working!"

def write(outbound):
    # for debugging only
    print(outbound)
    tnc.write(outbound)