import telecommands
import app_utils

def interpret(response):
    code = ord(response[0])
    data = response[1:]

    response_win = app_utils.open_window("Response")
    app_utils.create_dictionary(response_win, "Response Code: ", chr(code))
    app_utils.create_dictionary(response_win, "Response Data: ", data)

    if (code == telecommands.ACKNOWLEDGE):
        print("Success!")

    print("Response Code: " + chr(code))
    print("Response Data: " + data)