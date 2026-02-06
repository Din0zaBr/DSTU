from TchKa.first_lab.sixth import binary_euclid, final


def main():
    while True:
        try:
            task, mod = (int(input("Введите номер задания (1, 2, 3, 4): ")),
                         int(input("Введите 1 (Шифрование) или 2 (Дешифрование): ")))
            if task == 1:
                alp = input(
                    "Введите алфавит (по умолчанию АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ): " or "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
                key = int(input("Введите ключ шифрования (сдвиг): "))
                if mod == 1:
                    phrase: str = input("Введите сообщения для шифрования: ").upper()
                    if checking_caesar(key, alp):  # проверка
                        encrypted_phrase = encrypt_caesar(phrase, key, alp)  # шифрованное сообщение
                        print(encrypted_phrase)
                elif mod == 2:
                    phrase: str = input("Введите сообщения для дешифрования: ").upper()
                    if checking_caesar(key, alp):  # проверка
                        decrypted_phrase = decrypt_caesar(phrase, key, alp)  # шифрованное сообщение
                        print(decrypted_phrase)
            if task == 2:
                alp = input(
                    "Введите алфавит (по умолчанию АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ): " or "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
                a, b = int(input("Введите a: ")), int(input("Введите b: "))
                k1, k2, degree_of_two = binary_euclid(a, len(alp))
                if mod == 1:
                    phrase = input("Введите сообщения для шифрования: ").upper()
                    if final(k1, k2, degree_of_two) == 1:
                        encrypted_phrase = encrypt_affina_caesar(a, b, phrase, alp)  # шифрованное сообщение
                        print(encrypted_phrase)
                elif mod == 2:
                    phrase = input("Введите сообщения для дешифрования: ").upper()
                    if final(k1, k2, degree_of_two) == 1:
                        decrypted_phrase = decrypt_affina_caesar(a, b, phrase, alp)  # шифрованное сообщение
                        print(decrypted_phrase)
            if task == 3:
                alp = input(
                    "Введите алфавит (по умолчанию АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ): " or "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
                key = int(input("Введите первую часть ключа (число): "))
                keyword = input("Введите первую часть ключа (слово): ").upper()
                keyword_unique = ''.join(unique_ordered(keyword))
                if mod == 1:
                    phrase = input("Введите сообщения для шифрования: ").upper()
                    if checking_caesar(key, alp):  # проверка
                        encrypted_phrase = encrypt_caesar_with_keyword(phrase, key,
                                                                       keyword_unique, alp)  # шифрованное сообщение
                        print(encrypted_phrase)
                elif mod == 2:
                    phrase = input("Введите сообщения для дешифрования: ").upper()
                    if checking_caesar(key, alp):  # проверка
                        decrypted_phrase = decrypt_caesar_with_keyword(phrase, key,
                                                                       keyword_unique, alp)  # шифрованное сообщение
                        print(decrypted_phrase)
            if task == 4:
                alp = input(
                    "Введите алфавит (по умолчанию АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ): " or "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ").upper()
                keyword = input("Введите ключевое слово: ").upper()
                rows = int(input("Введите количество строк таблицы (по умолчанию 4): ") or "4")
                cols = int(input("Введите количество столбцов таблицы (по умолчанию 8): ") or "8")
                if mod == 1:
                    text = input("Введите текст для шифрования: ").upper()
                    if checking_trisemus(rows, cols, alp):  # проверка
                        encrypted_phrase = encrypt_trisemus(text, keyword, alp, rows, cols)  # шифрованное сообщение
                        print(encrypted_phrase)
                elif mod == 2:
                    text = input("Введите текст для дешифрования: ").upper()
                    if checking_trisemus(rows, cols, alp):  # проверка
                        decrypted_phrase = decrypt_trisemus(text, keyword, alp, rows, cols)  # шифрованное сообщение
                        print(decrypted_phrase)
        except:
            print('D=')


def checking_caesar(key, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    if key > len(alp):
        print("Ключ выходит за длину алфавита")
        print(f"Текущий ключ = {key % len(alp)}")
        return key % len(alp)
    else:
        return True


def encrypt_caesar(phrase, key, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    alp += alp
    encrypted_phrase = ''
    for letter in phrase:
        if letter not in alp:
            encrypted_phrase += letter
        else:
            letter_index = alp.index(letter)
            encrypted_phrase += alp[letter_index + key]

    return encrypted_phrase


def decrypt_caesar(encrypted_phrase, key, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    alp += alp
    decrypted_phrase = ''
    for letter in encrypted_phrase:
        if letter not in alp:
            decrypted_phrase += letter
        else:
            letter_index = alp.rindex(letter)
            decrypted_phrase += alp[letter_index - key]

    return decrypted_phrase


def encrypt_affina_caesar(a, b, phrase, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    encrypted_phrase = ''

    for letter in phrase:
        if letter not in alp:
            encrypted_phrase += letter
        else:
            letter_index = (a * alp.index(letter) + b) % len(alp)
            encrypted_phrase += alp[letter_index]
    return encrypted_phrase


def decrypt_affina_caesar(a, b, encrypted_phrase, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    decrypted_phrase = ""
    table = {}

    for index in range(len(alp)):
        letter_index = (a * index + b) % len(alp)
        table[letter_index] = index

    for letter in encrypted_phrase:
        if letter not in alp:
            decrypted_phrase += letter
        else:
            letter_index = alp.index(letter)
            decrypted_phrase += alp[table[letter_index]]
    return decrypted_phrase


def unique_ordered(lst):
    return list(dict.fromkeys(lst))


def caesar_with_keyword(key, keyword_unique, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    temp_alp = keyword_unique
    curr_alp = ''
    for alp_index in range(len(alp) - key):
        if alp[alp_index] in temp_alp:
            continue
        else:
            temp_alp += alp[alp_index]
    for letter in alp:
        if letter in temp_alp:
            continue
        else:
            curr_alp += letter
    curr_alp += temp_alp
    return curr_alp


def encrypt_caesar_with_keyword(phrase, key, keyword_unique, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    curr_alp = caesar_with_keyword(key, keyword_unique)
    my_alp_dict = dict(zip(alp, curr_alp))
    encrypted_phrase = ''
    for letter in phrase:
        if letter not in curr_alp:
            encrypted_phrase += letter
        else:
            encrypted_phrase += my_alp_dict[letter]

    return encrypted_phrase


def decrypt_caesar_with_keyword(encrypted_phrase, key, keyword_unique, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    curr_alp = caesar_with_keyword(key, keyword_unique)
    my_alp_dict = dict(zip(curr_alp, alp))
    decrypted_phrase = ''
    for letter in encrypted_phrase:
        if letter not in alp:
            decrypted_phrase += letter
        else:
            decrypted_phrase += my_alp_dict[letter]

    return decrypted_phrase


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


def encrypt_trisemus(phrase, keyword, alp='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', rows=4, cols=8):
    table = create_trisemus_table(keyword, alp, rows, cols)
    encrypted_phrase = ''

    for char in phrase:
        if char not in ''.join(table):
            encrypted_phrase += char
            continue
        # Ищем букву в таблице
        for row_idx, row in enumerate(table):
            if char in row:
                col_idx = row.index(char)
                # Берем букву снизу (если последняя строка - берем из первой)
                next_row_idx = (row_idx + 1) % rows
                encrypted_char = table[next_row_idx][col_idx]
                encrypted_phrase += encrypted_char
                break

    return ''.join(encrypted_phrase)


def decrypt_trisemus(ciphertext, keyword, alp, rows=4, cols=8):
    table = create_trisemus_table(keyword, alp, rows, cols)

    decrypted_text = ''

    for char in ciphertext:
        if char not in ''.join(table):
            decrypted_text += char
            continue

        for row_idx, row in enumerate(table):
            if char in row:
                col_idx = row.index(char)
                prev_row_idx = (row_idx - 1) % rows
                decrypted_char = table[prev_row_idx][col_idx]
                decrypted_text += decrypted_char
                break

    return ''.join(decrypted_text)


def checking_trisemus(rows, cols, alp):
    if rows * cols > len(alp):
        print(f"Количество букв в алфавите = {len(alp)}, что меньше чем {rows * cols} элементов")
        return False
    elif rows * cols < len(alp):
        print(f"Количество букв в алфавите = {len(alp)}, что больше чем {rows * cols} элементов")
        return False
    else:
        return True


if __name__ == '__main__':
    main()
