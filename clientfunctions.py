import socket
import select
import errno
import sys
from Cryptodome.Cipher import AES
from base64 import b64encode, b64decode

class Crypt:

    def __init__(self, salt='SlTeRlOHpygTYkP3'):
        self.salt = salt.encode('utf8')
        self.enc_dec_method = 'utf-8'

    def encrypt(self, str_to_enc, str_key):
        try:
            aes_obj = AES.new(str_key.encode('utf-8'), AES.MODE_CFB, self.salt)
            hx_enc = aes_obj.encrypt(str_to_enc.encode('utf8'))
            mret = b64encode(hx_enc).decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Encryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Encryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)

    def decrypt(self, enc_str, str_key):
        try:
            aes_obj = AES.new(str_key.encode('utf8'), AES.MODE_CFB, self.salt)
            str_tmp = b64decode(enc_str.encode(self.enc_dec_method))
            str_dec = aes_obj.decrypt(str_tmp)
            mret = str_dec.decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Decryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Decryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)


HEADER_LENGTH = 10

class bcolors:
    """Colors for formatting console outputs"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def new_socket(IP, PORT):
    """Creates new socket at given PORT of IP"""
    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to a given ip and port
    client_socket.connect((IP, PORT))

    # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
    client_socket.setblocking(False)

    return client_socket

def credential_login(socket1, my_username, my_password, ClientKey):
    crpt = Crypt()

    # Prepare username and header and send them
    # We need to encode username to bytes, then count number of bytes and prepare 
    # header of fixed size, that we encode to bytes as well
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    socket1.send(username_header + username)

    pwd = crpt.encrypt(my_password, ClientKey).encode('utf-8')
    pwd_header = f"{len(pwd):<{HEADER_LENGTH}}".encode('utf-8')
    socket1.send(pwd_header + pwd)

if __name__ == "__main__":
    print("Hello World")
    test_crpt = Crypt()
    test_text = """Lorem ipsum dolor sit amet"""

    
    test_key = 'MyKey4TestingYnP'
    test_enc_text = test_crpt.encrypt(test_text, test_key)
    test_dec_text = test_crpt.decrypt(test_enc_text, test_key)
    print(f'Encrypted:{test_enc_text}  Decrypted:{test_dec_text}')
    print(type(test_enc_text))

