import client
import keys
import utils
import threading
from colorama import Fore

is_client = True
public_key = 0
private_key = 0
server_key = 0

while True:
	if client.connect():
		public_key, private_key = keys.create_keys()
		client.public_key = public_key
		client.private_key = private_key
		if client.login():
			receive_thread = threading.Thread(target = client.print_message())
			receive_thread.daemon = True
			receive_thread.start()
			client.send_message()
	else:
		print(f"{Fore.RED}[QUITTING]Server closed or nonexisting")


"""
        TO-DO:

            -MAKE CHATROOM WORK WITH UI
            -ADD FILE TRANSFER

"""
