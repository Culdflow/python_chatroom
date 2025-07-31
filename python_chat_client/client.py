import keys
import UI

import socket
import threading
import signal
import sys
import rsa
import os
import base64
from cryptography.fernet import Fernet
from colorama import Fore

sys.setrecursionlimit(100000)


client = 0


HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED111"
CONNECTED_MESSAGE = "CONNECTED111"
CONNECTION_REFUSED = "CONNECTION REFUSED111"
LOGIN_SUCCESSFUL = "LOGIN SUCCESSFUL111"
SEND_MSG_LIST = "SEND MESSAGE LIST111"
ERROR_RECEIVING_MESSAGE = "ERROR RECV MSG111"
BROKEN_PIPE = "BROKEN PIPE111"

ADDR = 0

PUBLIC_KEY = 0
PRIVATE_KEY = 0

USERNAME = ""
PASSWORD = ""

msg_list = []


#sends message and encrypts it
def send(msg, encrypted = True):
    try:
        if msg == "!exit":
            return send(DISCONNECT_MESSAGE)
        if encrypted:
            sym_key = keys.create_sym_keys()
            key_to_encrypt = Fernet(sym_key)
            message = key_to_encrypt.encrypt(msg.encode(FORMAT))
            message = base64.b64encode(message).decode(FORMAT)
            send_key = rsa.encrypt(sym_key, main.server_key)
            send_key = base64.b64encode(send_key).decode()
            message = str([send_key, message]).encode()
        else:
            message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        if msg == DISCONNECT_MESSAGE:
            signal.signal(signal.SIGINT, exit_gracefully)
    except BrokenPipeError:
        print(f"{Fore.RED}[BROKEN PIPES]Quitting...{Fore.WHITE}")
        signal.signal(signal.SIGINT, exit_gracefully)
        exit()
    except ValueError:
        print(f"{Fore.RED}[VALUE ERROR]Message not sent{Fore.WHITE}")

#receives message and decrypts it
def receive(encrypted = True):
    try:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            if encrypted:
                msg = client.recv(msg_length).decode()
                msg = str_to_list(msg)
                sym_key = base64.b64decode(msg[0])
                sym_key = rsa.decrypt(sym_key, private_key)
                msg = base64.b64decode(msg[1])
                sym_key = Fernet(sym_key)
                msg = sym_key.decrypt(msg).decode(FORMAT)
            else:    
                msg = client.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                signal.signal(signal.SIGINT, exit_gracefully)
            return msg
        print(f"{Fore.RED}[ERROR RECEIVING MESSAGE]{Fore.WHITE}")
        return ERROR_RECEIVING_MESSAGE
    except BrokenPipeError:
        print(f"{Fore.RED}[BROKEN PIPE]Nothing received{Fore.WHITE}")
        print(f"{Fore.RED}[QUITTING]...{Fore.WHITE}")
        return BROKEN_PIPE

#will be modified with UI
def login(i=0):
    global USERNAME, PASSWORD
    send(str(public_key), False)
    main.server_key = receive(False)
    main.server_key = convert_str_publicKey(main.server_key)
    USERNAME, PASSWORD = UI.login_popup(i == 0)
    credentials = USERNAME + ":" + PASSWORD
    send(credentials)
    cred_response = receive()
    if cred_response != LOGIN_SUCCESSFUL:
        if i == 2:
            send(DISCONNECT_MESSAGE)
            sg.popup("Too many failed login attempts")
            return False
        return login(i+1)
    return True


#will be modified with UI and needs to be in main or graphics.py
def print_message():
    global msg_list
    send(SEND_MSG_LIST)
    msg = receive()
    if msg == ERROR_RECEIVING_MESSAGE:
        return print_message()
    server_msg_list = utils.decode_msg_list(msg)
    if server_msg_list != msg_list:
        for i in range(len(server_msg_list)):
            if i >= len(msg_list) or server_msg_list[i] != msg_list[i]:
                UI.print_message(server_msg_list[i][0], server_msg_list[i][1])   
        msg_list = server_msg_list
    return print_message()


def connect():#connects to server
    global ADDR, client
    ADDR = UI.connect_popup()
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect(ADDR)
        client.settimeout(None)
        connected_message = receive(False)
        if connected_message == CONNECTED_MESSAGE:
            return True
        else:
            return False
    except:
        return False
 

def exit_gracefully(signum, frame):
    print('\r', end='')
    print(f"{Fore.GREEN}[QUITTING]...{Fore.WHITE}")
    send(DISCONNECT_MESSAGE)
    client.close()
    exit()

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)


