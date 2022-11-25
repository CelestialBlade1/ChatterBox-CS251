import socket
import select
import errno
import string
import random
import sys
from Cryptodome.Cipher import AES
from base64 import b64encode, b64decode

class Crypt:
    """A Class Encrypt and decrypt messages.

    """

    def __init__(self, salt='SlTeRlOHpygTYkP3'):
        """Constructor for crypt
        Crypt created with salt"""
        self.salt = salt.encode('utf8')
        self.enc_dec_method = 'utf-8'

    def encrypt(self, str_to_enc, str_key):
        """Performs AES using public key of a user and encrypts the string.
        :param str_to_enc: String to be encrypted
        :param str_key: Key to be used for encryption

        :return: The encrypted string.  
        """
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
        """
        Derypts the string using AES by providing the private key. 
        
        :param enc_str: string to be decrypted.
        :param str_key: private key for decryption.
        :return: The decrypted string.
        :rtype: str
        """
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

def sendmessage(socket1, strn):
    """A function to send a message to the desired socket.

    :param socket1: socket to which the message must be sent.
    :param strn: the message to be sent.


    """
    strn = strn.encode('utf-8')
    strn_header = f"{len(strn):<{HEADER_LENGTH}}".encode('utf-8')
    socket1.send(strn_header + strn)

def new_socket(IP, PORT):
    """Creates new socket at given PORT of IP
    :param IP: IP of the new socket.
    :param PORT: Port of the new socket.
    :return: A new socket."""
    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to a given ip and port
    client_socket.connect((IP, PORT))

    # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
    client_socket.setblocking(False)

    return client_socket

def credential_login(socket1, my_username, my_password, ClientKey, uport):
    """Function to verify if the user has logged in.
    :param socket1: Socket of the server.
    :param my_username: username for logging in.
    :param my_password: Password for logging in.
    :param ClientKey: key to hash the password.

    :return: None
    """
    crpt = Crypt()
    sendmessage(socket1, "HELLOFROMCLIENT")

    # Prepare username and header and send them
    # We need to encode username to bytes, then count number of bytes and prepare 
    # header of fixed size, that we encode to bytes as well
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    socket1.send(username_header + username)

    pwd = crpt.encrypt(my_password, ClientKey).encode('utf-8')
    pwd_header = f"{len(pwd):<{HEADER_LENGTH}}".encode('utf-8')
    socket1.send(pwd_header + pwd) 

    sendmessage(socket1, str(uport))

def receive_message(client_socket):
    """Recieves and parses a message which comes from a client/server
    :param client_socket: socket on which the message would be recieved.
    :return: A parsed object consisting of header and the intended message.
    """
    try:
        client_socket.setblocking(1)
        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            print("u")
            return False
        client_socket.setblocking(0)
        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False


def sign_up(socket1, my_username, my_password, uport):
    """Function to register the user on the database.
    :param socket1: Socket of the connected server.
    :param my_username: Username of the new user.
    :param my_password: Password of the new user.

    :return: The private key of the client.
    """
    cmd = "SIGNUP".encode('utf-8')
    cmd_header = f"{len(cmd):<{HEADER_LENGTH}}".encode('utf-8')
    socket1.send(cmd_header + cmd)
    print("sent cmd")
    
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    socket1.send(username_header + username)
    print("sent username")



    # using random.choices()
    # generating random strings
    ClientKey = str(''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=16)))

    crpt = Crypt()
    pwd = crpt.encrypt(my_password, ClientKey).encode('utf-8')
    pwd_header = f"{len(pwd):<{HEADER_LENGTH}}".encode('utf-8')
    socket1.send(pwd_header + pwd) 

    sendmessage(socket1, str(uport))

    return ClientKey

if __name__ == "__main__":
    print("Hello World")
    test_crpt = Crypt()
    test_text = """Lorem ipsum dolor sit amet"""


    test_key = 'MyKey4TestingYnP'
    test_enc_text = test_crpt.encrypt(test_text, test_key)
    test_dec_text = test_crpt.decrypt(test_enc_text, test_key)
    print(f'Encrypted:{test_enc_text}  Decrypted:{test_dec_text}')
    print(type(test_enc_text))

