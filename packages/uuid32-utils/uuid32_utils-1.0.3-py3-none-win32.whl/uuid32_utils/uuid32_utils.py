import random
import string
import socket
import hashlib
import time

CHARACTERS_UUID32 = string.digits + string.ascii_lowercase
def get_bytes(str):
    bytes = ''
    for shift in range(0, 128, 8):
        bytes = chr((str.int >> shift) & 0xff) + bytes
    return bytes

def uuid32():
    """
    Generates a random 32-character string using digits (0-9)
    and lowercase English letters (a-z).
    """
    # Generate a random string of 32 characters
    return ''.join(random.choices(CHARACTERS_UUID32, k=32))