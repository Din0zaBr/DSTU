import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
from os import urandom

HOST = '127.0.0.1'
PORT = 5555
KEY = b'1234567890abcdef'

backend = default_backend()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

try:
    while True:
        msg = input('Введите сообщение (или leave для выхода): ')
        if msg == 'leave':
            break

        iv = urandom(16)
        padder = PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(msg.encode('utf-8')) + padder.finalize()

        cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        client_socket.sendall(iv + ciphertext)
finally:
    client_socket.close()