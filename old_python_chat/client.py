import keys
import socket
import threading
import signal
import sys
from colorama import Fore

sys.setrecursionlimit(100000)

PORT = 1948
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED"
CONNECTED_MESSAGE = "CONNECTED"
CONNECTION_REFUSED = "CONNECTION REFUSED"
LOGIN_SUCCESSFUL = "LOGIN SUCCESSFUL"
SEND_MSG_LIST = "SEND MESSAGE LIST"


SERVER = input(f"{Fore.GREEN}Server IP:{Fore.WHITE}  ")
ADDR = (SERVER, PORT)

USERNAME = ""
PASSWORD = ""

msg_list = []


def send(msg):
    if msg == "!exit":
        return send(DISCONNECT_MESSAGE)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def login(i=0):
    global USERNAME, PASSWORD
    USERNAME = input(f"{Fore.GREEN}[USERNAME]:   {Fore.WHITE}")
    PASSWORD = input(f"{Fore.GREEN}[PASSWORD]:   {Fore.WHITE}")
    credentials = USERNAME + ":" + PASSWORD
    client.send(credentials.encode(FORMAT))
    cred_response = client.recv(HEADER).decode(FORMAT)
    if cred_response != LOGIN_SUCCESSFUL:
        if i > 2:
            print(f"{Fore.RED}[LOGIN FAILED] Too many failed login attempts{Fore.WHITE}")
            print(f"{Fore.RED}Disconnecting...{Fore.WHITE}")
            client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            exit()
        print(f"{Fore.RED}[LOGIN FAILED] Try again...{Fore.WHITE}")
        return login(i+1)
    print(f"{Fore.GREEN}[LOGIN SUCCESSFUL] Logged in as:{Fore.WHITE} {USERNAME}")

def decode_msg_list(message_list):
    result = []
    message_list_split = message_list.split(";")
    message_list_split.pop()
    for i in message_list_split:
        split = i.split(":")
        result.append([split[0], split[1]])
    return result

def send_message():
    message = input()
    print ('\033[1A\033[K\033[1A')
    send(message)

def receive_msg():
    global msg_list
    send(SEND_MSG_LIST)
    thread = threading.Thread(target=send_message)
    thread.daemon = True
    thread.start()
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            client.close()
            exit()
        message_list = decode_msg_list(msg)
        if message_list != msg_list:
            for i in range(len(message_list)):
                if message_list[i][0] == USERNAME:
                    fore = f"{Fore.CYAN}"
                elif message_list[i][0] == "Admin":
                    fore = f"{Fore.RED}"
                else:
                    fore = f"{Fore.BLUE}"
                if i >= len(msg_list):
                    print(f"{fore}[{message_list[i][0]}]   {Fore.WHITE}{message_list[i][1]}")
                else:
                    if message_list[i] != msg_list[i]:
                        print(f"{fore}[{message_list[i][0]}]   {Fore.WHITE}{message_list[i][1]}")
            msg_list = message_list
    return receive_msg()

def exit_gracefully(signum, frame):
    print('\r', end='')
    print(f"{Fore.GREEN}[QUITTING]...{Fore.WHITE}")
    send(DISCONNECT_MESSAGE)
    client.close()
    exit()

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
connected_message = client.recv(HEADER).decode(FORMAT)
if connected_message == CONNECTED_MESSAGE:
    print(f"{Fore.GREEN}[CONNECTED]{Fore.WHITE}")
else:
    print(f"{Fore.RED}[CONNECTION FAILED]{Fore.WHITE}")
    exit()
login()


receive_msg()
send(DISCONNECT_MESSAGE)
