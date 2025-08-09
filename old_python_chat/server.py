import socket
import threading
import signal
import errno
import sys
from colorama import Fore

sys.setrecursionlimit(100000)

PORT = 1948
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED"
FIRST_CONNECTION = "FIRST CONNECTION"
CONNECTED_MESSAGE = "CONNECTED"
CONNECTION_REFUSED = "CONNECTION REFUSED"
LOGIN_SUCCESSFUL = "LOGIN SUCCESSFUL"
SEND_MSG_LIST = "SEND MESSAGE LIST"

whitelist = {}
msg_list = []
private_msg_list = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def check_whitelist(usr, pswd):
	whitelist_file = open("whitelist.txt", "r")
	content = whitelist_file.read()
	content_split = content.split("\n")
	for i in content_split:
		if i != "":
			split = i.split(":")
			whitelist[split[0]] = split[1]
	whitelist_file.close()
	if usr in whitelist.keys():
		if whitelist[usr] == pswd:
			return True
	return False

def make_msg_list():
	result = ""
	for i in msg_list:
		result += i[0] + ":" + i[1] + ";"
	return result

def	disconnect(conn, cred):
	conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
	conn.close()
	print(f"{Fore.BLUE}[DISCONNECT]{Fore.CYAN} {cred[0]} {Fore.BLUE}Disconnected{Fore.WHITE}")

def	handle_client(conn, addr):
	cred = ["anonymous", ""]
	try:
		conn.send(CONNECTED_MESSAGE.encode(FORMAT))
		credentials = conn.recv(HEADER).decode(FORMAT)
		if credentials == DISCONNECT_MESSAGE:
			disconnect(conn, cred)
			return 0
		cred = credentials.split(":")
		if check_whitelist(cred[0], cred[1]):
			conn.send(LOGIN_SUCCESSFUL.encode(FORMAT))
			connected = True
			print(f"{Fore.BLUE}[CONNECTED]{Fore.CYAN} {cred[0]} {Fore.BLUE}Connected{Fore.WHITE}")
		else:
			conn.send(CONNECTION_REFUSED.encode(FORMAT))
			return handle_client(conn, addr)
		msg_list.append([cred[0],CONNECTED_MESSAGE])
		while connected:
			msg_length = conn.recv(HEADER).decode(FORMAT)
			if msg_length:
				msg_length = int(msg_length)
				msg = conn.recv(msg_length).decode(FORMAT)
				if msg == DISCONNECT_MESSAGE:
					disconnect(conn, cred)
					connected = False
				if msg == SEND_MSG_LIST:
					message_list_send = make_msg_list().encode(FORMAT)
					length = len(message_list_send)
					send_length = str(length).encode(FORMAT)
					send_length += b' ' * (HEADER - len(send_length))
					conn.send(send_length)
					conn.send(message_list_send)
				else:
					msg_list.append([cred[0], msg])
	except:
		print(f"{Fore.RED}[ERROR] Terminating connection for {Fore.CYAN}{cred[0]}{Fore.RED}...{Fore.WHITE}")
	conn.close()
	return 0

def take_input():
	while True:
		message = input()
		print('\033[1A\033[K\033[1A')
		msg_list.append(["Admin", message])

def check_lists():
	global msg_list, private_msg_list
	while True:
		if private_msg_list != msg_list:
			print_messages()  

def start():
	global private_msg_list, msg_list
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
		print(f"{Fore.GREEN}[ACTIVE CONNECTIONS] {Fore.WHITE}{threading.active_count() - 2}")

def print_messages():
    global msg_list, private_msg_list
    for i in range(len(msg_list)):
        if msg_list[i][0] == "Admin":
            fore = f"{Fore.RED}"
        else:
            fore = f"{Fore.BLUE}"
        if i >= len(private_msg_list):
            print(f"{fore}[{msg_list[i][0]}]   {Fore.WHITE}{msg_list[i][1]}")
        else:
            if msg_list[i] != private_msg_list[i]: 
                print(f"{fore}[{msg_list[i][0]}]   {Fore.WHITE}{msg_list[i][1]}")
    private_msg_list = msg_list.copy()

def exit_gracefully(signum, frame):
    print('\r', end ='')
    print(f"{Fore.GREEN}[QUITTING]...{Fore.WHITE}")
    server.close()
    exit()

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

print(f"{Fore.GREEN}[STARTING] Server is starting...{Fore.WHITE}")
start()

