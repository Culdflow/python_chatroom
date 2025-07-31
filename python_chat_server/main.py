import client
import keys
import utils
import UI
import threading
import PySimpleGUI as sg

is_client = True
public_key = 0
private_key = 0
server_key = 0

while True:
    if client.connect():
        public_key, private_key = keys.create_keys()
        if client.login():
            UI.chat_window()
            receive_thread = threading.Thread(target = client.print_message())
            receive_thread.daemon = True
            receive_thread.start()
    else:
        sg.popup("Server closed or nonexistant")


"""
        TO-DO:

            -MAKE CHATROOM WORK WITH UI
            -ADD FILE TRANSFER

"""
