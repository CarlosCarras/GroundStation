#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : February 21, 2021
@modified    : May  11, 2021
@description : creates the KISS frame
'''

import telecommands
import app_utils
import listener
import time
import tnc

DATAFIELD_LEN = 256

SUCCESS = "Packet Success"
FAILURE = "Packet Failure"
SUCCESS_COLOR = 'green3'
FAILURE_COLOR = 'red'


def send_telecom(telecom, params):
    # creating progress bar GUI
    progress_win = app_utils.open_busywindow("Sending Packets")
    progress_txt = app_utils.create_label(progress_win, text="Sending Telecommand")
    progress_bar = app_utils.open_progressbar(progress_win)

    # transmitting packet
    outbound = chr(telecom) + params[0:DATAFIELD_LEN-1]
    app_utils.increment_progressbar(progress_win, progress_bar)
    response = send_packet(progress_win, outbound)
    status = get_status(response)
    status_label = display_status(progress_win, status)
    time.sleep(1)

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
    n = get_num_packets(len_dest, len_data)

    #creating progress bar GUI
    progress_win = app_utils.open_busywindow("Sending Packets")
    progress_txt = app_utils.create_label(progress_win, text="Sending Packet Number: 1")
    progress_bar = app_utils.open_progressbar(progress_win)
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
    app_utils.increment_progressbar(progress_win, progress_bar, inc)
    status = get_status(response)
    status_label = display_status(progress_win, status)

    time.sleep(1)
    if status == FAILURE:
        progress_win.destroy()
        return response

    # sending the remaining packets
    data += chr(telecommands.EOF)
    i = 0
    cnt_since_failure = 0
    while i < n-1:
        packet_num = i+2
        start = i*(DATAFIELD_LEN-2) + first_packet_data_len
        end = start + (DATAFIELD_LEN-2)
        outbound = chr(telecom) + chr(packet_num) + data[start:end]

        print("Sending Packet Number: " + str(packet_num))
        progress_txt.config(text="Sending Packet Number: " + str(packet_num))
        status_label.destroy()
        response = send_packet(progress_win, outbound)
        status = get_status(response)
        status_label = display_status(progress_win, status)

        if status == SUCCESS:
            app_utils.increment_progressbar(progress_win, progress_bar, inc)
            i += 1
            cnt_since_failure = 0
        else:
            cnt_since_failure += 1
            if (cnt_since_failure > 4):
                progress_win.destroy()
                return response

        time.sleep(1)

    # cleanup
    progress_win.destroy()

    return response


'''
  First Packet:
  Bytes:        1      |      1        |       1           |  0-253 |
           telecommand | packet number | number of packets |  data  |
 
 
  Other Packets:
  Bytes:        1      |      1        |  1-254 |
           telecommand | packet number |  data  |
 
'''
def get_file(telecom, dest):
    # creating progress bar GUI for transmission
    progress_win = app_utils.open_busywindow("Sending Packets")
    progress_txt = app_utils.create_label(progress_win, text="Waiting for Packet Number: 1")
    progress_win.lift()
    progress_bar = app_utils.open_progressbar(progress_win)

    # waiting for response: first packet
    outbound = chr(telecom) + dest
    app_utils.increment_progressbar(progress_win, progress_bar)
    response = send_packet(progress_win, outbound)
    status = get_status(response)
    status_label = display_status(progress_win, status)
    time.sleep(0.25)
    status_label.destroy()
    app_utils.increment_progressbar(progress_win, progress_bar, -1)         # reset progressbar
    time.sleep(0.25)

    # parsing response of first packet
    if not response:
        progress_win.destroy()
        return chr(telecommands.TELECOM_PACKET_LOSS)
    if (len(response) < 4):
        progress_win.destroy()
        return chr(telecommands.TELECOM_PACKET_FORMAT_ERR)                  # no packet should be shorter than 4 bytes
    if(response[1] != chr(1)):
        progress_win.destroy()
        return chr(telecommands.TELECOM_PACKET_LOSS)                        # packet #1 expected
    n = response[2]                                                         # number of packets
    contents = response[3:]

    inc = 100 / n
    app_utils.increment_progressbar(progress_win, progress_bar, inc)
    time.sleep(1)

    # waiting for response: remaining packets
    i = 0
    cnt_since_failure = 0
    while i < (n-1):
        packet_num = i+1
        print("Waiting on Packet Number: " + str(packet_num))
        progress_txt.config(text="Waiting on Packet Number: " + str(packet_num))
        status_label.destroy()
        response = listener.wait(progress_win)
        log_inbound(response)
        status = get_status(response)
        status_label = display_status(progress_win, status)

        if status == SUCCESS:
            app_utils.increment_progressbar(progress_win, progress_bar, inc)
            i += 1
            cnt_since_failure = 0
        else:
            cnt_since_failure += 1
            if (cnt_since_failure > 4):
                progress_win.destroy()
                return response

        if ord(response[1]) != i+1:
            progress_win.destroy()
            return chr(telecommands.TELECOM_PACKET_LOSS)

        contents += response[2:]
        time.sleep(1)

    # cleanup
    progress_win.destroy()

    return contents


#------------------------------- Supplementary -------------------------------#

def get_num_packets(len_dest, len_data):
    eff_len = len_dest + len_data + 4  # effective length = (length of dest) + (length of data) + 4 bytes for overhead (NUM_PACKETS, DEST_LEN, SOF, EOF)
    return (eff_len - 1) // (DATAFIELD_LEN - 2) + 1  # 256 bytes (in AX.25 frame) - 1 byte (telecom), - 1 byte (packet number) = 254 bytes


def get_status(response):
    if response is None:
        return FAILURE
    if response[0] == chr(telecommands.ACKNOWLEDGE):
        return SUCCESS
    return FAILURE


def display_status(win, status):
    if status == SUCCESS:
        status_color = SUCCESS_COLOR
    else:
        status_color = FAILURE_COLOR

    label = app_utils.create_label(win, text=status, color=status_color)
    return label


def send_packet(win, outbound):
    tnc.write(outbound)
    log_outbound(outbound)
    response = listener.wait(win)
    log_inbound(response)

    return response


def log_outbound(outbound):
    telecom_log = open("assets/D3Outbound.log", 'a', encoding="utf-8")
    local_time = time.ctime(time.time())
    telecom_log.write(local_time + ">> " + outbound+'\n')
    telecom_log.close()


def log_inbound(inbound):
    if not inbound: return

    telecom_log = open("assets/D3Inbound.log", 'a', encoding="utf-8")
    local_time = time.ctime(time.time())
    telecom_log.write(local_time + ">> " + inbound+'\n')
    telecom_log.close()