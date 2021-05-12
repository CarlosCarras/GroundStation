import telecommands
import app_utils

def interpret(response):
    if response is None:
        response_win = app_utils.open_window("Response")
        app_utils.create_dictionary(response_win, "Response Code: ", "0x00")
        app_utils.create_dictionary(response_win, "Response Data: ", "No response received.")
        return

    code = hex(ord(response[0]))

    if len(response) > 1:
        data = response[1:]
    else:
        data = ""

    response_win = app_utils.open_window("Response")
    app_utils.create_dictionary(response_win, "Response Code: ", code)
    app_utils.create_dictionary(response_win, "Response Data: ", data)

    if (code == telecommands.ACKNOWLEDGE):
        print("Success!")

    print("Response Code: " + str(code))
    print("Response Data: " + data)