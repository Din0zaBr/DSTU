"""
СИСТЕМА ВИЖИНЕРА

Модуль для шифрования и расшифрования текста с использованием системы Вижинера.
Система Вижинера - это полиалфавитный шифр подстановки, использующий ключ для циклического сдвига алфавита.
"""

import re

ALP = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'  # Алфавит для системы Вижинера (33 буквы русского алфавита)
ALP_DICT = {letter: idx for idx, letter in enumerate(ALP)}


def _prepare_key(key: str, text_length: int) -> str:
    """
    Расширяет ключ до длины текста путем циклического повторения.
    
    Args:
        key: Исходный ключ (str)
        text_length: Длина текста, до которой нужно расширить ключ (int)
    
    Returns:
        Расширенный ключ (str)
    """
    return (key * ((text_length // len(key)) + 1))[:text_length]


def _validate_and_clean_text(text: str, field_name: str = "текст") -> str:
    """
    Валидирует и очищает текст от всех символов, кроме русских букв, Ё -> Е
    
    Args:
        text: Исходный текст (str)
        field_name: Название поля для сообщения об ошибке (str)
    
    Returns:
        Очищенный текст в верхнем регистре (str)
    
    Raises:
        ValueError: Если текст пустой после очистки
    """
    cleaned = re.sub(r'[^А-ЯЁ]', '', text.upper()).replace('Ё', 'Е')
    if not cleaned:
        raise ValueError(f"Ошибка: {field_name} не может быть пустым!")
    return cleaned


def encrypt_vigenere():
    """
    Независимая функция шифрования системы Вижинера.
    
    Запрашивает у пользователя текст и ключ, затем шифрует текст
    методом Вижинера (сложение индексов букв текста и ключа по модулю длины алфавита).
    Функция полностью независима от decrypt_vigenere().
    """
    try:
        text = _validate_and_clean_text(input("\nВведите текст для шифрования: "), "текст")
        key = _validate_and_clean_text(input("Введите ключ: "), "ключ")
    except ValueError as e:
        print(e)
        return

    # Расширяем ключ до длины текста
    extended_key = _prepare_key(key, len(text))

    # Шифрование: для каждой буквы текста складываем её индекс с индексом соответствующей буквы ключа
    encrypted = ''.join(ALP[(ALP_DICT[text[i]] + ALP_DICT[extended_key[i]]) % len(ALP)]
                        for i in range(len(text)))

    print(f"\nРЕЗУЛЬТАТ ШИФРОВАНИЯ")
    print(f"Исходный текст: {text}")
    print(f"Ключ: {key}")
    print(f"Зашифрованный текст: {encrypted}")


def decrypt_vigenere():
    """
    Независимая функция расшифрования системы Вижинера.
    
    Запрашивает у пользователя шифртекст и ключ, затем расшифровывает текст
    методом Вижинера (вычитание индексов ключа из индексов шифртекста по модулю длины алфавита).
    Функция полностью независима от encrypt_vigenere().
    """
    try:
        encrypted_text = _validate_and_clean_text(input("\nВведите шифртекст для расшифрования: "), "шифртекст")
        key = _validate_and_clean_text(input("Введите ключ: "), "ключ")
    except ValueError as e:
        print(e)
        return

    # Расширяем ключ до длины зашифрованного текста
    extended_key = _prepare_key(key, len(encrypted_text))

    # Расшифровка: для каждой буквы шифртекста вычитаем индекс соответствующей буквы ключа
    decrypted = ''.join(ALP[(ALP_DICT[encrypted_text[i]] - ALP_DICT[extended_key[i]]) % len(ALP)]
                        for i in range(len(encrypted_text)))

    print(f"\nРЕЗУЛЬТАТ РАСШИФРОВАНИЯ")
    print(f"Шифртекст: {encrypted_text}")
    print(f"Ключ: {key}")
    print(f"Расшифрованный текст: {decrypted}")


def vigenere_menu():
    """
    Меню для системы Вижинера
    
    Предоставляет пользователю выбор между шифрованием и расшифрованием.
    """
    print("\n=== СИСТЕМА ВИЖИНЕРА ===")
    print("1. Зашифровать")
    print("2. Расшифровать")
    print("0. Назад")
    choice = input("Выбор: ").strip()

    if choice == "1":
        encrypt_vigenere()
    elif choice == "2":
        decrypt_vigenere()
    elif choice == "0":
        return
    else:
        print("Неверный выбор!")
