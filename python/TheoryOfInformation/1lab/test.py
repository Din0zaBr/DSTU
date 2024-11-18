txt, ascii_txt = input(), ''
for el in txt:
    ascii_txt += str(bin(ord(el)))[2:]
    print(ascii_txt)


def input_matrix(k, n):
    """
    Функция для ввода матрицы с заданными количеством строк k и столбцов n.

    :param k: Количество строк матрицы
    :param n: Количество столбцов матрицы
    :return: Введенная матрица
    """
    matrix = []
    print(f"Введите элементы матрицы {k}x{n}:")

    for i in range(k):
        row = []
        print(f"Введите элементы {i + 1}-й строки (через пробел):")
        row_input = input().split()

        if len(row_input) != n:
            print(f"Ошибка: Введено неверное количество элементов. Ожидалось {n}, получено {len(row_input)}.")
            return None

        for elem in row_input:
            try:
                row.append(int(elem))
            except ValueError:
                print(f"Ошибка: '{elem}' не является числом.")
                return None

        matrix.append(row)

    return matrix


# Пример использования функции
k = int(input("Введите количество строк (k): "))
n = int(input("Введите количество столбцов (n): "))

matrix = input_matrix(k, n)

if matrix:
    print("Введенная матрица:")
    for row in matrix:
        print(row)
else:
    print("Ошибка при вводе матрицы.")
