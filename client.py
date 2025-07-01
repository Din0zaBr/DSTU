import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
from os import urandom
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 5555
KEY = b'1234567890abcdef'
backend = default_backend()


class VPNClientGUI:
    def __init__(self, master):
        self.master = master
        master.title('VPN Client')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror('Ошибка подключения', str(e))
            master.destroy()
            return
        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=50, height=15)
        self.text_area.pack(padx=10, pady=10)
        self.entry = tk.Entry(master, width=40)
        self.entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.send_button = tk.Button(master, text='Отправить', command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)
        self.entry.bind('<Return>', lambda event: self.send_message())
        master.protocol('WM_DELETE_WINDOW', self.on_close)

    def send_message(self):
        msg = self.entry.get()
        if not msg:
            return
        if msg == 'leave':
            self.sock.close()
            self.master.destroy()
            return
        iv = urandom(16)
        padder = PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(msg.encode('utf-8')) + padder.finalize()
        cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        try:
            self.sock.sendall(iv + ciphertext)
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f'Вы: {msg}\n')
            self.text_area.config(state='disabled')
            self.entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror('Ошибка отправки', str(e))
            self.sock.close()
            self.master.destroy()

    def on_close(self):
        try:
            self.sock.close()
        except:
            pass
        self.master.destroy()


def main():
    root = tk.Tk()
    app = VPNClientGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
