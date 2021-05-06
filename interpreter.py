import telecommands

def handle(response):
    telecom = ord(response[0])
    data = response[1:]

    if (data == telecommands.ACKNOWLEDGE):
        print("Success!")

    print("Response Telecommand: " + chr(telecom))
    print("Response Data: " + data)