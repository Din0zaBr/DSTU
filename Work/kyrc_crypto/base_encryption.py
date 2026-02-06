"""
Базовый класс для алгоритмов блочного шифрования

Определяет интерфейс, который должны реализовывать все алгоритмы шифрования.
"""

from abc import ABC, abstractmethod
from typing import Protocol


class BlockCipher(Protocol):
    """
    Протокол (интерфейс) для алгоритмов блочного шифрования
    
    Используется для типизации и проверки соответствия интерфейсу
    """
    
    @property
    def block_size(self) -> int:
        """Размер блока в битах"""
        ...
    
    @property
    def key_size(self) -> int:
        """Размер ключа в битах"""
        ...
    
    def generate_key(self) -> bytes:
        """Генерация случайного ключа"""
        ...
    
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """Шифрование данных"""
        ...
    
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """Расшифрование данных"""
        ...


class BaseBlockCipher(ABC):
    """
    Абстрактный базовый класс для алгоритмов блочного шифрования
    
    Предоставляет общие методы и определяет обязательный интерфейс
    """
    
    @property
    @abstractmethod
    def block_size(self) -> int:
        """
        Размер блока в битах
        
        Returns:
            Размер блока в битах
        """
        pass
    
    @property
    @abstractmethod
    def key_size(self) -> int:
        """
        Размер ключа в битах
        
        Returns:
            Размер ключа в битах
        """
        pass
    
    @abstractmethod
    def generate_key(self) -> bytes:
        """
        Генерация случайного ключа
        
        Returns:
            Случайно сгенерированный ключ
        """
        pass
    
    @abstractmethod
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """
        Шифрование данных
        
        Args:
            plaintext: Открытый текст для шифрования
            key: Ключ шифрования
        
        Returns:
            Зашифрованные данные
        
        Raises:
            ValueError: Если размер ключа неверный
        """
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """
        Расшифрование данных
        
        Args:
            ciphertext: Зашифрованные данные
            key: Ключ шифрования
        
        Returns:
            Расшифрованные данные
        
        Raises:
            ValueError: Если размер ключа неверный или данные некорректны
        """
        pass
    
    def validate_key(self, key: bytes) -> None:
        """
        Валидация размера ключа
        
        Args:
            key: Ключ для проверки
        
        Raises:
            ValueError: Если размер ключа неверный
        """
        expected_size = self.key_size // 8
        if len(key) != expected_size:
            raise ValueError(
                f"Неверный размер ключа. Ожидается {expected_size} байт, "
                f"получено {len(key)} байт"
            )

