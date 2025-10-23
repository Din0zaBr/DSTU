import re


def unique_ordered(lst):
    return list(dict.fromkeys(lst))


def create_trisemus_table(keyword, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', rows=4, cols=8):
    temp_alp = list(unique_ordered(keyword))
    for alp_index in range(len(alp)):
        if alp[alp_index] in temp_alp:
            continue
        else:
            temp_alp += alp[alp_index]

    # Формируем таблицу как список строк
    table = []
    for i in range(rows):
        start_idx = i * cols
        end_idx = start_idx + cols
        table.append(''.join(temp_alp[start_idx:end_idx]))

    return table


def create_playfair_table(keyword, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', rows=4, cols=8):
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
    text = text.upper().replace(' ', '')
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


def playfair_encrypt(plaintext, keyword, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', rows=4, cols=8):
    """Шифрование текста методом Плейфейра"""
    # Создаем таблицу
    table = create_playfair_table(keyword, alp, rows, cols)

    # Подготавливаем текст
    prepared_text = prepare_text(plaintext)

    # Разбиваем на биграммы
    bigrams = split_into_bigrams(prepared_text)

    # Шифруем каждую биграмму
    encrypted_bigrams = [encrypt_bigram(table, bigram) for bigram in bigrams]

    # Объединяем результат
    ciphertext = ''.join(encrypted_bigrams)

    return ciphertext


def playfair_decrypt(ciphertext, keyword, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', rows=4, cols=8):
    """Дешифрование текста методом Плейфейра"""
    # Создаем таблицу
    table = create_playfair_table(keyword, alp, rows, cols)

    # Подготавливаем текст
    prepared_text = prepare_text(ciphertext)

    # Разбиваем на биграммы (по 2 символа)
    bigrams = [(prepared_text[i], prepared_text[i + 1]) for i in range(0, len(prepared_text), 2)]

    # Дешифруем каждую биграмму
    decrypted_bigrams = [decrypt_bigram(table, bigram) for bigram in bigrams]

    # Объединяем результат
    plaintext = ''.join(decrypted_bigrams)

    return plaintext


def print_table(table):
    """Печать таблицы в читаемом формате"""
    print("Таблица Плейфейра:")
    for i, row in enumerate(table):
        print(f"{i + 1}: | {' | '.join(row)} |")
    print()


# Демонстрация работы с примером из задания
if __name__ == "__main__":
    # Параметры из примера
    keyword = "РАБОТА"
    plaintext = "ПРИЛЕТАЮ ЗАВТРА"
    rows, cols = 4, 8

    print("=== Шифр Плейфейра ===")
    print(f"Ключевое слово: {keyword}")
    print(f"Исходный текст: {plaintext}")
    print()

    # Создаем и показываем таблицу
    table = create_playfair_table(keyword, rows=rows, cols=cols)
    print_table(table)

    # Шифруем
    ciphertext = playfair_encrypt(plaintext, keyword, rows=rows, cols=cols)
    print(f"Зашифрованный текст: {ciphertext}")

    # Дешифруем
    decrypted_text = playfair_decrypt(ciphertext, keyword, rows=rows, cols=cols)
    print(f"Расшифрованный текст: {decrypted_text}")

    # Проверка соответствия с примером из задания
    expected_cipher = "НАЙМЙРГЩЖБГВАБ"
    print(f"Ожидаемый шифртекст из примера: {expected_cipher}")
    print(f"Совпадение: {ciphertext == expected_cipher}")

    # Дополнительный пример для проверки
    print("\n" + "=" * 50)
    print("Дополнительный пример:")

    test_text = "ПРИВЕТ"
    test_keyword = "ШИФР"

    print(f"Ключевое слово: {test_keyword}")
    print(f"Текст: {test_text}")

    test_table = create_playfair_table(test_keyword, rows=4, cols=8)
    print_table(test_table)

    encrypted = playfair_encrypt(test_text, test_keyword, rows=4, cols=8)
    decrypted = playfair_decrypt(encrypted, test_keyword, rows=4, cols=8)

    print(f"Зашифровано: {encrypted}")
    print(f"Расшифровано: {decrypted}")