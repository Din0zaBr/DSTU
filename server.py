import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend

HOST = '0.0.0.0'
PORT = 5555
KEY = b'1234567890abcdef'  # 16 байт для AES-128

backend = default_backend()

# Создание TCP-сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f'Сервер запущен на {HOST}:{PORT}')

conn, addr = server_socket.accept()
print(f'Подключение от {addr}')

while True:
    data = conn.recv(1024)
    if not data:
        break

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    try:
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        print('Получено сообщение:', plaintext.decode('utf-8'))
    except Exception as e:
        print('Ошибка расшифровки:', e)

conn.close()
server_socket.close()