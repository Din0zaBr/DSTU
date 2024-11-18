txt, bin_list_txt, max_len_el = input(), [], -1
for el in txt:
    temp = str(bin(ord(el)))[2:]
    len_temp = len(temp)
    print(el, end=" ")

    bin_list_txt.append(temp)

    if len_temp > max_len_el:
        max_len_el = len_temp
print()
print(bin_list_txt)

bin_list_txt = ['0' * (max_len_el - len(el)) + el for el in bin_list_txt]
print(bin_list_txt)


def input_matrix(k, n):
    """
    Функция для ввода матрицы с заданными количеством строк k и столбцов n,
    где каждый элемент должен быть либо 1, либо 0.

    :param k: Количество строк матрицы
    :param n: Количество столбцов матрицы
    :return: Введенная матрица
    """
    matrix = []
    print(f"Введите элементы матрицы {k}x{n} (каждый элемент должен быть либо 1, либо 0):")

    for i in range(k):
        while True:
            row = []
            print(f"Введите элементы {i + 1}-й строки (через пробел):")
            row_input = input().split()

            if len(row_input) != n:
                print(
                    f"Ошибка: Введено неверное количество элементов. Ожидалось {n}, получено {len(row_input)}. Попробуйте снова.")
                continue

            valid = True
            for elem in row_input:
                if elem not in ['0', '1']:
                    print(f"Ошибка: '{elem}' не является допустимым значением (должно быть 0 или 1). Попробуйте снова.")
                    valid = False
                    break
                row.append(int(elem))

            if valid:
                matrix.append(row)
                break

    return matrix


def find_identity_columns(matrix):
    """
    Функция для нахождения столбцов, которые образуют единичную квадратную матрицу.

    :param matrix: Введенная матрица
    :return: Список индексов столбцов, которые образуют единичную квадратную матрицу
    """
    k = len(matrix)
    identity_columns = []

    for i in range(k):
        for j in range(k):
            if matrix[i][j] == 1 and j not in identity_columns:
                identity_columns.append(j)
                break

    return identity_columns


def create_Hsys(matrix):
    """
    Функция для создания матрицы Hsys.

    :param matrix: Введенная матрица
    :return: Матрица Hsys
    """
    identity_columns = find_identity_columns(matrix)
    Hsys = []

    for row in matrix:
        new_row = [row[i] for i in identity_columns] + row[len(identity_columns):]
        Hsys.append(new_row)

    return Hsys


def create_Gsys(matrix):
    """
    Функция для создания матрицы Gsys.

    :param matrix: Введенная матрица
    :return: Матрица Gsys
    """
    identity_columns = find_identity_columns(matrix)
    Gsys = []

    for row in matrix:
        new_row = row[:len(identity_columns)] + [row[i] for i in identity_columns]
        Gsys.append(new_row)

    return Gsys


# Пример использования функции
k = int(input("Введите количество строк (k): "))
n = int(input("Введите количество столбцов (n): "))

matrix_type = input("Хотите ли вы создать матрицу H или матрицу G? (введите H или G): ").upper()

if matrix_type not in ['H', 'G']:
    print("Неверный выбор. Пожалуйста, введите H или G.")
    exit()

matrix = input_matrix(k, n)

if matrix_type == 'H':
    Hsys = create_Hsys(matrix)
    print("Матрица Hsys:")
    for row in Hsys:
        print(row)
elif matrix_type == 'G':
    Gsys = create_Gsys(matrix)
    print("Матрица Gsys:")
    for row in Gsys:
        print(row)
