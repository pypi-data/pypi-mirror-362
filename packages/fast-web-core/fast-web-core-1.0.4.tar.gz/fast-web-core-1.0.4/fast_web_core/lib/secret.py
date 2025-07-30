import base64
import hashlib
from typing import Callable
from uuid import uuid4

uuidChars = ("a", "b", "c", "d", "e", "f",
             "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
             "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
             "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
             "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
             "W", "X", "Y", "Z")


def short_uuid():
    uuid = str(uuid4()).replace('-', '')
    result = ''
    for i in range(0, 8):
        sub = uuid[i * 4: i * 4 + 4]
        x = int(sub, 16)
        result += uuidChars[x % 0x3E]
    return result


def base64_decode(base64_message: str) -> str:
    """
    base64 decode
    :param base64_message: base64 message to be decoded
    :return: decoded string
    """
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('ascii')


def base64_encode(message: str) -> str:
    """
    base64 encode
    :param message: message to be encoded
    :return: encoded base64 string
    """
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')


def hs(s: str, length: int = 16, hasher: Callable = hashlib.md5) -> str:
    """
    hash a string
    :param s: string
    :param length: length (default is 16)
    :param hasher: hash function, refer hashlib for details
    :return: hashed string
    """
    if length <= 0:
        length = 16
    ret = hasher(s.encode()).hexdigest()
    if len(ret) > length:
        ret = ret[:length]
    return ret
