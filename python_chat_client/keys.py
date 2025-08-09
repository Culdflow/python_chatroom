import os
import rsa
from colorama import Fore
from cryptography.fernet import Fernet

KEYS_PATH = "keys/public.pem"


#generating or importing keys if already present
def create_keys():
    if os.path.isfile(KEYS_PATH):
        print(f"{Fore.GREEN}[LOADING KEYS]...{Fore.WHITE}")
        with open("serverKeys/public.pem", "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
        with open("serverKeys/private.pem", "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
        print(f"{Fore.GREEN}[KEYS LOADED]{Fore.WHITE}")
    else:
        print(f"{Fore.GREEN}[GENERATING KEYS]...{Fore.WHITE}")
        if not os.path.isdir("serverKeys"):
            os.mkdir("serverKeys")
        public_key, private_key = rsa.newkeys(1024)
        with open("serverKeys/public.pem", "wb") as f:
            f.write(public_key.save_pkcs1("PEM"))
        with open("serverKeys/private.pem", "wb") as f:
            f.write(private_key.save_pkcs1("PEM"))
        print(f"{Fore.GREEN}[KEYS GENERATED]{Fore.WHITE}")
    return (public_key, private_key)

#creates symmetric key
def create_sym_keys():
    sym_keys = Fernet.generate_key()
    return sym_keys


