def main():
    while True:
        try:
            task, mod = (int(input("Введите 1 или 2 (номер задания): ")),
                         int(input("Введите 1 (Шифрование) или 2 (Дешифрование): ")))
            if task == 1:
                if mod == 1:
                    phrase: list = list(input("Введите сообщения для шифрования: "))
                    row_count, colum_count = map(int,
                                                 input("Введите количество строк и столбцов через пробел: ").split())
                    table: list = [[] for _ in range(colum_count)]
                    array = 0
                    if checking_first(phrase, row_count, colum_count):  # проверка
                        for row in range(0, row_count * colum_count, row_count):  # заполнение таблицы
                            table[array] = phrase[row:(row + 1 * row_count)]
                            array += 1
                        keyword: list = list(input("Введите ключевое слово: "))
                        my_dict = dict(zip(keyword, table))  # сопоставление буквы к определённому отрезку текста
                        encrypted_phrase = encrypt_1(my_dict, keyword)  # шифрованное сообщение
                        print(encrypted_phrase)
                        print()
                elif mod == 2:
                    true_keyword: list = list(input("Введите ключевое слово: "))
                    row_count, colum_count = map(int,
                                                 input("Введите количество строк и столбцов через пробел: ").split())
                    encrypted_phrase_list: list = list(input("Введите сообщения для дешифрования: "))
                    encrypted_phrase_dict = {}
                    encrypted_keyword = sorted(true_keyword)
                    # Разбиваем зашифрованный текст обратно на столбцы
                    # Берем каждый colum_count-ый символ для каждого столбца
                    for col_index in range(colum_count):
                        letter = encrypted_keyword[col_index]
                        column = []
                        for row_index in range(row_count):
                            char_index = row_index * colum_count + col_index
                            if char_index < len(encrypted_phrase_list):
                                column.append(encrypted_phrase_list[char_index])
                        encrypted_phrase_dict[letter] = column
                    decrypted_message = decrypt_1(true_keyword, encrypted_phrase_dict)  # дешифрованное сообщение
                    print(decrypted_message)
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


def checking_first(phrase, row_count, colum_count):
    if len(phrase) > row_count * colum_count:
        print("Фраза не поместится в таблицу")
        return False
    elif len(phrase) < row_count * colum_count:
        print("В таблице будет присутствовать свободное место")
        return False
    else:
        return True


def checking_second(matrix):
    if len(matrix) != len(matrix[0]):
        print("Это не квадратная матрица!")
        return False
    n = len(matrix)
    # Вычисляем суммы строк
    row_sums = [sum(row) for row in matrix]
    # Вычисляем суммы столбцов
    col_sums = [sum(matrix[row][col] for row in range(n)) for col in range(n)]
    # Вычисляем суммы диагоналей
    sm_diag1 = sum(matrix[i][i] for i in range(n))
    sm_diag2 = sum(matrix[i][n - i - 1] for i in range(n))
    # Проверяем, что все суммы строк одинаковы
    all_row_sums_equal = all(s == row_sums[0] for s in row_sums)
    if not all_row_sums_equal:
        print("Все суммы строк не одинаковы!")
        return False
    # Проверяем, что все суммы столбцов одинаковы
    all_col_sums_equal = all(s == col_sums[0] for s in col_sums)
    if not all_col_sums_equal:
        print("Все суммы столбцов не одинаковы!")
        return False
    # Проверяем, что суммы строк и столбцов одинаковы между собой
    all_sums_equal = row_sums[0] == col_sums[0]
    if not all_sums_equal:
        print("Все суммы строк и столбцов не одинаковы между собой!")
        return False
    # Проверяем, что суммы диагоналей также совпадают с суммами строк и столбцов
    diagonals_equal = row_sums[0] == sm_diag1 and row_sums[0] == sm_diag2
    if not diagonals_equal:
        print("Все суммы диагоналей не совпадают с всеми суммами строк и столбцов!")
        return False
    # Проверяем, что все числа от 1 до n^2 встречаются ровно один раз
    all_numbers_present = sorted(sum(matrix, [])) == list(range(1, n * n + 1))
    if not all_numbers_present:
        print("Последовательность чисел должна начинаться с 1!")
        return False
    if all_row_sums_equal and all_col_sums_equal and all_sums_equal and diagonals_equal and all_numbers_present:
        return True


def encrypt_1(my_dict, keyword):
    # Сортируем ключевое слово и получаем отсортированные столбцы
    sorted_keyword = sorted(keyword)
    sorted_columns = [my_dict[letter] for letter in sorted_keyword]
    
    # Читаем по строкам (по 1 символу из каждого столбца)
    encrypted_phrase = []
    if sorted_columns:
        for row_index in range(len(sorted_columns[0])):
            for column in sorted_columns:
                if row_index < len(column):
                    encrypted_phrase.append(column[row_index])
    
    return ''.join(encrypted_phrase)


def decrypt_1(keyword, my_dict):
    # Получаем столбцы в правильном порядке (согласно исходному ключевому слову)
    columns = [my_dict[letter] for letter in keyword]
    print(columns)
    # Читаем по столбцам (сначала весь первый столбец, потом второй и т.д.)
    decrypted_phrase = []
    for column in columns:
        decrypted_phrase.extend(column)
    
    return ''.join(decrypted_phrase)


def encrypt_2(phrase, table):
    n = len(table[0])
    encrypted_table = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            index_of_letter = table[i][j]
            encrypted_table[i][j] = phrase[index_of_letter - 1]

    return encrypted_table


def decrypt_2(encrypted_table, table):
    n = len(table[0])
    phrase = ""
    stop = 1
    while stop != n * n + 1:
        for i in range(n):
            for j in range(n):
                if table[i][j] == stop:
                    phrase += encrypted_table[i][j]
        stop += 1

    return phrase


if __name__ == '__main__':
    main()
