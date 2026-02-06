"""
Реализация AES (Advanced Encryption Standard)

AES - американский стандарт шифрования (FIPS 197), утвержден в 2001 году.
"""

import os
from typing import Literal

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .base_encryption import BaseBlockCipher


class AESEncryption(BaseBlockCipher):
    """
    Класс для шифрования AES (Advanced Encryption Standard)
    
    Стандарт США (FIPS 197), утвержден в 2001 году.
    Использует библиотеку cryptography для реализации.
    """
    
    # Поддерживаемые размеры ключей
    SUPPORTED_KEY_SIZES: tuple[int, ...] = (128, 192, 256)
    BLOCK_SIZE: int = 128  # AES всегда использует блоки 128 бит
    IV_SIZE: int = 16  # Размер вектора инициализации в байтах
    
    def __init__(self, key_size: Literal[128, 192, 256] = 256) -> None:
        """
        Инициализация AES шифрования
        
        Args:
            key_size: Размер ключа в битах (128, 192, или 256)
        
        Raises:
            ValueError: Если размер ключа не поддерживается
        """
        if key_size not in self.SUPPORTED_KEY_SIZES:
            raise ValueError(
                f"Размер ключа должен быть один из {self.SUPPORTED_KEY_SIZES} бит, "
                f"получено {key_size} бит"
            )
        
        self._key_size = key_size
    
    @property
    def block_size(self) -> int:
        """Размер блока в битах"""
        return self.BLOCK_SIZE
    
    @property
    def key_size(self) -> int:
        """Размер ключа в битах"""
        return self._key_size
    
    def generate_key(self) -> bytes:
        """
        Генерация случайного ключа
        
        Returns:
            Случайно сгенерированный ключ нужного размера
        """
        return os.urandom(self._key_size // 8)
    
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """
        Шифрование данных
        
        Args:
            plaintext: Открытый текст (байты)
            key: Ключ шифрования
        
        Returns:
            Зашифрованные данные (IV + ciphertext в байтах)
        
        Raises:
            ValueError: Если размер ключа неверный
        """
        self.validate_key(key)
        
        # Генерация случайного IV
        iv = os.urandom(self.IV_SIZE)
        
        # Добавление padding для выравнивания размера блока
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        
        # Шифрование
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Возвращаем IV + зашифрованные данные
        return iv + ciphertext
    
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """
        Расшифрование данных
        
        Args:
            ciphertext: Зашифрованные данные (IV + ciphertext в байтах)
            key: Ключ шифрования
        
        Returns:
            Расшифрованные данные (байты)
        
        Raises:
            ValueError: Если размер ключа неверный или данных недостаточно для IV
        """
        self.validate_key(key)
        
        if len(ciphertext) < self.IV_SIZE:
            raise ValueError(
                f"Размер зашифрованных данных слишком мал. "
                f"Ожидается минимум {self.IV_SIZE} байт для IV"
            )
        
        # Извлечение IV
        iv = ciphertext[:self.IV_SIZE]
        encrypted_data = ciphertext[self.IV_SIZE:]
        
        # Расшифрование
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Удаление padding
        unpadder = padding.PKCS7(self.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext

