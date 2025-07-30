# -*- coding: UTF-8 -*-
import json
import uuid
import hashlib
import time

from base64 import b64encode, b64decode

chars = ["a", "b", "c", "d", "e", "f",
         "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
         "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
         "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
         "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
         "W", "X", "Y", "Z"]


def generate_app_id():
    """
    生成APP ID
    """
    short_buffer = []
    uuid_str = str(uuid.uuid4()).replace('-', '')

    for i in range(8):
        substr = uuid_str[i * 4: i * 4 + 4]
        x = int(substr, 16)
        short_buffer.append(chars[x % 0x3E])

    return ''.join(short_buffer)


def generate_access_key(data: dict):
    """
    生成Access Key
    """
    # 将数据转换为 UTF-8 编码的 JSON 字符串
    utf8_string = json.dumps(data).encode('utf-8')

    # 对 UTF-8 编码的 JSON 字符串进行 base64 编码
    encoded_data = b64encode(utf8_string)

    # 将 base64 编码后的数据与 app_id 进行拼接
    combined_data = encoded_data.decode("utf-8")

    # 计算拼接后字符串的 MD5 摘要
    md5_hash = hashlib.md5(combined_data.encode('utf-8')).hexdigest()

    return md5_hash


def generate_secret_key():
    """
    生成 Secret Access Key
    """
    # 生成 Secret Key，这里使用当前时间戳和一些随机性
    secret_key_data = f"{time.time()}:{uuid.uuid4()}"
    secret_key = hashlib.sha256(secret_key_data.encode()).hexdigest()

    return secret_key


# 加密
def encrypt_aes(data, key: str, iv: str):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    # 使用 AES 算法，CBC 模式进行加密
    cipher = Cipher(algorithms.AES(key.encode('utf-8')), modes.CFB(iv.encode('utf-8')), backend=default_backend())
    encryptor = cipher.encryptor()
    utf8_string = json.dumps(data).encode('utf-8').decode('utf-8')
    # 加密数据
    encrypted_data = encryptor.update(utf8_string.encode('utf-8')) + encryptor.finalize()

    # 将加密后的数据进行 Base64 编码
    return b64encode(encrypted_data).decode('utf-8')


# 解密
def decrypt_aes(encrypted_data, key: str, iv: str):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    # 使用 AES 算法，CBC 模式进行解密
    cipher = Cipher(algorithms.AES(key.encode('utf-8')), modes.CFB(iv.encode('utf-8')), backend=default_backend())
    decryptor = cipher.decryptor()
    # Base64 解码
    encrypted_data_bytes = b64decode(encrypted_data)
    # 解密数据
    decrypted_data = decryptor.update(encrypted_data_bytes) + decryptor.finalize()

    return decrypted_data.decode('utf-8')

# if __name__ == '__main__':
#     data_to_encrypt = {
#         "id": 1,
#         'userId': '1067246875800000001',
#         'username': 'admin',
#         'realName': '超级管理员',
#         'tenantCode': 'system'
#     }
#     print(generate_app_id())
#     encrypted_data = encrypt_aes(data_to_encrypt, key, iv)
#     print(f'Encrypted: {encrypted_data}')
#     #
#     decrypted_data = decrypt_aes(encrypted_data, key, iv)
#     print(f'Decrypted: {decrypted_data}')
