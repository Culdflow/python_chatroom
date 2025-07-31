import server
import keys
import UI

SERVER = "192.168.1.29"
PORT = 5050

public_key = 0
private_key = 0

try:
    server.start((SERVER, PORT))
    public_key, private_key = keys.create_keys()
    server.public_key = public_key
    server.private_key = private_key
    UI.chat_window()
except:
    print("SERVER ERROR")

"""
    TODO:
        -create socket and bind it to port ip
        -create keys
        -launch GUI
        -connect received messages to GUI
"""
