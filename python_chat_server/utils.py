import rsa

#checks whitelist for user and passwd
def check_whitelist(usr, pswd):#this should go in utilities script
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

#converts string looking like a list to actual list
def str_to_list(string):#should go in utilities script
    string = string.replace("[","")
    string = string.replace("]","")
    return eval(string)

#converts string looking like public key to aactual public key
def convert_str_publicKey(key):#should go in utilities script
    key = key.replace("PublicKey", "")
    key = key.replace("(","")
    key = key.replace(")","")
    key = key.split(",")
    key = rsa.PublicKey(int(key[0]), int(key[1]))
    return key

#creates a message list for better communication between server and client
def make_msg_list():#should go in utilities
    result = ""
    for i in msg_list:
        result += i[0] + ":" + i[1] + ";"
    return result


def decode_msg_list(message_list):
    result = []
    message_list_split = message_list.split(";")
    message_list_split.pop()
    for i in message_list_split:
        split = i.split(":")
        result.append([split[0], split[1]])
    return result


