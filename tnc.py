import kamxl

DEBUG_CNT = 0

tnc = kamxl.KAMXL_TNC()

def read():
    # return tnc.read()

    # for debugging only
    global DEBUG_CNT
    if DEBUG_CNT < 2:
        DEBUG_CNT += 1
        return None
    DEBUG_CNT = 0
    return "Testing!"

def write(outbound):
    # tnc.write(outbound)

    # for debugging only
    print(outbound)