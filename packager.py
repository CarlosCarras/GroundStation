#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : May 6, 2021
@description : creates the KISS frame
'''

import telecommands
import app_utils
import listener
#import kamxl

DATAFIELD_LEN = 256

SUCCESS = "Packet Success"
FAILURE = "Packet Failure"
SUCCESS_COLOR = 'green3'
FAILURE_COLOR = 'red'

def getNumPackets(len_dest, len_data):
    eff_len = len_dest + len_data + 4                # effective length = (length of dest) + (length of data) + 4 bytes for overhead (NUM_PACKETS, DEST_LEN, SOF, EOF)
    return (eff_len - 1) // (DATAFIELD_LEN - 2) + 1  # 256 bytes (in AX.25 frame) - 1 byte (telecom), - 1 byte (packet number) = 254 bytes


def send_telecom(telecom, params):
    # creating progress bar GUI
    progress_win = app_utils.open_busywindow("Sending Packets")
    progress_txt = app_utils.create_label(progress_win, text="Sending Telecommand")
    progress_bar = app_utils.openProgressbar(progress_win)

    # transmitting packet
    outbound = chr(telecom) + params[0:DATAFIELD_LEN-1]
    app_utils.incrementProgressbar(progress_win, progress_bar)
    response = send_packet(progress_win, outbound)

    # cleanup
    progress_win.destroy()

    return response


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

    #creating progress bar GUI
    progress_win = app_utils.open_busywindow("Sending Packets")
    progress_txt = app_utils.create_label(progress_win, text="Sending Packet Number: 1")
    progress_bar = app_utils.openProgressbar(progress_win)
    inc = 100 / n

    # sending the first packet
    outbound = chr(telecom) + chr(1) + chr(n) + chr(len_dest) + dest + chr(telecommands.SOF)
    len_outbound = len(outbound)
    first_packet_data_len = DATAFIELD_LEN-len_outbound
    if (len_outbound > DATAFIELD_LEN):
        print("Error: The length of the destination directory is longer than the permissible length of 251.")
        return
    elif (len_outbound < DATAFIELD_LEN):
        outbound += data[0:first_packet_data_len]
    print("Sending Packet Number: 1")

    response = send_packet(progress_win, outbound)
    status_label = display_status(progress_win, response)

    # sending the remaining packets
    data += chr(telecommands.EOF)
    for i in range(n-1):
        packet_num = i+2
        start = i*(DATAFIELD_LEN-2) + first_packet_data_len
        end = start + (DATAFIELD_LEN-2)
        outbound = chr(telecom) + chr(packet_num) + data[start:end]

        print("Sending Packet Number: " + str(packet_num))
        progress_txt.config(text="Sending Packet Number: " + str(packet_num))
        status_label.destroy()
        response = send_packet(progress_win, outbound)
        status_label = display_status(progress_win, response)
        app_utils.incrementProgressbar(progress_win, progress_bar, inc)

    # cleanup
    progress_win.destroy()

    return response


def display_status(win, response, label=None):
    status = FAILURE
    status_color = FAILURE_COLOR

    if response:
        status = SUCCESS
        status_color = SUCCESS_COLOR

    label = app_utils.create_label(win, text=status, color=status_color)

    return label


def send_packet(win, outbound):
    # kamxl.write(packet)
    print(outbound)
    response = listener.wait(win)

    #to generate the output.txt file (telecommand testing)
    file1 = open('output.txt', 'a')
    file1.write(outbound+'\n')
    file1.close()

    return response