SRC_CALLSIGN = 'D3GND'
DST_CALLSIGN = 'D3SAT'

#---- Uplinked Commands ----#
TELECOM_UPLOAD_FILE	         = 0x79
TELECOM_GET_FILE             = 0x81
TELECOM_UNDO_UPLOAD          = 0xF5
TELECOM_GET_HISTORY          = 0x12
TELECOM_GET_HEALTH           = 0x4C
TELECOM_OVERRIDE_ANTENNA     = 0x6A
TELECOM_DEBUG_ON             = 0xE0
TELECOM_DEBUG_OFF            = 0x0F
TELECOM_DEBUG_TOGGLE         = 0x7A

#----  Downlinked Commands ----#
ACKNOWLEDGE                  = 0x40
TELECOM_LAST_PACKET_RECEIVED = 0x11
TELECOM_DOWNLINK_FILE		 = 0x45
TELECOM_DOWNLINK_STRING      = 0x46

#----  Downlinked Errors ----#
ERROR                        = 0x32
TELECOM_PACKET_LOSS          = 0xE6
TELECOM_PACKET_LOSS_RESET    = 0xE7
TELECOM_PACKET_FORMAT_ERR    = 0xE8
TELECOM_FILE_UNAVAILABLE     = 0xE9


SOF = 0x02
EOF = 0x03