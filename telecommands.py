SRC_CALLSIGN = 'W2GMD-14'
DST_CALLSIGN = 'PYKISS'

FEND = 0xC0

CSV_START = chr(0xB9)
CSV_END = chr(0xC9)

TELECOM_UPDATEGUIDANCE = chr(0x27)

class Packet():
    def __init__(self, telecom, params):
        self.telecom = telecom
        self.params = params
