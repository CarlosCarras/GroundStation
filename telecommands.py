
FEND = 0xC0

class Packet():
    def __init__(self, telecom, params):
        self.telecom = telecom
        self.params = params

class Frame():
    def __init__(self, telecom, params):
        self.begin = FEND
        #self.
        self.telecom = telecom
        self.params = params
        self.end = FEND