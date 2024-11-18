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


# Пример использования функции
k = int(input("Введите количество строк (k): "))
n = int(input("Введите количество столбцов (n): "))

matrix = input_matrix(k, n)

print("Введенная матрица:")
for row in matrix:
    print(row)
