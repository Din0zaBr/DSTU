"""
Модуль для шифрования и расшифрования текста с использованием шифра Гронсфельда.

Шифр Гронсфельда является многоалфавитной модификацией шифра Цезаря.
Если в шифре Цезаря величина сдвига фиксирована,
то в шифре Гросфельда она меняется в процессе шифрования.
Для этого используется числовой ключ, который циклически записывается под сообщением.
В процессе шифрования сдвиг происходит на цифру, указанную под шифруемой буквой.
"""

from typing import Dict

# Константы алфавита: русские буквы + пробел + знаки препинания
ALP: str = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ .,!?;:-()"'
ALP_DICT: Dict[str, int] = {letter: idx for idx, letter in enumerate(ALP)}


def _prepare_key(key: str, text_length: int) -> str:
    """
    Расширяет ключ до длины текста путем циклического повторения.

    Args:
        key: Исходный ключ (str)
        text_length: Длина текста, до которой нужно расширить ключ (int)

    Returns:
        Расширенный ключ (str)
    """
    if not key:
        raise ValueError("Ключ не может быть пустым!")
    
    return (key * ((text_length // len(key)) + 1))[:text_length]


def _validate_and_clean_text(text: str, field_name: str = "текст") -> str:
    """
    Валидирует и очищает текст, оставляя только символы из алфавита.

    Args:
        text: Исходный текст (str)
        field_name: Название поля для сообщения об ошибке (str)

    Returns:
        Очищенный текст (str)

    Raises:
        ValueError: Если текст пустой после очистки
    """
    cleaned: str = ''
    for char in text:
        char_upper = char.upper()
        if char in ALP_DICT:
            cleaned += char
        elif char_upper in ALP_DICT and ('А' <= char_upper <= 'Я' or char_upper == 'Ё'):
            cleaned += char_upper
    
    if not cleaned:
        raise ValueError(f"Ошибка: {field_name} не может быть пустым!")
    return cleaned


def encrypt_text(text: str, key: str) -> str:
    """
    Шифрует текст с использованием шифра Гронсфельда.
    
    Args:
        text: Текст для шифрования (str)
        key: Числовой ключ (str)
    
    Returns:
        Зашифрованный текст (str)
    
    Raises:
        ValueError: Если текст или ключ некорректны
    """
    cleaned_text: str = _validate_and_clean_text(text, "текст")
    
    if not key or not key.strip():
        raise ValueError("Ключ должен содержать только цифры!")
    
    if not key.isdigit():
        raise ValueError("Ключ должен содержать только цифры!")
    
    extended_key: str = _prepare_key(key, len(cleaned_text))
    
    encrypted: str = ''.join(
        ALP[(ALP_DICT[cleaned_text[i]] - int(extended_key[i])) % len(ALP)]
        for i in range(len(cleaned_text))
    )
    
    return encrypted


def decrypt_text(encrypted_text: str, key: str) -> str:
    """
    Расшифровывает текст с использованием шифра Гронсфельда.
    
    Args:
        encrypted_text: Зашифрованный текст (str)
        key: Числовой ключ (str)
    
    Returns:
        Расшифрованный текст (str)
    
    Raises:
        ValueError: Если текст или ключ некорректны
    """
    cleaned_text: str = _validate_and_clean_text(encrypted_text, "шифртекст")
    
    if not key or not key.strip():
        raise ValueError("Ключ должен содержать только цифры!")
    
    if not key.isdigit():
        raise ValueError("Ключ должен содержать только цифры!")
    
    extended_key: str = _prepare_key(key, len(cleaned_text))
    
    decrypted: str = ''.join(
        ALP[(ALP_DICT[cleaned_text[i]] + int(extended_key[i])) % len(ALP)]
        for i in range(len(cleaned_text))
    )
    
    return decrypted

