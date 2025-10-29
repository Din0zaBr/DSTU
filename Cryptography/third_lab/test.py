from Cryptography.second_lab.sixth import create_trisemus_table

import re
# В симметричной криптосистеме секретный ключ передается по защищенному каналу
# СПРАВОЧНИК

def unique_ordered(lst):
    return list(dict.fromkeys(lst))


def create_playfair_table(keyword, alp='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', rows=4, cols=8):
    """Создание таблицы Плейфейра через таблицу Трисемуса"""
    return create_trisemus_table(keyword, alp, rows, cols)


def find_position(table, char):
    """Нахождение позиции символа в таблице"""
    for i, row in enumerate(table):
        for j, cell in enumerate(row):
            if cell == char:
                return i, j
    return None


def prepare_text(text):
    """Подготовка текста: удаление пробелов, приведение к верхнему регистру"""
    text = text.upper()
    text = re.sub(r'[^А-ЯЁ]', '', text)  # Удаляем все не-буквы
    return text


def split_into_bigrams(text):
    """Разбиение текста на биграммы с обработкой повторяющихся букв"""
    bigrams = []
    i = 0

    while i < len(text):
        if i + 1 < len(text):
            char1, char2 = text[i], text[i + 1]

            # Если две одинаковые буквы подряд, вставляем Ъ между ними
            if char1 == char2:
                bigrams.append((char1, 'Ъ'))
                i += 1
            else:
                bigrams.append((char1, char2))
                i += 2
        else:
            # Если нечетное количество букв, добавляем Ъ в конец
            bigrams.append((text[i], 'Ъ'))
            i += 1

    return bigrams


def encrypt_bigram(table, bigram):
    """Шифрование одной биграммы"""
    row1, col1 = find_position(table, bigram[0])
    row2, col2 = find_position(table, bigram[1])

    # Случай 1: буквы в одной строке
    if row1 == row2:
        encrypted1 = table[row1][(col1 + 1) % len(table[0])]
        encrypted2 = table[row2][(col2 + 1) % len(table[0])]

    # Случай 2: буквы в одном столбце
    elif col1 == col2:
        encrypted1 = table[(row1 + 1) % len(table)][col1]
        encrypted2 = table[(row2 + 1) % len(table)][col2]

    # Случай 3: буквы образуют прямоугольник
    else:
        encrypted1 = table[row1][col2]
        encrypted2 = table[row2][col1]

    return encrypted1 + encrypted2


def decrypt_bigram(table, bigram):
    """Дешифрование одной биграммы"""
    row1, col1 = find_position(table, bigram[0])
    row2, col2 = find_position(table, bigram[1])

    # Случай 1: буквы в одной строке
    if row1 == row2:
        decrypted1 = table[row1][(col1 - 1) % len(table[0])]
        decrypted2 = table[row2][(col2 - 1) % len(table[0])]

    # Случай 2: буквы в одном столбце
    elif col1 == col2:
        decrypted1 = table[(row1 - 1) % len(table)][col1]
        decrypted2 = table[(row2 - 1) % len(table)][col2]

    # Случай 3: буквы образуют прямоугольник
    else:
        decrypted1 = table[row1][col2]
        decrypted2 = table[row2][col1]

    return decrypted1 + decrypted2


def playfair_encrypt(plaintext, keyword, alp='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', rows=4, cols=8):
    """Шифрование текста методом Плейфейра"""
    table = create_playfair_table(keyword, alp, rows, cols)
    prepared_text = prepare_text(plaintext)
    bigrams = split_into_bigrams(prepared_text)
    encrypted_bigrams = [encrypt_bigram(table, bigram) for bigram in bigrams]
    ciphertext = ''.join(encrypted_bigrams)

    return ciphertext


def playfair_decrypt(ciphertext, keyword, alp='АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', rows=4, cols=8):
    """Дешифрование текста методом Плейфейра"""
    table = create_playfair_table(keyword, alp, rows, cols)
    prepared_text = prepare_text(ciphertext)
    bigrams = [(prepared_text[i], prepared_text[i + 1]) for i in range(0, len(prepared_text), 2)]
    decrypted_bigrams = [decrypt_bigram(table, bigram) for bigram in bigrams]
    plaintext = ''.join(decrypted_bigrams)

    return plaintext


def print_table(table):
    """Печать таблицы в читаемом формате"""
    print("Таблица Плейфейра:")
    for i, row in enumerate(table):
        print(f"{i + 1}: | {' | '.join(row)} |")
    print()


def encrypt_mode():
    """Режим шифрования"""
    print("\n" + "=" * 60)
    print("РЕЖИМ ШИФРОВАНИЯ")
    print("=" * 60)
    
    keyword = input("Введите ключ (слово): ").upper()
    plaintext = input("Введите текст для шифрования: ")
    rows = int(input("Введите количество строк таблицы: "))
    cols = int(input("Введите количество столбцов таблицы: "))
    
    print("\nСоздание таблицы Плейфейра...")
    table = create_playfair_table(keyword, rows=rows, cols=cols)
    print_table(table)
    
    print("Шифрование...")
    ciphertext = playfair_encrypt(plaintext, keyword, rows=rows, cols=cols)
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТ ШИФРОВАНИЯ:")
    print("=" * 60)
    print(f"Исходный текст: {plaintext}")
    print(f"Зашифрованный текст: {ciphertext}")
    print("=" * 60)


def decrypt_mode():
    """Режим дешифрования"""
    print("\n" + "=" * 60)
    print("РЕЖИМ ДЕШИФРОВАНИЯ")
    print("=" * 60)
    
    keyword = input("Введите ключ (слово): ").upper()
    ciphertext = input("Введите текст для дешифрования: ")
    rows = int(input("Введите количество строк таблицы: "))
    cols = int(input("Введите количество столбцов таблицы: "))
    
    print("\nСоздание таблицы Плейфейра...")
    table = create_playfair_table(keyword, rows=rows, cols=cols)
    print_table(table)
    
    print("Дешифрование...")
    decrypted_text = playfair_decrypt(ciphertext, keyword, rows=rows, cols=cols)
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТ ДЕШИФРОВАНИЯ:")
    print("=" * 60)
    print(f"Зашифрованный текст: {ciphertext}")
    print(f"Расшифрованный текст: {decrypted_text}")
    print("=" * 60)


# Главная программа
if __name__ == "__main__":
    print("=" * 60)
    print("ШИФР ПЛЕЙФЕЙРА")
    print("=" * 60)
    print("Выберите режим работы:")
    print("1. Зашифровать текст")
    print("2. Расшифровать текст")
    print("0. Выход")
    print("=" * 60)
    
    choice = input("Ваш выбор: ").strip()
    
    if choice == "1":
        encrypt_mode()
    elif choice == "2":
        decrypt_mode()
    elif choice == "0":
        print("Выход из программы.")
    else:
        print("Неверный выбор! Пожалуйста, выберите 1, 2 или 0.")
