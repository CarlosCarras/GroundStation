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

def getNumPackets(len_dest, len_data):
    eff_len = len_dest + len_data + 4                # effective length = (length of dest) + (length of data) + 4 bytes for overhead (NUM_PACKETS, DEST_LEN, SOF, EOF)
    return (eff_len - 1) // (DATAFIELD_LEN - 2) + 1  # 256 bytes (in AX.25 frame) - 1 byte (telecom), - 1 byte (packet number) = 254 bytes

def send_telecom(telecom, params):
    outbound = chr(telecom) + params[0:DATAFIELD_LEN-1]
    send_packet(outbound)

'''
First Packet Params Field:
   Bytes:   |      1        |       1           |              1              |    1-251    |  1  |  0-250 |
            | packet number | number of packets | length of destination field | destination | SOF |  data  |
   
   NOTE: Start of File (SOF) must be in the first packet.
         
Other Packets Params Field:
   Bytes:   |      1        |  1-254 |  1  |
            | packet number |  data  | EOF |

   NOTE: End of File (EOF) must be in the last packet.
'''
def send_file(telecom, dest, data):
    len_data = len(data)
    len_dest = len(dest)
    n = getNumPackets(len_dest, len_data)

    # sending the first packet
    outbound = chr(telecom) + chr(1) + chr(n) + chr(len_dest) + dest + chr(telecommands.SOF)
    len_outbound = len(outbound)
    first_packet_data_len = DATAFIELD_LEN-len_outbound
    if (len_outbound > DATAFIELD_LEN):
        print("Error: The length of the destination directory is longer than the perimissible length of 251.")
        return
    elif (len_outbound < DATAFIELD_LEN):
        outbound += data[0:first_packet_data_len]
    print("Sending Packet Number: 1")
    send_packet(outbound)

    # sending the remaining packets
    data += chr(54)#telecommands.EOF)
    for i in range(n-1):
        start = i*(DATAFIELD_LEN-2) + first_packet_data_len
        end = start + (DATAFIELD_LEN-2)
        outbound = chr(telecom) + chr(i+2) + data[start:end]
        print("Sending Packet Number: " + str(i+2))
        send_packet(outbound)

def send_packet(outbound):
    # kamxl.write(packet)
    print(outbound)