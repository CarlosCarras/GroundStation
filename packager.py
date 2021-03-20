#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : March 19, 2021
@description : creates the KISS frame
'''

import telecommands
#import kamxl

DATAFIELD_LEN = 256
BUF_LEN = DATAFIELD_LEN - 1
TRANSMIT_PREAMBLE = 0x1ACF

def getNumPackets(data):
    return (len(data) - 1)// BUF_LEN + 1

def getChecksum(str):
    sum = 0
    n = len(str)

    for i in range(n):
        sum += ord(str[i])

    return sum % DATAFIELD_LEN


def send_telecom(telecom, data):
    n = getNumPackets(data)
    for i in range(n):
        print("Packet Number: " + str(i))
        outbound = chr(telecom) + data[i*BUF_LEN:(i+1)*BUF_LEN]
        send_packet(outbound)

def send_packet(outbound):
    preamble = chr(TRANSMIT_PREAMBLE >> 8) + chr(TRANSMIT_PREAMBLE & 0xFF)
    data_len = chr(len(outbound))
    data = outbound
    checksum = chr(getChecksum(outbound))

    packet = preamble + data_len + data + checksum
    # kamxl.write(packet)
    print(packet)