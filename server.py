import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = '0.0.0.0'
PORT = 5555
KEY = b'1234567890abcdef'  # 16 байт для AES-128
backend = default_backend()


class VPNServerGUI:
    def __init__(self, master):
        self.master = master
        master.title('VPN Server')
        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=60, height=20)
        self.text_area.pack(padx=10, pady=10)
        self.server_thread = threading.Thread(target=self.run_server, daemon=True)
        self.server_thread.start()
        master.protocol('WM_DELETE_WINDOW', self.on_close)
        self.server_socket = None
        self.conn = None

    def run_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)
        self.append_text(f'Сервер запущен на {HOST}:{PORT}\nОжидание подключения...\n')
        self.conn, addr = self.server_socket.accept()
        self.append_text(f'Подключение от {addr}\n')
        while True:
            try:
                data = self.conn.recv(1024)
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
                    self.append_text(f'Клиент: {plaintext.decode("utf-8")}\n')
                except Exception as e:
                    self.append_text(f'Ошибка расшифровки: {e}\n')
            except Exception as e:
                self.append_text(f'Ошибка соединения: {e}\n')
                break
        if self.conn:
            self.conn.close()
        if self.server_socket:
            self.server_socket.close()
        self.append_text('Соединение закрыто.\n')

    def append_text(self, text):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, text)
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)

    def on_close(self):
        try:
            if self.conn:
                self.conn.close()
            if self.server_socket:
                self.server_socket.close()
        except:
            pass
        self.master.destroy()


def main():
    root = tk.Tk()
    app = VPNServerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
