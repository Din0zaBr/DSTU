def main():
    while True:
        try:
            alp = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
            task, mod = (int(input("Введите 1 или 2 (номер задания): ")),
                         int(input("Введите 1 (Шифрование) или 2 (Дешифрование): ")))
            if task == 1:
                if mod == 1:
                    phrase: str = input("Введите сообщения для шифрования: ").upper()
                    key = int(input())
                    if checking_ceasar(key, alp):  # проверка
                        encrypted_phrase = encrypt_Ceasar(phrase, key)  # шифрованное сообщение
                        print(encrypted_phrase)
                elif mod == 2:
                    phrase: str = input("Введите сообщения для шифрования: ").upper()
                    key = int(input())
                    if checking_ceasar(key, alp):  # проверка
                        decrypted_phrase = encrypt_Ceasar(phrase, key)  # шифрованное сообщение
                        print(decrypted_phrase)
            if task == 2:
                if mod == 1:
                    phrase = input("Введите сообщения для шифрования: ").upper()
                    a, b = int(input()), int(input())
                    if 1:
                        encrypted_phrase = encrypt_affina_ceasar(a, b, phrase, alp)  # шифрованное сообщение
                        print(encrypted_phrase)
                if mod == 2:
                    phrase = input("Введите сообщения для дешифрования: ").upper()
                    a, b = int(input()), int(input())
                    if 1:
                        decrypted_phrase = decrypt_affina_ceasar(a, b, phrase, alp)  # шифрованное сообщение
                        print(decrypted_phrase)





                else:
                    print('Попробуйте почитать D=')
            elif task == 2:
                if mod == 1:
                    row_count, colum_count = map(int,
                                                 input("Введите количество строк и столбцов через пробел: ").split())
                    table: list = [[int(input("Введите цифру или число: ")) for _ in range(row_count)] for _ in
                                   range(colum_count)]
                    print(table)
                    if checking_second(table):
                        phrase: list = list(input("Введите сообщения для шифрования: "))
                        encrypted_message = encrypt_2(phrase, table)
                        print(encrypted_message)
                elif mod == 2:
                    row_count, colum_count = map(int,
                                                 input("Введите количество строк и столбцов через пробел: ").split())
                    encrypted_table: list = [[input("Введите символ шифр текста: ") for _ in range(row_count)] for _ in
                                             range(colum_count)]
                    table: list = [[int(input("Введите цифру или число: ")) for _ in range(row_count)] for _ in
                                   range(colum_count)]
                    if checking_second(table) and len(encrypted_table) == len(encrypted_table[0]):
                        decrypted_message = decrypt_2(encrypted_table, table)
                        print(decrypted_message)
                else:
                    print('Попробуйте почитать D=')
            else:
                print('Попробуйте почитать D=')
        except:
            print('D=')


def checking_ceasar(key, alp):
    if key > len(alp):
        print("Ключ выходит за длину алфавита")
        print(f"Текущий ключ = {key % len(alp)}")
        return key % len(alp)


def encrypt_Ceasar(phrase, key):
    alp = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    encrypted_phrase = ''
    for letter in phrase:
        if letter not in alp:
            encrypted_phrase += letter
        else:
            letter_index = alp.index(letter)
            encrypted_phrase += alp[letter_index + key]

    return encrypted_phrase


def decrypt_Ceasar(encrypted_phrase, key):
    alp = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    decrypted_phrase: dict = {}
    for letter in encrypted_phrase:
        if letter not in alp:
            decrypted_phrase += letter
        else:
            letter_index = alp.rindex(letter)
            decrypted_phrase += alp[letter_index - key]

    return decrypted_phrase


def encrypt_affina_ceasar(a, b, phrase, alp):
    encrypted_phrase = ''

    for letter in phrase:
        if letter not in alp:
            encrypted_phrase += letter
        else:
            letter_index = (a * alp.index(letter) + b) % len(alp)
            encrypted_phrase += alp[letter_index]
    return encrypted_phrase


def decrypt_affina_ceasar(a, b, encrypted_phrase, alp):
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


if __name__ == '__main__':
    main()
