"""
Реализация ГОСТ 28147-89 (Магма)

ГОСТ 28147-89 - российский стандарт шифрования, утвержден в 1989 году.
Полная реализация алгоритма с нуля.
"""

import os
from typing import Tuple, Final

from .base_encryption import BaseBlockCipher


class GOST28147(BaseBlockCipher):
    """
    Класс для шифрования ГОСТ 28147-89 (Магма)
    
    Российский стандарт шифрования, утвержден в 1989 году.
    Полная реализация алгоритма с использованием сети Фейстеля.
    """
    
    # S-блоки для замены (стандартная таблица замен из RFC 4357)
    S_BOX: Final[list[list[int]]] = [
        [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
        [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
        [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
        [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
        [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
        [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
        [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
        [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]
    ]
    
    BLOCK_SIZE: Final[int] = 64  # 64 бита = 8 байт
    KEY_SIZE: Final[int] = 256  # 256 бит = 32 байта
    ROUNDS: Final[int] = 32  # Количество раундов
    KEY_PARTS: Final[int] = 8  # Количество частей ключа
    ROTATION_BITS: Final[int] = 11  # Количество бит для циклического сдвига
    
    def __init__(self) -> None:
        """Инициализация ГОСТ 28147-89"""
        pass  # Все параметры фиксированы
    
    @property
    def block_size(self) -> int:
        """Размер блока в битах"""
        return self.BLOCK_SIZE
    
    @property
    def key_size(self) -> int:
        """Размер ключа в битах"""
        return self.KEY_SIZE
    
    def generate_key(self) -> bytes:
        """
        Генерация случайного ключа
        
        Returns:
            Случайно сгенерированный ключ (32 байта)
        """
        return os.urandom(self.KEY_SIZE // 8)
    
    @staticmethod
    def _split_64bit(value: int) -> Tuple[int, int]:
        """
        Разделение 64-битного значения на два 32-битных
        
        Args:
            value: 64-битное значение
        
        Returns:
            Кортеж из двух 32-битных значений (left, right)
        """
        return (value >> 32) & 0xFFFFFFFF, value & 0xFFFFFFFF
    
    @staticmethod
    def _join_32bit(left: int, right: int) -> int:
        """
        Объединение двух 32-битных значений в одно 64-битное
        
        Args:
            left: Левая 32-битная часть
            right: Правая 32-битная часть
        
        Returns:
            64-битное значение
        """
        return ((left & 0xFFFFFFFF) << 32) | (right & 0xFFFFFFFF)
    
    def _s_box_substitution(self, value: int) -> int:
        """
        Замена по S-блокам (таблицам замен)
        
        Args:
            value: 32-битное значение для замены
        
        Returns:
            Преобразованное 32-битное значение
        """
        result = 0
        for i in range(8):
            nibble = (value >> (i * 4)) & 0xF
            result |= (self.S_BOX[7 - i][nibble] << (i * 4))
        return result
    
    @staticmethod
    def _rotate_left_11(value: int) -> int:
        """
        Циклический сдвиг влево на 11 бит
        
        Args:
            value: 32-битное значение для сдвига
        
        Returns:
            Преобразованное 32-битное значение
        """
        return ((value << 11) | (value >> 21)) & 0xFFFFFFFF
    
    def _generate_round_keys(self, key: bytes) -> list[int]:
        """
        Генерация ключей для 32 раундов
        
        Args:
            key: Ключ шифрования (32 байта)
        
        Returns:
            Список из 32 ключей для раундов
        
        Raises:
            ValueError: Если размер ключа неверный
        """
        if len(key) != self.KEY_SIZE // 8:
            raise ValueError(
                f"Ключ должен быть {self.KEY_SIZE // 8} байт (256 бит), "
                f"получено {len(key)} байт"
            )
        
        # Разделение ключа на 8 частей по 32 бита
        keys: list[int] = []
        for i in range(self.KEY_PARTS):
            key_part = int.from_bytes(key[i*4:(i+1)*4], 'little')
            keys.append(key_part)
        
        # Генерация ключей для раундов (32 раунда, ключи повторяются)
        round_keys: list[int] = []
        for i in range(self.ROUNDS):
            if i < 24:
                round_keys.append(keys[i % self.KEY_PARTS])
            else:
                round_keys.append(keys[7 - (i % self.KEY_PARTS)])
        
        return round_keys
    
    def _f_function(self, data: int, key: int) -> int:
        """
        Функция F (основная функция преобразования)
        
        Args:
            data: 32-битное входное значение
            key: 32-битный ключ раунда
        
        Returns:
            32-битное преобразованное значение
        """
        # Сложение с ключом по модулю 2^32
        temp = (data + key) & 0xFFFFFFFF
        
        # Замена по S-блокам
        temp = self._s_box_substitution(temp)
        
        # Циклический сдвиг влево на 11 бит
        temp = self._rotate_left_11(temp)
        
        return temp
    
    def encrypt_block(self, block: bytes, key: bytes) -> bytes:
        """
        Шифрование одного блока (64 бита)
        
        Args:
            block: Блок данных (8 байт)
            key: Ключ шифрования (32 байта)
        
        Returns:
            Зашифрованный блок (8 байт)
        
        Raises:
            ValueError: Если размер блока или ключа неверный
        """
        if len(block) != self.BLOCK_SIZE // 8:
            raise ValueError(
                f"Размер блока должен быть {self.BLOCK_SIZE // 8} байт (64 бита), "
                f"получено {len(block)} байт"
            )
        
        self.validate_key(key)
        
        # Генерация ключей раундов
        round_keys = self._generate_round_keys(key)
        
        # Преобразование блока в 64-битное число
        data = int.from_bytes(block, 'little')
        left, right = self._split_64bit(data)
        
        # 32 раунда шифрования (сеть Фейстеля)
        for i in range(self.ROUNDS):
            new_right = left ^ self._f_function(right, round_keys[i])
            left = right
            right = new_right
        
        # Финальная перестановка (меняем местами left и right)
        result = self._join_32bit(right, left)
        
        # Преобразование обратно в байты
        return result.to_bytes(self.BLOCK_SIZE // 8, 'little')
    
    def decrypt_block(self, block: bytes, key: bytes) -> bytes:
        """
        Расшифрование одного блока (64 бита)
        
        Args:
            block: Зашифрованный блок (8 байт)
            key: Ключ шифрования (32 байта)
        
        Returns:
            Расшифрованный блок (8 байт)
        
        Raises:
            ValueError: Если размер блока или ключа неверный
        """
        if len(block) != self.BLOCK_SIZE // 8:
            raise ValueError(
                f"Размер блока должен быть {self.BLOCK_SIZE // 8} байт (64 бита), "
                f"получено {len(block)} байт"
            )
        
        self.validate_key(key)
        
        # Генерация ключей раундов
        round_keys = self._generate_round_keys(key)
        
        # Преобразование блока в 64-битное число
        data = int.from_bytes(block, 'little')
        left, right = self._split_64bit(data)
        
        # 32 раунда расшифрования (ключи в обратном порядке)
        for i in range(self.ROUNDS - 1, -1, -1):
            new_right = left ^ self._f_function(right, round_keys[i])
            left = right
            right = new_right
        
        # Финальная перестановка
        result = self._join_32bit(right, left)
        
        # Преобразование обратно в байты
        return result.to_bytes(self.BLOCK_SIZE // 8, 'little')
    
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """
        Шифрование данных произвольного размера (режим простой замены)
        
        Args:
            plaintext: Открытый текст (байты)
            key: Ключ шифрования (32 байта)
        
        Returns:
            Зашифрованные данные (байты)
        
        Raises:
            ValueError: Если размер ключа неверный
        """
        self.validate_key(key)
        
        block_size_bytes = self.BLOCK_SIZE // 8
        
        # Дополнение данных до размера, кратного 8 байтам
        padding_len = block_size_bytes - (len(plaintext) % block_size_bytes)
        if padding_len == block_size_bytes:
            padding_len = 0
        
        padded_text = plaintext + bytes([padding_len] * padding_len)
        
        # Шифрование каждого блока
        ciphertext = b''
        for i in range(0, len(padded_text), block_size_bytes):
            block = padded_text[i:i+block_size_bytes]
            encrypted_block = self.encrypt_block(block, key)
            ciphertext += encrypted_block
        
        return ciphertext
    
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """
        Расшифрование данных
        
        Args:
            ciphertext: Зашифрованные данные (байты)
            key: Ключ шифрования (32 байта)
        
        Returns:
            Расшифрованные данные (байты)
        
        Raises:
            ValueError: Если размер ключа неверный или данные некорректны
        """
        self.validate_key(key)
        
        block_size_bytes = self.BLOCK_SIZE // 8
        
        if len(ciphertext) % block_size_bytes != 0:
            raise ValueError(
                f"Размер зашифрованных данных должен быть кратен {block_size_bytes} байтам, "
                f"получено {len(ciphertext)} байт"
            )
        
        # Расшифрование каждого блока
        plaintext = b''
        for i in range(0, len(ciphertext), block_size_bytes):
            block = ciphertext[i:i+block_size_bytes]
            decrypted_block = self.decrypt_block(block, key)
            plaintext += decrypted_block
        
        # Удаление padding
        if len(plaintext) > 0:
            padding_len = plaintext[-1]
            if 0 < padding_len <= block_size_bytes:
                plaintext = plaintext[:-padding_len]
        
        return plaintext

