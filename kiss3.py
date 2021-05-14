#!/usr/bin/env python

'''
@author      : Carlos Carrasquillo
@created     : May 14, 2021
@modified    : May 14, 2021
@description : library that composes a KISS packet and transmits it over serial

@disclosure  : This code is a heavily stripped-down version of that found on 'https://github.com/ampledata/kiss'. Huge
               thank you to all of the contributors to that module.
'''

import serial
import time

#------------- Special Characters -------------#
FEND  = b'\xC0'
FESC  = b'\xDB'
TFEND = b'\xDC'
TFESC = b'\xDD'

FESC_TFEND = b''.join([FESC, TFEND])
FESC_TFESC = b''.join([FESC, TFESC])

#--------------- Command Codes ----------------#
DATA_FRAME   = b'\x00'
TX_DELAY     = b'\x01'
PERSISTENCE  = b'\x02'
SLOT_TIME    = b'\x03'
TX_TAIL      = b'\x04'
FULL_DUPLEX  = b'\x05'
SET_HARDWARE = b'\x06'
EXIT_KISS    = b'\xFF'

#---------------- Frame Class -----------------#
class Frame():
    def __init__(self):
        self._source = ""
        self._dest = ""
        self.text = ""

    def set_source(self, callsign):
        if valid_callsign(callsign):
            self._source = callsign
        else:
            print("ERROR: The callsign of the source is invalid.")

    def set_dest(self, callsign):
        if valid_callsign(callsign):
            self._dest = callsign
        else:
            print("ERROR: The callsign of the destination is invalid.")

    @property
    def source(self):
        return self._source

    @property
    def dest(self):
        return self._dest

#-------------- SerialKISS Class --------------#
class SerialKISS():
    def __init__(self, port, speed):
        self._port = port
        self._speed = speed
        self._interface = None

    def start(self):
        self._interface = serial.Serial(self._port, self._speed)
        self._interface.timeout = 0.01

    def write(self, frame: Frame):
        if not frame._source:
            print("ERROR: The callsign of the source has not been properly set.")
        if not frame._dest:
            print("ERROR: The callsign of the destination has not been properly set.")
        if not frame.text:
            print("INFO: Nothing to send.")
            return

        frame_str = frame.source + '>' + frame.dest + ':' + frame.text
        escaped_frame = escape_special_codes(frame_str)
        frame_kiss = b''.join([FEND, DATA_FRAME, escaped_frame, FEND])
        self._interface.write(frame_kiss)

    def read_handler(self):
        read_data = self._interface.read(1000)
        try:
            waiting_data = self._interface.in_waiting
        except AttributeError:
            waiting_data = self._interface.outWaiting()

        if waiting_data:
            read_data += self._interface.read(waiting_data)
        return read_data

    def read(self):
        read_buffer = bytes()

        while 1:
            read_data = self.read_handler()

            if read_data is not None and len(read_data):
                frames = []
                split_data = read_data.split(FEND)
                fends = len(split_data)

                if fends == 1:
                    # no FEND in frame
                    read_buffer += split_data[0]
                elif fends == 2:
                    # single FEND in frame
                    if split_data[0]:
                        # closing FEND found
                        frames.append(b''.join([read_buffer, split_data[0]]))    # partial frame continued, otherwise drop
                        read_buffer = bytes()
                    else:
                        # opening FEND found
                        frames.append(read_buffer)
                        read_buffer = split_data[1]

                elif fends >= 3:
                    # at least one complete frame received: [FEND, xxx, FEND]

                    # iterate through split_data and extract just the frames.
                    for i in range(0, fends - 1):
                        buf = bytearray(b''.join([read_buffer, split_data[i]]))
                        if buf:
                            frames.append(buf)
                            read_buffer = bytearray()

                frames = [_f for _f in frames if _f]      # remove None frames
                log(frames)

                return frames

#----------------- Utilities ------------------#

def valid_callsign(callsign):
    callsign = callsign.lstrip().rstrip().strip('*')

    if '-' in callsign:
        if not callsign.count('-') == 1:
            return False
        else:
            callsign, ssid = callsign.split('-')
    else:
        ssid = 0

    # callsign should be <6
    if (len(callsign) < 2 or len(callsign) > 6 or len(str(ssid)) < 1 or
            len(str(ssid)) > 2):
        return False

    for char in callsign:
        if not (char.isalpha() or char.isdigit()):
            if char != '*' or callsign[-1] != '*':
                return False

    if not str(ssid).isdigit():
        return False

    if int(ssid) < 0 or int(ssid) > 15:
        return False

    return True


def escape_special_codes(raw_codes):
    return raw_codes.encode('utf-8').replace(
        FESC,
        FESC_TFESC
    ).replace(
        FEND,
        FESC_TFEND
    )


def recover_special_codes(escaped_codes):
    return escaped_codes.encode('utf-8').replace(
        FESC_TFESC,
        FESC
    ).replace(
        FESC_TFEND,
        FEND
    )


def log(frames):
    if not frames: return

    log = open("assets/D3Raw.log", 'a', encoding="utf-8")
    for i in frames:
        local_time = time.ctime(time.time())
        log.write(local_time + ">> " + i + '\n')
        log.close()

