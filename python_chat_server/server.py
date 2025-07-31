import UI
import utils

import socket
import threading
import signal
import errno
import os
import sys
import rsa
import base64
from cryptography.fernet import Fernet
from colorama import Fore

sys.setrecursionlimit(100000)

public_key = 0
private_key = 0

PORT = 5050
SERVER = "192.168.1.29"
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED111"
CONNECTED_MESSAGE = "CONNECTED111"
CONNECTION_REFUSED = "CONNECTION REFUSED111"
LOGIN_SUCCESSFUL = "LOGIN SUCCESSFUL111"
SEND_MSG_LIST = "SEND MESSAGE LIST111"
ERROR_RECEIVING_MESSAGE = "ERROR RECV MSG111"

KEYS_PATH = "serverKeys/public.pem"

whitelist = {}
keys = {}
msg_list = []
private_msg_list = []

#receives message and decrypts it
def receive(conn, cred = "Anonymous User", encrypted = False):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        if encrypted:
            msg = conn.recv(msg_length).decode()
            msg = str_to_list(msg)
            sym_key = base64.b64decode(msg[0])
            sym_key = rsa.decrypt(sym_key, private_key)
            msg = base64.b64decode(msg[1])
            sym_key = Fernet(sym_key)
            msg = sym_key.decrypt(msg).decode(FORMAT)
        else: 
            msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            print(f"{Fore.BLUE}[DISCONNECT]{Fore.CYAN} {cred} {Fore.BLUE}Disconnected{Fore.WHITE}")
            conn.close()
            return 0
        return msg
    print(f"{Fore.RED}[ERROR RECEIVING MESSAGE]{Fore.WHITE}")
    return ERROR_RECEIVING_MESSAGE


#sends message and encrypts it based on encrypted
def send(conn, addr, message, encrypted = True):
    if encrypted:
        sym_key = create_sym_keys()
        key_to_encrypt = Fernet(sym_key)
        send_message = key_to_encrypt.encrypt(message.encode(FORMAT))
        send_message = base64.b64encode(send_message).decode(FORMAT)
        send_key = rsa.encrypt(sym_key, keys[addr])
        send_key = base64.b64encode(send_key).decode()
        send_message = str([send_key, send_message]).encode()
    else:
        send_message = message.encode(FORMAT)
    send_length = str(len(send_message)).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(send_message)

#handles client
def handle_client(conn, addr):
    try:
        keys[addr] = receive(conn)
        keys[addr] = utils.convert_str_publicKey(keys[addr])
        send(conn, addr, str(public_key), False)
        credentials = receive(conn, "Anonymous User", True)
        if credentials == ERROR_RECEIVING_MESSAGE:
            print(f"{Fore.RED}[ERROR RECEIVING MESSAGE]{Fore.WHITE}")
        cred = credentials.split(":")
        if check_whitelist(cred[0], cred[1]):
            send(conn, addr, LOGIN_SUCCESSFUL)
            connected = True
            print(f"{Fore.BLUE}[CONNECTED]{Fore.CYAN} {cred[0]} {Fore.BLUE}Connected{Fore.WHITE}")
        else:
            send(conn, addr, CONNECTION_REFUSED)
            return handle_client(conn, addr)
        msg_list.append([cred[0],CONNECTED_MESSAGE])
        while connected:
            msg = receive(conn, cred[0], True)
            if msg == 0:
                return 0
            if msg == SEND_MSG_LIST:
                send(conn, addr, make_msg_list())
            else:
                msg_list.append([cred[0], msg])
                check_lists()
    except socket.error:
        print(f"{Fore.RED}[SOCKET ERROR] Terminating connection for {Fore.CYAN}{cred[0]}{Fore.RED}...{Fore.WHITE}")
        conn.close()
        return 0
    conn.close()
    return 0

#this will be removed with UI
def take_input():
    while True:
        message = input()
        print('\033[1A\033[K\033[1A')
        msg_list.append(["Admin", message])

#checks if new messages are available but it is very ugly
def check_lists():
    if private_msg_list != msg_list:
        print_messages()  

#starts server and daemons 
def start(ADDR):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"{Fore.GREEN}[OPEN] Server is listening on {SERVER}{Fore.WHITE}")
    checklist = threading.Thread(target=check_lists)
    checklist.daemon = True
    checklist.start()
    fun_input = threading.Thread(target=take_input)
    fun_input.daemon = True
    fun_input.start()
        
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()
        send(conn, addr, CONNECTED_MESSAGE, False)
        print(f"{Fore.GREEN}[ACTIVE CONNECTIONS] {Fore.WHITE}{threading.active_count() - 1}")

#will be modified with UI
def print_messages():
    global msg_list, private_msg_list
    for i in range(len(msg_list)):
        if msg_list[i][0] == "Admin":
            fore = f"{Fore.RED}"
        else:
            fore = f"{Fore.BLUE}"
        if i >= len(private_msg_list):
            UI.print_message(msg_list[i][0], msg_list[i][1])     
        else:
            if msg_list[i] != private_msg_list[i]:
                UI.print_message(msg_list[i][0], msg_list[i][1])      
    private_msg_list = msg_list.copy()

#Needs to be in main but also not very significant
def exit_gracefully(signum, frame):
    print('\r', end ='')
    print(f"{Fore.GREEN}[QUITTING]...{Fore.WHITE}")
    server.close()
    exit()
#needs to be in main too
if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

#create_keys()
#print(f"{Fore.GREEN}[STARTING] Server is starting...{Fore.WHITE}")
#start()

