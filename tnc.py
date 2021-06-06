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
    # log(frames)
    # tnc_buffer.append(frames)
    #
    # if tnc_buffer:
    #     return tnc_buffer.pop(0)
    # return None

    # for debugging only
    global DEBUG_CNT
    if DEBUG_CNT < 4:
        DEBUG_CNT += 1
        return None
    DEBUG_CNT = 0
    return "@Working!"

def write(outbound):
    # for debugging only
    print(outbound)
    tnc.write(outbound)


def log(frames):
    if not frames: return

    log = open("assets/D3AllInbound.log", 'a', encoding="utf-8")
    for i in frames:
        local_time = time.ctime(time.time())
        log.write(local_time + ">> " + i + '\n')
        log.close()